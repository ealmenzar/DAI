from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from . import models
from .forms import SearchForm, AddForm, DelForm

# Create your views here.

def test():
    return HttpResponse('Hello World!')

def index(request):
    return render(request, 'base.html', {})

@login_required
def modify(request):
    db = models.db
    data = db.restaurants.find({'name': "Indian Oven"})
    dic = {}
    print(type(data))
    for d in data:
        dic['name'] = d['name']

    return render(request, 'modify.html', dic)

@login_required
def search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            restaurant = form.cleaned_data['restaurant']
            db = models.db
            data = db.restaurants.find({'name': restaurant})
            dic = {}
            b = []
            cuisine = " "
            name = " "
            dic['form'] = form
            for d in data:
                b.append(d['borough'])
                cuisine = d['cuisine']
                name = d['name']
            if name == " " and cuisine == " ":
                dic['message'] = "No se ha encontrado ningun restaurante con estos criterios"
            dic['restaurant'] = {'cuisine': cuisine,
                                 'borough': b,
                                 'name': name}
            return render(request, 'search.html', dic)
    else:
        form = SearchForm()
    return render(request, 'search.html', {'form': form})

@login_required
def add(request):
    if request.method == 'POST':
        form = AddForm(request.POST)
        if form.is_valid():
            dic = {'name': form.cleaned_data['name'],
                   'borough': form.cleaned_data['borough'],
                   'cuisine': form.cleaned_data['cuisine']}
            db = models.db
            data = db.restaurants.insert(dic)

            return render(request, 'add.html',
                          {'form': form,
                           'message': 'Restaurante agregado correctamente'})
    else:
        form = AddForm()
    return render(request, 'add.html', {'form': form})

@login_required
def delete(request):
    if request.method == 'POST':
        form = DelForm(request.POST)
        if form.is_valid():
            dic = {'name': form.cleaned_data['name']}
            db = models.db
            db.restaurants.remove(dic)

            return render(request, 'delete.html',
                          {'form': form,
                           'message': 'Restaurante borrado correctamente'})
    else:
        form = DelForm()
    return render(request, 'delete.html', {'form': form})


# python manage.py runserver 0.0.0.0:5000
# http://localhost:8080/restaurantes