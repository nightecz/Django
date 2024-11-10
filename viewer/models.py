from django.db.models import (
  DO_NOTHING, CharField, DateField, DateTimeField, ForeignKey, IntegerField,
  Model, TextField
)


class Genre(Model):
  name = CharField(max_length=128)

  def __str__(self):
    return self.name


class Movie(Model):
  title = CharField(max_length=128)
  genre = ForeignKey(Genre, on_delete=DO_NOTHING)  # Nebo CASCADE dle potřeby
  rating = IntegerField()
  released = DateField()
  description = TextField(blank=True, null=True)  # Popis je volitelný
  created = DateTimeField(auto_now_add=True)

  def __str__(self):
    return f"{self.title} ({self.released.year})"

class Actor(Model):
  first_name = CharField(max_length=50)
  last_name = CharField(max_length=50)
  birth_date = DateField(default=None)

  def __str__(self):
    return f"{self.first_name}  ({self.last_name})"
