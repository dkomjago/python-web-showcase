from django.shortcuts import render
from web_app.models import Visit, Message
from django.utils import timezone
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_safe, require_http_methods
from django.contrib import messages
from math import floor


def index(request):
    # Number of visits and left messages
    num_visits = Visit.objects.all().count()
    num_messages = Message.objects.all().count()

    # Users who logged in during the last hour
    recent_users = ", ".join([str(d.username) for d in Visit.objects.filter(visit_end__hour=timezone.now().hour)
                              .exclude(username='anonymous')])

    # Visits during the day
    num_daily_visits = Visit.objects.filter(visit_start__day=timezone.now().day).count()

    context = {
        'recent_users': recent_users,
        'num_visits': num_visits,
        'num_messages': num_messages,
        'num_daily_visits': num_daily_visits,
    }

    return render(request, 'messaging/index.html', context=context)


def read(request):
    return render(request, 'messaging/read.html')


@require_http_methods(['GET', 'POST', 'HEAD'])
def post(request):
    if request.POST:
        try:
            visit = Visit.objects.filter(id=request.session['visit']).get()
            message = Message(visit=visit,
                              time=timezone.now(),
                              message_text=request.POST.get('message'))
            message.save()
        except:
            messages.error("Error! Message not published")
        else:
            messages.success(request, 'Message published')
    return render(request, 'messaging/post.html')


@require_safe
def search(request):
    get_by = request.GET.get('get_by') + '__contains'
    order_by = request.GET.get('order_by')
    limit = int(request.GET.get('limit'))
    page = int(request.GET.get('page'))
    val = request.GET.get('val')
    data = Message.objects\
        .filter(**{get_by: val})\
        .order_by(order_by)\
        .select_related()[page*limit:(page+1)*limit]

    posts = {d.id: d.__str__() for d in data}
    response = {'posts': posts, 'page_count': floor(data.count()/limit)+1}
    return JsonResponse(response)


def session(request):
    kwargs = {
        'username': request.user.username if request.user.is_authenticated else 'anonymous',
        'visit_end': request.session.get_expiry_date()
    }
    if 'visit' in request.session:
        kwargs['id'] = request.session['visit']
    visit = Visit(**kwargs)
    visit.save()
    request.session['visit'] = visit.id
    return HttpResponse(status=200)
