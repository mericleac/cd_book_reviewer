from django.shortcuts import render, redirect
from .models import *

def index (request):
    if 'errors' not in request.session:
        request.session['errors'] = {}
    context = {
        'errors': request.session['errors']
    }
    return render(request, 'registration_app/index.html', context)

def register (request):
    errors = User.objects.register_validator(request.POST)
    if len(errors):
        request.session['errors'] = errors
        return redirect('/')
    else:
        import bcrypt
        hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        user = User(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], hashed_password=hashed_pw)
        user.save()
        request.session['current_user'] = user.id
        request.session['action'] = 'registered'
        return redirect('/books')

def login (request):
    errors = User.objects.login_validator(request.POST)
    if len(errors):
        request.session['errors'] = errors
        return redirect('/')
    else:
        request.session['current_user'] = User.objects.get(email=request.POST['email']).id
        request.session['action'] = 'logged in'
        return redirect('/books')

def success (request):
    if 'current_user' in request.session:
        user = User.objects.get(id=request.session['current_user'])
        request.session['errors'] = {}
        return render(request, 'registration_app/success.html', { 'user': User.objects.get(id=request.session['current_user']) })
    else:
        return redirect('/')

def show_user(request, user_id):
    from django.db.models import Count
    user = User.objects.get(id=int(user_id))
    total_reviews = User.objects.annotate(num_reviews=Count('reviews')).order_by('num_reviews')
    context = {
        'user': user,
        'reviews': user.reviews.all(),
        'total_reviews': total_reviews.get(id=int(user_id)).num_reviews,
    }
    return render(request, 'registration_app/user.html', context)

def logout (request):
    request.session['current_user'] = None
    return redirect('/')
