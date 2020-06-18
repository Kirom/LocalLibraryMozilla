from django import template

register = template.Library()


def available_book_instances(value, arg):
    # Создание своего(кастомного) фильтра
    # value = BookInstance QuerySet
    # arg = book as string
    # Возвращает кол-во экземпляров книг переданной в arg книги со статусом 'available' (доступных книг)
    return value.filter(book__exact=arg, status__exact='a').count()


register.filter('available_book_instances', available_book_instances)
