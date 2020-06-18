import uuid
from datetime import date

from django.db import models

# Create your models here.
from django.db.models.signals import pre_save
from django.urls import reverse
from django.contrib.auth.models import User

from utils import unique_slug_generator


class Genre(models.Model):
    """
    Модель жанра (e.g. Science Fiction, Non Fiction).
    """
    name = models.CharField(max_length=200, help_text="Введите жанр (e.g. Science Fiction, French Poetry etc.)")

    # class Meta:
    #     verbose_name = 'Жанр'
    #     verbose_name_plural = 'Жанры'
    def __str__(self):
        """
        Строковое отображение объекта модели ( в админке так же )
        """
        return self.name


class Language(models.Model):
    """Model representing a Language (e.g. English, French, Japanese, etc.)"""
    name = models.CharField(max_length=200,
                            help_text="Введите язык, на котором написана книга (e.g. English, French, Japanese etc.)")

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return self.name


class Book(models.Model):
    """
    Модель книги представляет всю информацию о доступной книге в общем смысле,
    но не конкретный физический «экземпляр» или «копию» для временного использования.
    """
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    # Foreign Key used because book can only have one author, but authors can have multiple books
    # Author as a string rather than object because it hasn't been declared yet in the file.
    summary = models.TextField(max_length=1000, help_text="Введите краткое описание книги")
    isbn = models.CharField('ISBN', max_length=13,
                            help_text='''13 Character <a href="https://www.isbn-international.org/content/what-isbn">
                            ISBN number</a>''', unique=True)
    genre = models.ManyToManyField(Genre, help_text="Выберите жанр книги")
    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)
    slug = models.SlugField(unique=True, blank=True, null=True)

    # ManyToManyField used because genre can contain many books. Books can cover many genres.
    # Genre class has already been defined so we can specify the object above.

    def __str__(self):
        """
        Строковое отображение объекта модели ( в админке так же )
        """
        return self.title

    def display_genre(self):
        """
        Creates a string for the Genre. This is required to display genre in Admin.
        Потому что жанр - ManyToMany поле.
        """
        return ', '.join([genre.name for genre in self.genre.all()[:3]])

    display_genre.short_description = 'Genre'

    def get_absolute_url(self):
        """
        Возвращает url для доступа к определенному экземпляру книги.
        Returns the url to access a particular book instance.
        """
        return reverse('book-detail', args=[str(self.slug)])


class BookInstance(models.Model):
    """
    Model representing a specific copy of a book (i.e. that can be borrowed from the library).
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text="Уникальный ID для этой копии книги во всей библиотеке")
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m', help_text='Доступность книги')

    class Meta:
        permissions = (("can_mark_returned", "Set book as returned"),)
        ordering = ["due_back"]

    def __str__(self):
        """
        String for representing the Model object
        """
        return f'{self.id} ({self.book.title})'

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False


class Author(models.Model):
    """
    Model representing an author.
    """
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField('Дата рождения', null=True, blank=True)
    date_of_death = models.DateField('Дата смерти', null=True, blank=True)

    def get_absolute_url(self):
        """
        Returns the url to access a particular author instance.
        """
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        """
        String for representing the Model object.
        """
        return f'{self.first_name} {self.last_name}'


def slug_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(slug_generator, sender=Book)
