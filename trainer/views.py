from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DetailView, DeleteView

from student.models import Student
from trainer.filters import TrainerFilter
from trainer.forms import TrainerForm, TrainerUpdateForm
from trainer.models import Trainer


class TrainerCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    template_name = 'trainer/create_trainer.html'
    model = Trainer
    form_class = TrainerForm
    success_url = reverse_lazy('home_page')
    permission_required = 'trainer.add_trainer'


class TrainerListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    template_name = 'trainer/list_of_trainers.html'
    model = Trainer
    context_object_name = 'all_trainers'
    permission_required = 'trainer.view_list_of_trainers'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        trainers = Trainer.objects.filter(active=True)
        filters = TrainerFilter(self.request.GET, queryset=trainers)
        context['all_trainers'] = filters.qs
        context['filter_form'] = filters.form

        return context


class TrainerUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    template_name = 'trainer/update_trainer.html'
    model = Trainer
    form_class = TrainerUpdateForm
    success_url = reverse_lazy('list-of-trainers')
    permission_required = 'trainer.change_trainer'


class TrainerDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    template_name = 'trainer/details_trainer.html'
    model = Trainer
    permission_required = 'trainer.view_trainer'


class TrainerDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    template_name = 'trainer/delete_trainer.html'
    model = Trainer
    success_url = reverse_lazy('list-of-trainers')
    permission_required = 'trainer.delete_trainer'


class TrainerStudentListView(LoginRequiredMixin, ListView):
    template_name = 'trainer/student_trainer.html'
    context_object_name = 'all_students'

    def get_queryset(self):
        trainer_id = self.kwargs['trainer_id']
        return Student.objects.filter(trainer_id=trainer_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['trainer'] = Trainer.objects.get(id=self.kwargs['trainer_id'])
        return context
