from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^add$', views.add),
    url(r'^process_add$', views.process_add),
    url(r'^(?P<book_id>\d+)$', views.show_book),
    url(r'^(?P<book_id>\d+)/process_review$', views.process_review),
    url(r'^(?P<book_id>\d+)/delete_review/(?P<review_id>\d+)$', views.delete_review),
]