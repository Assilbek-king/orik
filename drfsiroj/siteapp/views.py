from django.shortcuts import render, redirect
from api.models import *
# Create your views here.


def indexHandler(request):
    if not request.session.get('user_id', None):
        return redirect('/login')

    user_id = request.session.get('user_id', None)
    active_user = None
    if user_id:
        active_user = UserSite2.objects.get(id=int(user_id))



    return render(request, 'index.html',{

        'active_user': active_user
    })

def zakazHandler(request):
    if not request.session.get('user_id', None):
        return redirect('/login')

    user_id = request.session.get('user_id', None)
    active_user = None
    if user_id:
        active_user = UserSite2.objects.get(id=int(user_id))

    carts = Cart2.objects.filter(status__gt=-1)

    return render(request, 'tables-data.html',{
        'carts': carts,
        'active_user': active_user

    })

def moyzakazHandler(request):
    if not request.session.get('user_id', None):
        return redirect('/login')

    user_id = request.session.get('user_id', None)
    active_user = None
    if user_id:
        active_user = UserSite2.objects.get(id=int(user_id))

    carts = Cart2.objects.filter(status__gt=-1).filter(siteuser__id = active_user.id)

    return render(request, 'tables-data.html',{
        'carts': carts,
        'active_user': active_user

    })

def zakazItemHandler(request,or_id):
    if not request.session.get('user_id', None):
        return redirect('/login')

    user_id = request.session.get('user_id', None)
    active_user = None
    if user_id:
        active_user = UserSite2.objects.get(id=int(user_id))

    cart = Cart2.objects.get(id=int(or_id))
    return render(request, 'users-profile.html',{
        'cart': cart,
        'active_user': active_user

    })


def loginHandler(request):
    if request.POST:
        email = request.POST.get('email', {})
        password = request.POST.get('password', {})
        if email and password:

            site_user = UserSite2.objects.filter(email=email).filter(password=password)

            if site_user:
                site_user = site_user[0]
                request.session['user_id'] = site_user.id
                return redirect('/')
            else:
                print('User not found')
        else:
            print('Error arguments')

    return render(request, 'pages-login.html', {
    })

def logoutHandler(request):
    request.session['user_id'] = None
    return redirect('/login')


