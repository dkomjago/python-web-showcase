from django.shortcuts import render
from web_app.models import Visit, Message
from django.utils import timezone
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_safe, require_http_methods
from django.contrib import messages
from math import floor


# Main page
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


# Write and submit post page
@require_http_methods(['GET', 'POST', 'HEAD'])
def post(request):
    if request.POST:
        try:
            # Create Message instance
            visit = Visit.objects.filter(id=request.session['visit']).get()
            message = Message(visit=visit,
                              time=timezone.now(),
                              message_text=request.POST.get('message'))
            message.save()
        # Display according creation status
        except:
            messages.error(request, 'Error! Message not published')
        else:
            messages.success(request, 'Message published')

    return render(request, 'messaging/post.html')


# Read posts page
def read(request):
    return render(request, 'messaging/read.html')


# Search function performed by search component on read posts page
@require_safe
def search(request):
    # Get all parameters for query
    get_by = request.GET.get('get_by') + '__contains'
    order_by = request.GET.get('order_by')
    limit = int(request.GET.get('limit'))
    page = int(request.GET.get('page'))
    val = request.GET.get('val')

    # Query
    data = Message.objects\
        .filter(**{get_by: val})\
        .order_by(order_by)\
        .select_related()[page*limit:(page+1)*limit]

    # Convert to string format with according class func and return
    posts = {d.id: d.__str__() for d in data}
    response = {'posts': posts, 'page_count': floor(data.count()/limit)+1}

    return JsonResponse(response)


# Function embedded into each page for session tracking purposes, creates visit instance for each new session
def session(request):
    # Set appropriate username and session end
    kwargs = {
        'username': request.user.username if request.user.is_authenticated else 'anonymous',
        'visit_end': request.session.get_expiry_date()
    }

    # Update info with each call
    if 'visit' in request.session:
        kwargs['id'] = request.session['visit']

    # Save/Update session in db
    visit = Visit(**kwargs)
    visit.save()

    # Set session variable according with ID in db
    request.session['visit'] = visit.id

    return HttpResponse(status=200)
