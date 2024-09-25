from random import randint
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail, EmailMessage
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import CreateView, ListView

from djangoProject.settings import DEFAULT_FROM_EMAIL
from userextend.forms import UserForm
from userextend.models import UserHistory


class UserCreateView(CreateView):
    template_name = 'userextend/create_user.html'
    model = User
    form_class = UserForm
    success_url = reverse_lazy('login')

    # Aceasta metoda form_valid este folosita pentru clasele de view-uri(CreateView, UpdateView, DeleteView etc)
    # Atunci cand datele din formular sunt trimise catre salvare, programatorul poate sa suplimenteze cu actiuni noi

    def form_valid(self, form):
        if form.is_valid():
            new_user = form.save(commit=False)  # Cand commit=False datele nu sunt salvate in baza de date.

            # 1. Scriere cu litera mare first_name si last_name
            new_user.first_name = new_user.first_name.title()
            # Atribui user.first_name.title() campului first_name din cadrul obiectului user
            new_user.last_name = new_user.last_name.title()

            # 2. Generarea username-ului

            new_user.username = f'{new_user.first_name[0].lower()}{new_user.last_name.lower().replace(" ", "")}_{randint(100000, 999999)}'

            new_user.is_active = False

            new_user.save()

            # 3. Trimitere mail

            subject = 'Create a new user'
            message = f'Hello, {new_user.first_name} {new_user.last_name}\n Your username: {new_user.username}.'
            # send_mail(subject, message, DEFAULT_FROM_EMAIL, [new_user.email])

            # 4. Activarea contului FARA TEMPLATE DE MAIL

            # Generare token de activare

            token = default_token_generator.make_token(new_user)  # Generare token pentru utilizator
            uid = urlsafe_base64_encode(force_bytes(new_user.id))  # Generare codificare pentru utilizator
            activation_url = self.request.build_absolute_uri(
                reverse_lazy('activate', kwargs={'uid64': uid, 'token': token})
            )
            subject = 'Activate your account!'
            # message = f'Please use the following link to activate your account {activation_url}.\n' \
            #           f'Your username is: {new_user.username}'
            # send_mail(subject, message, DEFAULT_FROM_EMAIL, [new_user.email])

            # 5. Activarea contului CU TEMPLATE DE MAIL

            details_user = {
                'fullname': f'{new_user.first_name} {new_user.last_name}',
                'username': new_user.username,
                'activation_url': activation_url
            }

            message = get_template('email.html').render(details_user)
            mail = EmailMessage(subject, message, DEFAULT_FROM_EMAIL, [new_user.email])
            mail.content_subtype = 'html'
            mail.send()

            # 6. Istoric folosind modelul UserHistory

            user_data = {
                'last_login': new_user.last_login,
                'is_superuser': new_user.is_superuser,
                'username': new_user.username,
                'last_name': new_user.last_name,
                'email': new_user.email,
                'is_staff': new_user.is_staff,
                'first_name': new_user.first_name
            }

            # Adaugam o instanta noua in tabela userextend - userhistory

            UserHistory.objects.create(user_data=user_data)

        return redirect('login')


def activate_user(request, uid64, token):
    # La apelarea functiei (adica utilizatorul da click din mail pe link) utilizatorul va trimite uid si tokenul
    try:  # Incercam decodarea uid-ului si apoi gasirea userului cu id-ul respectiv
        uid = urlsafe_base64_decode(uid64).decode()  # Se decodeaza uid in id-ul userului
        user = get_object_or_404(User, pk=uid)  # Stocam in variabila user obiectul User daca cu id-ul decodat din uid exista, daca nu 404

    except User.DoesNotExist:  # Daca obiectul nu exista
        user = None  # userul va fi None
    # Daca userul nu este None si tokenul generat exista
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('login')
    else:
        return HttpResponse('NU EXISTA')


class UserHistoryListView(ListView):
    template_name = 'userextend/history.html'
    model = UserHistory
    context_object_name = 'all_histories'
