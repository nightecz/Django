import re
from django.core.exceptions import ValidationError
from django.forms import (
    CharField, DateField, Form, IntegerField, ModelChoiceField, Textarea, TextInput, EmailInput, PasswordInput,
    ModelForm, DateInput
)
from viewer.models import Genre, Movie, Actor
from django.contrib.auth.forms import UserCreationForm
from django import forms

class MovieForm(ModelForm):
    # title = CharField(max_length=128)
    # genre = ModelChoiceField(queryset=Genre.objects.all())
    # rating = IntegerField(min_value=1, max_value=10)
    # released = DateField()
    # description = CharField(widget=Textarea, required=False) #widget pro text
    class Meta:
        model = Movie
        fields = "__all__"

    def clean_description(self):
        #každá věta bude začínat velkým písmenem
        initial = self.cleaned_data['description']
        sentences = re.sub(r'\s*\.\s*', '.', initial).split('.')
        return '. '.join(sentence.capitalize() for sentence in sentences if sentence)

    def clean(self):
        result = super().clean()
        if 'genre' in result and 'rating' in result:
            if result['genre'].name.lower() == 'comedy' and result['rating'] > 5:
                self.add_error('genre', 'Comedies should have a rating of 5 or below.')
                self.add_error('rating', 'Comedies should have a rating of 5 or below.')
                raise ValidationError("Comedies aren't usually rated over 5.")
        return result

class GenreForm(Form):
    name = CharField(max_length=128)

class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = ['username', 'first_name', 'last_name', 'email'] #heslo se automaticky dává
        # widgets = {
        #     'username' : TextInput(attrs={'class': 'form-control'}),
        #     'first_name': TextInput(attrs={'class': 'form-control'}),
        #     'email': EmailInput(attrs={'class': 'form-control'}), #je to slovník pro atributy
        #     'last_name': TextInput(attrs={'class': 'form-control'}),
        #     'password1': PasswordInput(attrs={'class': 'form-control'})
        # }
#výše je jedna metoda a níže je druhá
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in ['username', 'first_name', 'email', 'last_name', 'password1', 'password2']:
            self.fields[field_name].widget.attrs['class'] = 'form-control' #dává jiné atributy ve třídě class

class ActorForm(ModelForm):
    # birth_date = forms.DateField()

    class Meta:
        model = Actor
        # fields = ['first_name', 'last_name', 'date_of_birth']
        fields = "__all__"
        widgets = {
            'first_name': TextInput(attrs={'class': 'form-control'}),
            'last_name': TextInput(attrs={'class': 'form-control'}),
            'birth_date': DateInput(attrs={'class': 'form-control', 'type':'date'})
             }