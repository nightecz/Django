import re
from django.core.exceptions import ValidationError
from django.forms import (
    CharField, DateField, Form, IntegerField, ModelChoiceField, Textarea
)
from viewer.models import Genre


class MovieForm(Form):
    title = CharField(max_length=128)
    genre = ModelChoiceField(queryset=Genre.objects.all())
    rating = IntegerField(min_value=1, max_value=10)
    released = DateField()
    description = CharField(widget=Textarea, required=False)

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