from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product
from django.utils import timezone

def home(request):
    products = Product.objects.order_by('-cnt')
    return render(request, 'products/home.html', {'products':products})

@login_required(login_url='/accounts/signup')
def mysites(request):
    products = Product.objects.filter(hunter=request.user).order_by('-cnt')
    return render(request, 'products/mysites.html', {'products':products})
    
@login_required(login_url='/accounts/signup')
def delete(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=product_id)
        product.delete()
        return mysites(request)

@login_required(login_url='/accounts/signup')
def edit(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        if request.POST['title'] and request.POST['body'] and request.POST['url'] and request.FILES['icon'] and request.FILES['image']:
            product.title = request.POST['title']
            product.body = request.POST['body']
            if request.POST['url'].startswith('http://') or request.POST['url'].startswith('https://'):
                product.url = request.POST['url']
            else:
                product.url = 'http://' + request.POST['url']
            product.icon = request.FILES['icon']
            product.image = request.FILES['image']
            product.pub_date = timezone.datetime.now()
            product.hunter = request.user
            product.save()
            return redirect('/products/' + str(product.id))
        return render(request, 'products/edit.html', {'error':'All fields are required', 'product':product})
    return render(request, 'products/edit.html', {'product':product})


@login_required(login_url='/accounts/signup')
def create(request):
    if request.method == 'POST':
        if request.POST['title'] and request.POST['body'] and request.POST['url'] and request.FILES['icon'] and request.FILES['image']:
            product = Product()
            product.title = request.POST['title']
            product.body = request.POST['body']
            if request.POST['url'].startswith('http://') or request.POST['url'].startswith('https://'):
                product.url = request.POST['url']
            else:
                product.url = 'http://' + request.POST['url']
            product.icon = request.FILES['icon']
            product.image = request.FILES['image']
            product.pub_date = timezone.datetime.now()
            product.hunter = request.user
            product.save()
            product.votes.add(request.user)
            return redirect('/products/' + str(product.id))
        return render(request, 'products/create.html', {'error':'All fields are required'})
    return render(request, 'products/create.html')

def detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'products/detail.html', {'product':product})

@login_required(login_url='/accounts/signup')
def upvote(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=product_id)
        if request.user in product.votes.all():
            product.votes.remove(request.user)
            product.cnt -= 1
        else:
            product.votes.add(request.user)
            product.cnt += 1
        product.save()
        return redirect('/products/' + str(product.id))