from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

# Create your views here.
from sign.models import Event, Guest


def index(request):
    return render(request, "sign/index.html")


def login_action(request):
    if request.method == 'POST':
        user_name = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=user_name, password=password)
        if user is not None:
            request.session['user'] = user_name
            response = HttpResponseRedirect('/event_manage/')
            return response
        else:
            return render(request, 'sign/index.html', {"error": "账户或密码错误"})


def event_manage(request):
    event_list = Event.objects.all()
    user_name = request.session.get('user', '')

    return render(request, "sign/event_manage.html", {"user_name": user_name,
                                                      'events': event_list})


def guest_manage(request):
    user_name = request.session.get('user', '')
    guest_list = Guest.objects.all()
    paginator = Paginator(guest_list, 2)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    return render(request, "sign/guest_manage.html", {"user": user_name,
                                                      "guests": contacts})

#@login_required
def event_guest_manage(request):
    user_name = request.session.get('user_name', "")
    contacts = []
    if request.method == 'GET':
        event_id = request.GET.get('id')
        if event_id:
            guest_list = Guest.objects.filter(event_id=event_id).order_by('id')
            paginator = Paginator(guest_list, 2)
            page = request.GET.get('page')
            try:
                contacts = paginator.page(page)
            except PageNotAnInteger:
                contacts = paginator.page(1)
            except EmptyPage:
                contacts = paginator.page(paginator.num_pages)
        return render(request, 'sign/guest_manage.html', {'user': user_name,
                                                          'guests': contacts,
                                                          'id': event_id})


#@login_required
def search_name(request):
    user_name = request.session.get('user', '')
    search_name_ = request.GET.get('name', "")
    event_list = Event.objects.filter(name__contains=search_name_)
    return render(request, "sign/event_manage.html", {"user": user_name,
                                                      "events": event_list})


#@login_required
def sign_index(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'sign/sign_index.html', {'event': event})


def sign_index_action(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    phone = request.POST.get('phone', '')

    result = Guest.objects.filter(phone=phone)
    if not result:
        return render(request, 'sign/sign_index.html', {'event': event,
                                                        'hint': '号码错误'})
    result = Guest.objects.filter(event_id=event_id, phone=phone)
    if not result:
        return render(request, 'sign/sign_index.html', {'event': event,
                                                        'hint': '号码错误或者会议号错误'})
    result = Guest.objects.get(event_id=event_id, phone=phone)
    if result.sign:
        return render(request, 'sign/sign_index.html', {'event': event,
                                                        'hint': '已经签过到'})
    else:
        Guest.objects.filter(event_id=event_id, phone=phone).update(sign='1')

        event_limit = Event.objects.get(id=event_id).limit
        str_total_count = '一共' + str(event_limit) + '个人'

        event_message = Event.objects.get(id=event_id)
        sign_count = event_message.guest_set.filter(sign='1').count()
        str_sign_count = '第' + str(sign_count) + '位签到'

        return render(request, 'sign/sign_index.html', {'event': event,
                                                        'hint': '签到成功',
                                                        'guest': result,
                                                        'total_count': str_total_count,
                                                        'sign_count': str_sign_count})

@login_required
def logout(request):
    auth.logout(request)
    response=HttpResponseRedirect('/index/')
    return response