

from django.shortcuts import render, redirect
from api.models import *
# Create your views here.
import json
from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

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

@csrf_exempt
def update_order_status(request):
    if request.method == 'POST':
        cart_id = request.POST.get('cart_id')
        status = request.POST.get('status')

        try:
            cart = Cart2.objects.get(id=cart_id)
            cart.status = int(status)

            if status == '2':  # Проверяем, если это подтверждение заказа
                delivery_person_id = request.POST.get('delivery_person_id')
                user_site = UserSite2.objects.get(id=int(delivery_person_id))
                cart.siteuser = user_site

            cart.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))  # Перенаправляем обратно
        except Cart2.DoesNotExist:
            return JsonResponse({'error': 'Заказ не найден'}, status=404)
        except UserSite2.DoesNotExist:
            return JsonResponse({'error': 'Пользователь не найден'}, status=404)
    return JsonResponse({'error': 'Неверный запрос'}, status=400)


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

    return render(request, 'moizakazi.html',{
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


