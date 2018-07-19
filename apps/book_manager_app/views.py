from django.shortcuts import render, redirect
from .models import *

def index(request):
    request.session['errors'] = {}
    reviews = Review.objects.all()
    last_three = reviews[len(reviews) - 3:]
    context = {
        'user': User.objects.get(id=request.session['current_user']),
        'reviews': last_three, 
        'books': Book.objects.all()
    }
    return render(request, 'book_manager_app/index.html', context)

def add(request):
    context = {
        'user': User.objects.get(id=request.session['current_user']),
        'books': Book.objects.all()
    }
    return render(request, 'book_manager_app/add.html', context)

def process_add(request):
    book = Book(title=request.POST['title'], author=request.POST['author'])
    book.save()
    review = Review(review=request.POST['review'], stars=int(request.POST['stars']), book=book, user=User.objects.get(id=request.session['current_user']))
    review.save()
    return redirect('/books')

def show_book(request, book_id):
    book = Book.objects.get(id=int(book_id))
    context = {
        'user': User.objects.get(id=request.session['current_user']),
        'book': book,
        'reviews': book.reviews.all()
    }
    return render(request, 'book_manager_app/book.html', context)

def process_review(request, book_id):
    book = Book.objects.get(id=int(book_id))
    user = User.objects.get(id=request.session['current_user'])
    review = Review(review=request.POST['review'], stars=int(request.POST['stars']), book=book, user=user)
    review.save()
    return redirect('/books/' + book_id)

def delete_review(request, review_id, book_id):
    review = Review.objects.get(id=int(review_id))
    review.delete()
    return redirect('/books/' + book_id)
