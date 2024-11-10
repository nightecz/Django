"""
URL configuration for hollymovies project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.contrib.auth import views
from django.urls import path
from viewer.models import Genre, Movie
from viewer.views import hello, stranka, index, MovieCreateView, MoviesView, GenreView, GenreCreateView, CustomLoginView, ProfileView, \
    RegisterView, MovieUpdateView, ActorView, ActorCreateView, ActorUpdateView
# django.contrib.auth.urls   když si nepamatuji, ty předpřipravené tak zde v urls najdu
#admin.site.register(Movie)
#admin.site.register(Genre)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('stranka/<hodnota>', stranka),
    path('hello', hello, name='hello'),
    path('', index, name='index'),

    path('login/', CustomLoginView.as_view(), name='login'),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("register", RegisterView.as_view(), name="register"),
    path('profile', ProfileView.as_view(), name="profile"),

    path('movie_add', MovieCreateView.as_view(), name='movie_add'),
    path('movies', MoviesView.as_view(), name='movies'),
    path('movie/update/<pk>', MovieUpdateView.as_view(), name='movie_update'),
    path('genre_add', GenreCreateView.as_view(), name='genre_add'),
    path('genres', GenreView.as_view(), name='genres'),
    path('actors', ActorView.as_view(), name='actors'),
    path('actor/add/', ActorCreateView.as_view(), name='actor_add'),
    path('actor/update/<int:pk>', ActorUpdateView.as_view(), name='actor_update'),
]
