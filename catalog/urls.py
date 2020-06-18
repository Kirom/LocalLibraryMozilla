from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^books/$', views.BookListView.as_view(), name='books'),
    # url(r'^book/(?P<pk>\d+)$', views.BookDetailView.as_view(), name='book-detail'),
    url(r'^book/(?P<slug>[-\w]+)$', views.BookDetailView.as_view(), name='book-detail'),
    url(r'^book/instance/(?P<pk>[-\w]+)$', views.BookInstanceDetailView.as_view(), name='book-instance-detail'),
    url(r'^authors/$', views.AuthorListView.as_view(), name='authors'),
    url(r'^author/(?P<pk>\d+)$', views.AuthorDetailView.as_view(), name='author-detail'),
    url(r'^mybooks/$', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    url(r'^on_loan_books/$', views.AllLoanedBooksListView.as_view(), name='on-loan'),
    url(r'^book/(?P<pk>[-\w]+)/renew/$', views.renew_book_librarian, name='renew-book-librarian'),
    url(r'^author/create/$', views.AuthorCreate.as_view(), name='author_create'),
    url(r'^author/(?P<pk>\d+)/update/$', views.AuthorUpdate.as_view(), name='author_update'),
    url(r'^author/(?P<pk>\d+)/delete/$', views.AuthorDelete.as_view(), name='author_delete'),
    url(r'^books/create/$', views.BookCreate.as_view(), name='book_create'),
    url(r'^book/(?P<slug>[-\w]+)/update/$', views.BookUpdate.as_view(), name='book_update'),
    url(r'^book/(?P<slug>[-\w]+)/delete/$', views.BookDelete.as_view(), name='book_delete'),
]
# TO DO Примечание: В качестве дополнительного задания, рассмотрите возможность того, как вы могли бы закодировать url
#  на список всех книг, вышедших в определенный год, месяц, день и какое РВ (паттерн) должно соответствовать этому.
# url(r'^books/(?P<year>\d{0,4}&<month>\d{0,2}&<day>\d{0,2})$', views.BookListView.as_view(), name='books'),
