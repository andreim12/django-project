import datetime

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DetailView, DeleteView

from djangoProject.settings import DEFAULT_FROM_EMAIL
from student.filters import StudentFilters
from student.forms import StudentForm, StudentUpdateForm
from student.models import Student, HistoryStudent


# CreateView -> clasa de view dezvoltata de Django folosita pentru a genera un formular si de a salva datele in tabela
# din baza de date.

class StudentCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    template_name = 'student/create_student.html'  # specificam calea catre pagina html pe care o vom folosi in randarea formularului
    model = Student  # specificam modelul pentru care va fi generat formularul
    form_class = StudentForm
    success_url = reverse_lazy('home_page')  # in momentul salvarii datelor din formular utilizatorul va fi redirectionat catre pagina de home
    permission_required = 'student.add_student'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        students = Student.objects.all()
        context['all_students'] = students

        return context

    def form_valid(self, form):
        if form.is_valid():
            new_student = form.save(commit=True)
            new_student.first_name = new_student.first_name.title()
            new_student.last_name = new_student.last_name.title()
            details_student = {
                'fullname': f'{new_student.first_name} {new_student.last_name}',
                'email': f'{new_student.email}',
                'id_student': f'{new_student.id}'
            }

            subject = 'Confirmation student account'
            message = get_template('student/email_student.html').render(details_student)
            recipient_email = new_student.email
            mail = EmailMessage(subject, message, DEFAULT_FROM_EMAIL, [recipient_email])
            mail.content_subtype = 'html'
            mail.send()

            student_data = {
                'first_name': new_student.first_name,
                'last_name': new_student.last_name,
                'email': new_student.email,
                'active': new_student.active
            }

            HistoryStudent.objects.create(message=student_data, created_at=datetime.datetime.now, active=True,
                                          user_id=self.request.user.id)

        return redirect('list-of-students')


# ListView -> clasa de view dezvoltata de Django folosita pentru a afisa o lista de obiecte pe baza unui model

class StudentListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    template_name = 'student/list_of_students.html'
    model = Student
    context_object_name = 'all_students'  # Student.objects.all()
    permission_required = 'student.view_list_of_students'

    # Metoda get_queryset este folosita in view-urile generice pentru a defini ce obiecte sunt trimise si afisate in interfata
    def get_queryset(self):
        return Student.objects.filter(active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        students = Student.objects.filter(active=True)  # Vedem ce studenti trimitem initial in interfata si stocam acelasi query
        filters = StudentFilters(self.request.GET, queryset=students)  # In momentul in care utilizatorul completeaza in interfata formularul de filtrare se realizeaza cautarea studentilor
        context['all_students'] = filters.qs  # Rescriem cheia 'all_students' din dictionarul context prin care trimitem studentii ramasi in urma filtrarii
        context['filter_form'] = filters.form  # Trimitem in html formularul de filtrare

        return context


# UpdateView -> clasa de view dezvoltata de Django folosita pentru a actualiza datele unui obiect

class StudentUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    template_name = 'student/update_student.html'
    model = Student
    form_class = StudentUpdateForm
    success_url = reverse_lazy('list-of-students')
    permission_required = 'student.change_student'


# DetailView -> clasa de view dezvoltata de Django folosita pentru a afisa detaliile unui obiect

class StudentDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    template_name = 'student/details_student.html'
    model = Student
    permission_required = 'student.view_student'

# DeleteView -> clasa de view dezvoltata de Django folosita pentru stergerea unui obiect


class StudentDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    template_name = 'student/delete_student.html'
    model = Student
    success_url = reverse_lazy('list-of-students')
    permission_required = 'student.delete_student'


class HistoryStudentListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    template_name = 'student/history_students.html'
    model = HistoryStudent
    context_object_name = 'history_students'
    permission_required = 'student.view_history_students'

    def get_queryset(self):
        return HistoryStudent.objects.filter(active=True, user_id=self.request.user.id)
