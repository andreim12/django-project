from student.models import Student
from trainer.models import Trainer


def get_all_students(request):
    return {'students': Student.objects.all()}


# Pasul 1: Adaugare fisier nou numit context_processors.py in folderul djangoProject
# Pasul 2: In fisierul context_processors.py se defineste o functie in care se vor returna toti studentii
# Pasul 3: In fisierul settings.py in variabila templates, unde este context processors se va adauga calea catre
# apelarea functiei get_all_students
# Pasul 4: Implementare in navbar.html

def get_all_trainers(request):
    return {'trainers': Trainer.objects.all()}
