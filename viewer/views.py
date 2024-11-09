from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.http import HttpResponse

from django.urls import reverse
from django.views.generic import FormView, ListView, TemplateView
from viewer.models import Movie, Genre
from viewer.forms import MovieForm, GenreForm
from django.urls import reverse_lazy
# Create your views here.

def hello(request):
    value = request.GET.get('value', '')
    aa = request.GET.get('parametr', '')
    if value == 10:
        print()
    return HttpResponse(f'Hello, {value} world! {aa}')


def stranka(request, hodnota):
    return HttpResponse(f'Hodnota stránky: {hodnota}')


def index(request):
    value = request.GET.get('value', '')
    return render(request, template_name='index.html', context={'hodnota': value})

# def login(request):
    # value = request.GET.get('value', '')
    # return render(request, template_name='login.html')#, context={'hodnota': value})

# def register(request):
    # value = request.GET.get('value', '')
    # return render(request, template_name='register.html')#, context={'hodnota': value})

"""
def movie_add(request):
    form = MovieForm()
    # value = request.GET.get('value', '')
    return render(request, template_name='movies.html', context={'form': form})
"""

def register():
    return None

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

    def form_invalid(self, form):
        messages.error(self.request, "Nesprávné uživatelské jméno nebo heslo")
        print("Chyba: Nesprávné přihlášení")  # Přidej log pro kontrolu
        return super().form_invalid(form)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        return super().dispatch(request, *args, **kwargs)



class MoviesView(ListView):
    template_name = 'movies.html'
    model = Movie

class GenreView(ListView):
    template_name = 'genres.html'
    model = Genre

class GenreCreateView(FormView):
    template_name = 'form.html'
    form_class = GenreForm
    success_url = reverse_lazy('genres')

    def form_valid(self, form):
        result = super().form_valid(form)
        cleaned_data = form.cleaned_data
        Genre.objects.create(
            name=cleaned_data['name']
        )
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        # Zkontrolujeme, jestli už nějaké žánry existují
        if Genre.objects.exists():
            # Pokud existují, vrátíme šablonu s hláškou
            return render(request, 'genre_add.html', {
                'message': 'Všechny žánry jsou již přidány!',
            })
        # Jinak zobrazíme formulář
        return super().get(request, *args, **kwargs)
class ProfileView(TemplateView):
    template_name = 'profile.html'

class RegistrationView(TemplateView):
    template_name = 'registration.html'

class MovieCreateView(FormView):
    template_name = 'form.html'
    form_class = MovieForm# Zde je potřeba zadat jen třídu, nikoli její instanci.
    success_url = reverse_lazy('movies') #Zadej platný název URL

    def form_valid(self, form):
        result = super().form_valid(form)
        cleaned_data = form.cleaned_data
        Movie.objects.create(
            title=cleaned_data['title'],
            genre=cleaned_data['genre'],
            rating=cleaned_data['rating'],
            released=cleaned_data['released'],
            description=cleaned_data['description'],
        )
        return super().form_valid(form)  # Použij správný název `form_valid`
        print(result)
        return result