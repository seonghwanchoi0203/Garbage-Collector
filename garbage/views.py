from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import get_template
from django.contrib.auth.models import User
from django.contrib.postgres.search import SearchVector

import datetime
from django.shortcuts import render, redirect
from django.shortcuts import render_to_response, get_object_or_404
from userprof.models import ExtendedUser, AdminUser
from django.shortcuts import render
from garbage.models import Garbage, Watch
from userprof.views import profile,sell
from garbage.form import GarbageAdd, GarbageEdit,ImageUploadForm
from datetime import date
from django.contrib.gis.geos import Point
from django.urls import reverse
from datetime import date


# from django.contrib.gis.measure import D #
# from django.contrib.gis.geos import Point
# from django.contrib.gis.geoip import GeoIP

from django.forms.models import model_to_dict

# from message.models import Message, ResMessage
from django.contrib.auth.models import User
import os
import json

from django.contrib.auth.decorators import login_required
# from django.utils.six.moves.urllib.parse import urlparse

import json
from uuid import UUID


class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            # if the obj is uuid, we simply return the value of uuid
            return obj.hex
        if isinstance(obj, (datetime,date)):
            return obj.isoformat()
        return json.JSONEncoder.default(self, obj)


# Create your views here.
def home(request):
    garbages= []
    garbages = Garbage.objects.all()
    print(type(garbages))
    ret_list = []
    for index, x in enumerate(garbages):
        # some fields with object points need manual translation for json
        # also some additional fields are necessary.
        # moved to a method of the model?
        #temp_dict = model_to_dict(x)
        tmp = x.postdate.isocalendar()
        temp_dict={}
        temp_dict['title'] = x.title
        temp_dict['seller'] = x.owner.getAdminuUserName()
        temp_dict['id'] = x.id.hex
        temp_dict['description'] = x.description
        temp_dict['zipcode'] = x.zipcode
        temp_dict['condition'] = x.condition
        temp_dict['cost'] = x.cost
        temp_dict['location'] = {'latitude': x.location.coords[0], 'longitude': x.location.coords[1]}
        temp_dict['photos'] = x.photos.url
        temp_dict['postdate'] = tmp
        ret_list.append(temp_dict)
    json_garbage = json.dumps(ret_list,cls=UUIDEncoder)

    #print(json_garbage)
    context = {'garbage': garbages,
               'json_garbage':json_garbage,
              }

    return render(request, 'index.html', context)

def search(request):
	garbages = []
	search_query = request.POST['searchBar']
	garbages = Garbage.objects.annotate(
					search=SearchVector('title', 'description'),
			   ).filter(search = str(search_query))
	print ('this is '+ str(search_query))
	ret_list = []

	for index, x in enumerate(garbages):
        	# some fields with object points need manual translation for json
       		# also some additional fields are necessary.
        	# moved to a method of the model?
        	#temp_dict = model_to_dict(x)
		tmp = x.postdate.isocalendar()
		temp_dict={}
		temp_dict['title'] = x.title
		temp_dict['seller'] = x.owner.getAdminuUserName()
		temp_dict['id'] = x.id.hex
		temp_dict['description'] = x.description
		temp_dict['zipcode'] = x.zipcode
		temp_dict['condition'] = x.condition
		temp_dict['cost'] = x.cost
		temp_dict['location'] = {'latitude': x.location.coords[0], 'longitude': x.location.coords[1]}
		temp_dict['photos'] = x.photos.url
		temp_dict['postdate'] = tmp
		ret_list.append(temp_dict)
	json_garbage = json.dumps(ret_list,cls=UUIDEncoder)
	search_res = {'garbage': garbages ,
			'json_garbage': json_garbage,
			} 
	return render(request, 'index.html', search_res)

def about(request):
    return render(request, 'about.html')


def orderComplete(request):
    return render(request, 'orderComplete.html')


def about(request):
    return render(request, 'about.html')

def buyerMessage(request):
    return render(request, 'buyerMessage.html')

def inAppTransaction(request):
    return render(request, 'inAppTransaction.html')

@login_required
def watch(request):
    if not request.user.is_authenticated:
        print("no is_authenticated")
        return redirect("/accounts/login")
    current_user = request.user
    e_user = get_object_or_404(ExtendedUser, user=current_user)
    pid = request.POST['edit']
    print(pid)
    instance = get_object_or_404(Garbage, id=pid)
    print('------')
    w = Watch(user=e_user, garbage=instance, date_watch=date.today())
    print(w)
    w.save()
    try:
        if request.method == 'POST':
            context = {'title': instance.title, 'description': instance.description, 'cost': instance.cost,
                       'photos': instance.photos, 'zipcode': instance.zipcode, 'condition': instance.condition,
                       'distance': instance.distance, 'owner': instance.owner, 'postdate': instance.postdate,
                       'watched': True, 'id': instance.id}
            return render(request, 'ItemDetails.html', context)
            #redirect(ItemDetails,context)
            #reverse('ItemDetails', kwargs={'garbage': instance.id})
    except:
        print("no exteneduser or garbage")
        #reverse('ItemDetails', kwargs={'garbage': instance.id})
        redirect("/accounts/login")

    return redirect("/accounts/login")


def unwatch(request):
    if not request.user.is_authenticated:
        return redirect("/accounts/login")
    current_user = request.user
    try:
        e_user = get_object_or_404(ExtendedUser,user=current_user)
        if request.method == 'POST':
            pid = request.POST['unwatch']
            print(pid)
            instance = get_object_or_404(Garbage, id=pid)  # TODO, switch to ID
            context = {'title': instance.title, 'description': instance.description, 'cost': instance.cost,
                       'photos': instance.photos, 'zipcode': instance.zipcode, 'condition': instance.condition,
                       'distance': instance.distance, 'owner': instance.owner, 'postdate': instance.postdate,
                       'watched': False, 'id': instance.id,'garbage':instance.id}
            try:
                watch_list = Watch.objects.filter(user=e_user, garbage=instance)
                watch_list.delete()
                print('???')
                return render(request, 'ItemDetails.html', context)
            except:
                pass
            watch_list = Watch.objects.filter(user=e_user, garbage=instance)
            watch_list.delete()
            return render(request, 'ItemDetails.html', context)
    except:
        redirect("/accounts/login")

    redirect("/accounts/login")


def edit_item(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')
    current_user = request.user
    e_user = ExtendedUser.objects.get(user=current_user)
    try:
        a_user = get_object_or_404(AdminUser, extended_user=e_user)
    except:
        return redirect('/home')

    if a_user.registered is not True:
        return redirect('/home')
    if request.method == 'POST':
        pid = request.POST['send']
        instance = get_object_or_404(Garbage, id=pid)
        form = GarbageEdit(request.POST, request.FILES, instance = instance)
        if form.is_valid():
            instance.cost = form.cleaned_data['cost']
            instance.title = form.cleaned_data['title']
            instance.condition = form.cleaned_data['condition']
            instance.description = form.cleaned_data['description']
            instance.zipcode = form.cleaned_data['zipcode']
            print(form.cleaned_data['photos'])
            instance.photos = form.cleaned_data['photos']
            instance.save(force_update=True)
            return redirect(sell)
    elif request.method == 'GET':
        pid = request.GET['edit']
        instance = get_object_or_404(Garbage, id=pid)  # TODO, switch to ID
        #print(instance)
        form = GarbageEdit(instance=instance)
        sendfrom = "edit"
    return render(request, "new_item.html", {'form': form, 'instance':instance,'pid': pid, 'sendfrom':sendfrom})


def new_item(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')
    current_user = request.user
    e_user = ExtendedUser.objects.get(user=current_user)
    try:
        a_user = get_object_or_404(AdminUser, extended_user=e_user)
    except:
        return redirect('/home')
    if a_user.registered is not True:
        return redirect('/home')
    if request.method == 'POST':
        instance = Garbage(owner=a_user)
        form = GarbageAdd(request.POST, request.FILES, instance=instance)
        #form = GarbageAdd(request.POST)
        #imageForm = ImageUploadForm(request.POST, request.FILES)
        #print(form)
        sendfrom = "edit"
        if form.is_valid():
            print("lalal")
            instance.cost = form.cleaned_data['cost']
            instance.title = form.cleaned_data['title']
            instance.condition = form.cleaned_data['condition']
            instance.description = form.cleaned_data['description']
            instance.zipcode =form.cleaned_data['zipcode']
            instance.photos = form.cleaned_data['photos']
            if(form.cleaned_data['Latitude'] == None or form.cleaned_data['Longitude'] == None):
                instance.location = Point(32.715736, -117.161087)
            else:
                instance.location = Point(form.cleaned_data['Latitude'], form.cleaned_data['Longitude'])
            instance.save()
            message_type = True
            message = "Item created successfully."
            request.session['message'] = message
            request.session['message_type'] = message_type
            return redirect(sell)
    elif request.method == 'GET':
        form = GarbageAdd()
        sendfrom ="new"
    return render(request, "new_item.html", {'sendfrom':sendfrom})


def contact(request):
    return render(request, 'contact.html')


def sendEmail(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        subject = "Garbage Collector Questions"
        from_email = email
        to_email = [settings.DEFAULT_FROM_EMAIL]

        context = {
        'user': name,
        'email': email,
        'message':message
        }

        send_mail(subject, message, from_email, to_email,fail_silently = True)

    return render(request,'contact.html')


def ItemDetails(request):
    pid = request.GET.get('garbage')
    instance = get_object_or_404(Garbage, id=pid)
    current_user = request.user
    try:
        e_user = get_object_or_404(ExtendedUser,user=current_user)
    except:
        context = {'title': instance.title, 'description': instance.description, 'cost': instance.cost,
            'photos': instance.photos, 'zipcode': instance.zipcode, 'condition': instance.condition,
            'distance': instance.distance, 'owner': instance.owner, 'postdate': instance.postdate, 'watched': False,
            'id': instance.id,

        }
        return render(request, 'ItemDetails.html', context)

    watch_list = list(Watch.objects.filter(user=e_user,garbage=instance))
    if len(watch_list) == 0:
        watched = False
    else:
        watched = True
    context = {
        'title': instance.title,
        'description': instance.description,
        'cost': instance.cost,
        'photos': instance.photos,
        'zipcode': instance.zipcode,
        'condition': instance.condition,
        'distance': instance.distance,
        'owner':instance.owner,
        'postdate': instance.postdate,
        'watched': watched,
        'id': instance.id,

    }
    return render(request, 'ItemDetails.html', context)
