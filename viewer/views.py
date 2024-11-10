from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.contrib.auth import logout, login
from django.http import HttpResponse

from django.urls import reverse
from django.views.generic import FormView, ListView, TemplateView, UpdateView
from viewer.models import Movie, Genre, Actor
from viewer.forms import MovieForm, GenreForm, SignUpForm, ActorForm
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
        # messages.success(self.request, "Přihlášení se podařilo")
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



class RegisterView(FormView):
    template_name = 'registration/register.html'
    form_class = SignUpForm
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.success_url)

    def for_invalid(self, form):
        messages.error(self.request, form.errors)
        return super().form_invalid(form)

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

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/login')
        return super().dispatch(request, *args, **kwargs)
class MovieUpdateView(UpdateView):
    template_name = 'form.html'
    form_class = MovieForm
    model = Movie
    success_url = reverse_lazy('movies')


    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/login')
        return super().dispatch(request, *args, **kwargs)
class ActorView(ListView):
    template_name = 'actors.html'
    model = Actor

class ActorCreateView(FormView):
    template_name = 'form.html'
    form_class = ActorForm
    success_url = reverse_lazy('actors')

    def form_valid(self, form):
        cleaned_data = form.cleaned_data
        Actor.objects.create(
            first_name=cleaned_data.get('first_name'),
            last_name=cleaned_data.get('last_name'),
            birth_date=cleaned_data.get('birth_date')
        )
        return super().form_valid(form)

class ActorUpdateView(UpdateView):
    template_name = 'form.html'
    form_class = ActorForm
    model = Actor
    success_url = reverse_lazy('actors')