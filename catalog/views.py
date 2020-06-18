import datetime

from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from catalog.forms import RenewBookForm, RenewBookModelForm
from catalog.models import Book, BookInstance, Author, Genre


def index(request):
    """
    Функция отображения для домашней страницы сайта.
    """
    # Генерация "количеств" некоторых главных объектов
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    num_instances_available = BookInstance.objects.filter(status__exact='a').count()  # Доступные книги (статус = 'a')
    num_books_with_1_in_title = Book.objects.filter(title__icontains='1').count()
    num_genres_roman = Genre.objects.filter(name__icontains='roman').count()
    num_authors = Author.objects.count()  # Метод 'all()' применен по умолчанию.

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    # Отрисовка HTML-шаблона index.html с данными внутри
    # переменной контекста context
    return render(request, 'index.html', context={'num_books': num_books, 'num_instances': num_instances,
                                                  'num_instances_available': num_instances_available,
                                                  'num_authors': num_authors,
                                                  'num_books_with_1_in_title': num_books_with_1_in_title,
                                                  'num_genres_roman': num_genres_roman,
                                                  'num_visits': num_visits},
                  )


class BookListView(ListView):
    model = Book
    context_object_name = 'my_book_list'  # ваше собственное имя переменной контекста в шаблоне
    # queryset = Book.objects.filter(title__icontains='1')[:5]  # Получение 5 книг, содержащих слово 'war' в заголовке
    template_name = 'book_list.html'  # Определение имени вашего шаблона и его расположения
    paginate_by = 5


class BookDetailView(DetailView):
    model = Book
    template_name = 'book_detail.html'


class BookInstanceDetailView(DetailView):
    model = BookInstance
    template_name = 'book_instance_detail.html'


class AuthorListView(ListView):
    model = Author
    template_name = 'author_list.html'
    paginate_by = 6


class AuthorDetailView(DetailView):
    model = Author
    template_name = 'author_detail.html'
    extra_context = {'book_instance_query_set': BookInstance.objects.filter()}


class LoanedBooksByUserListView(LoginRequiredMixin, ListView):
    """
    Generic class-based view listing books on loan to current user.
    """
    model = BookInstance
    template_name = 'bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user, status__exact='o').order_by('due_back')


class AllLoanedBooksListView(PermissionRequiredMixin, ListView):
    model = BookInstance
    template_name = 'on_loan_books.html'
    permission_required = 'catalog.book_instance.can_mark_returned'

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')


@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    """
    View function for renewing a specific BookInstance by librarian
    """
    book_inst = get_object_or_404(BookInstance, pk=pk)

    # Если данный запрос типа POST, тогда
    if request.method == 'POST':

        # Создаем экземпляр формы и заполняем данными из запроса (связывание, binding):
        form = RenewBookModelForm(request.POST)

        # Проверка валидности формы:
        if form.is_valid():
            # Обработка данных из form.cleaned_data (здесь мы просто присваиваем их полю due_back)
            book_inst.due_back = form.cleaned_data['due_back']
            book_inst.save()

            # Переход по адресу 'on-loan':
            return HttpResponseRedirect(reverse('on-loan'))

    # Если это GET (или какой-либо еще), создаем форму по умолчанию.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookModelForm(initial={'due_back': proposed_renewal_date, })

    return render(request, 'book_renew_librarian.html', {'form': form, 'bookinst': book_inst})


class AuthorCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'catalog.book_instance.can_mark_returned'
    model = Author
    fields = '__all__'
    initial = {'date_of_death': '12/10/2019', }
    template_name = 'author_form.html'


class AuthorUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'catalog.book_instance.can_mark_returned'
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    template_name = 'author_form.html'


class AuthorDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'catalog.book_instance.can_mark_returned'
    model = Author
    success_url = reverse_lazy('authors')
    template_name = 'author_confirm_delete.html'


class BookCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'catalog.book_instance.can_mark_returned'
    model = Book
    fields = '__all__'
    initial = {'summary': 'Some text', }
    template_name = 'book_form.html'


class BookUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'catalog.book_instance.can_mark_returned'
    model = Book
    fields = ['title', 'author', 'summary', 'isbn', 'genre', 'language', 'slug']
    template_name = 'book_form.html'


class BookDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'catalog.book_instance.can_mark_returned'
    model = Book
    success_url = reverse_lazy('books')
    template_name = 'book_confirm_delete.html'
