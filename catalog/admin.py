from django.contrib import admin

from .models import Book, Language, Author, Genre, BookInstance

# admin.site.register(Book)
admin.site.register(Language)
# admin.site.register(BookInstance)
# admin.site.register(Author)
admin.site.register(Genre)


class BooksInline(admin.TabularInline):
    model = Book
    extra = 0


# Define the admin class
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death',)
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death'), ]
    inlines = [BooksInline]
    list_display_links = ['first_name', 'last_name']


# Register the admin class with the associated model
admin.site.register(Author, AuthorAdmin)


# Register the Admin classes for Book using the decorator
class BooksInstanceInline(admin.TabularInline):
    '''
    Дополнительная таблица, предоставляющая доступ к моделе (BookInstance) из другой модели (Book)
    '''
    model = BookInstance
    # extra - дополнительные поля(заготовки) для добавления
    extra = 0


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    # inlines - Добавляет внизу панель с BookInstance-ами.
    inlines = [BooksInstanceInline]


# Register the Admin classes for BookInstance using the decorator

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_filter = ('status', 'due_back')
    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id',)
        }),
        ('Availability', {
            'fields': ('status', 'due_back', 'borrower',)
        }),
    )
    list_display = ['book', 'status', 'borrower', 'due_back', 'id', ]
