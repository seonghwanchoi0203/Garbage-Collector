from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import get_template
from django.contrib.auth.models import User
from django.contrib.postgres.search import SearchVector
from urllib.request import urlopen
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
import stripe

# from django.contrib.gis.measure import D #
# from django.contrib.gis.geos import Point
# from django.contrib.gis.geoip import GeoIP

from django.forms.models import model_to_dict

# from message.models import Message, ResMessage
from django.contrib.auth.models import User
import os
import json

import nltk
from nltk.corpus import wordnet


from uszipcode import ZipcodeSearchEngine
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
    import ssl
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        pass
    else:
        ssl._create_default_https_context = _create_unverified_https_context

    nltk.download('punkt')
    nltk.download('averaged_perceptron_tagger')
    nltk.download('wordnet')

    try:
        current_user = request.user
        e_user = get_object_or_404(ExtendedUser, user=current_user)
        a_user = get_object_or_404(AdminUser, extended_user=e_user)
        garbages = Garbage.objects
        garbages = garbages.exclude(owner=a_user)
    except:
        garbages = Garbage.objects.all()

    garbages = garbages.exclude(sold=True)
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
        temp_dict['location'] = {'latitude': x.latitude, 'longitude': x.longitude}
        temp_dict['photos'] = x.photos.url
        temp_dict['postdate'] = tmp
        temp_dict['city'] = x.city
        temp_dict['state'] = x.state
        ret_list.append(temp_dict)
    json_garbage = json.dumps(ret_list,cls=UUIDEncoder)

    #print(json_garbage)
    context = {'garbage': garbages,
               'json_garbage':json_garbage,
               }

    return render(request, 'index.html', context)

def search(request):
    garbages = Garbage.objects.none()
    search_query = request.POST['searchBar']
    sentences = nltk.sent_tokenize(str(search_query)) #tokenize sentences
    nouns = [] #empty to array to hold all nouns
    for sentence in sentences:
        for word,pos in nltk.pos_tag(nltk.word_tokenize(str(sentence))):
            if (pos == 'NN' or pos == 'NNP' or pos == 'NNS' or pos == 'NNPS'):
                nouns.append(word)
                print(word)
    #garbages = Garbage.objects.annotate(
    #				search=SearchVector('title', 'description'),
    #		   ).filter(search = search_query)
    if not nouns: #if no nouns are detected, use the exact same text to search
        nouns = search_query.split()
    query = []
    for n in nouns: #expend nouns to query by adding synonyms
        query.append(n)
        if wordnet.synsets(str(n)):
            for syn in wordnet.synsets(str(n)): #str(n)+".n.01"
                for l in syn.lemmas():
                    query.append(l.name())
    for q in query:
        res_q = Garbage.objects.annotate(
            search=SearchVector('title', 'description'),
        ).filter(search = str(q))
        garbages |= res_q
    ret_list = []

    try:
        current_user = request.user
        e_user = get_object_or_404(ExtendedUser, user=current_user)
        a_user = get_object_or_404(AdminUser, extended_user=e_user)
        garbages = garbages.exclude(owner=a_user)
    except:
        garbages = garbages

    garbages = garbages.exclude(sold=True)
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
        temp_dict['location'] = {'latitude': x.latitude, 'longitude': x.longitude}
        temp_dict['photos'] = x.photos.url
        temp_dict['postdate'] = tmp
        temp_dict['city'] = x.city
        temp_dict['state'] = x.state
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

def ratepage(request):
    if request.method == 'POST':
        pid = request.POST['edit']
        garbage = get_object_or_404(Garbage, id=pid)
    return render(request, 'rate.html',{'garbage':garbage})

def about(request):
    return render(request, 'about.html')

def buyerMessage(request):
    return render(request, 'buyerMessage.html')

def inAppTransaction(request):
    return render(request, 'inAppTransaction.html')


def watch(request):
    if not request.user.is_authenticated:
        print("no is_authenticated")
        return redirect("/accounts/login")
    current_user = request.user
    e_user = get_object_or_404(ExtendedUser, user=current_user)
    pid = request.POST['edit']
    instance = get_object_or_404(Garbage, id=pid)
    seller = instance.owner
    extend_seller = seller.extended_user
    w = Watch(user=e_user, garbage=instance, date_watch=date.today())
    temp_dict = {}
    temp_dict['latitude'] = instance.latitude
    temp_dict['longitude'] = instance.longitude
    json_temp = json.dumps(temp_dict)
    mine = False
    print(w)
    w.save()
    try:
        if request.method == 'POST':
            context = {'title': instance.title, 'description': instance.description, 'cost': instance.cost,
                       'photos': instance.photos, 'zipcode': instance.zipcode, 'condition': instance.condition,
                       'distance': instance.distance, 'owner': instance.owner, 'postdate': instance.postdate,
                       'watched': True, 'id': instance.id,'sold':instance.sold,'rating': instance.owner.rate*12,
                        'json_pos':json_temp,'photo':extend_seller.photos,
                         'mine':mine}
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
            instance = get_object_or_404(Garbage, id=pid)
            seller = instance.owner
            extend_seller = seller.extended_user
            temp_dict = {}
            temp_dict['latitude'] = instance.latitude
            temp_dict['longitude'] = instance.longitude
            json_temp = json.dumps(temp_dict)
            mine = False
            context = {'title': instance.title, 'description': instance.description, 'cost': instance.cost,
                       'photos': instance.photos, 'zipcode': instance.zipcode, 'condition': instance.condition,
                       'distance': instance.distance, 'owner': instance.owner, 'postdate': instance.postdate,
                       'watched': False, 'id': instance.id,'garbage':instance.id,'sold':instance.sold,
                        'json_pos':json_temp,'rating': instance.owner.rate*12, 'photo':extend_seller.photos,
                        'mine':mine}
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

@login_required
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
        sendfrom = "new"
        if form.is_valid():
            print("lalal")
            sendfrom = "new"
            instance.cost = form.cleaned_data['cost']
            instance.title = form.cleaned_data['title']
            instance.condition = form.cleaned_data['condition']
            instance.description = form.cleaned_data['description']
            instance.photos = form.cleaned_data['photos']
            if(form.cleaned_data['Latitude'] == None or form.cleaned_data['Longitude'] == None):
                search = ZipcodeSearchEngine()
                res = search.by_city_and_state(e_user.city, e_user.state)
                instance.location = Point(res[0]["Latitude"],res[0]["Longitude"])
                instance.latitude = res[0]["Latitude"]
                instance.longitude = res[0]["Longitude"]
            else:
                instance.location = Point(form.cleaned_data['Latitude'], form.cleaned_data['Longitude'])
                instance.latitude = instance.location.coords[0]
                instance.longitude = instance.location.coords[1]
            instance.city,instance.state = getplace(instance.latitude, instance.longitude,e_user.city,e_user.state)
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



def getplace(lat, lon, city, state):
    try:
        url = "http://maps.googleapis.com/maps/api/geocode/json?"
        url += "latlng=%s,%s&sensor=false" % (lat, lon)
        v = urlopen(url).read()
        j = json.loads(v)
        print(j)
        components = j['results'][0]['address_components']
        for c in components:
            if "administrative_area_level_1" in c['types']:
                state = c['short_name']
            if "administrative_area_level_2" in c['types']:
                city = c['long_name']
    except:
        return city, state
    return city, state


def contact(request):
    return render(request, 'contact.html')

def delete(request):
    if request.method == "POST":
        pid = request.POST['delete']
        instance = get_object_or_404(Garbage, id=pid)
        instance.delete()
    return redirect(sell)

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
    mine = False;
    pid = request.GET.get('garbage')
    instance = get_object_or_404(Garbage, id=pid)
    seller = instance.owner
    extend_seller = seller.extended_user
    current_user = request.user
    temp_dict = {}
    temp_dict['latitude'] = instance.latitude
    temp_dict['longitude'] = instance.longitude
    json_temp = json.dumps(temp_dict)
    try:
        e_user = get_object_or_404(ExtendedUser,user=current_user)
    except:
        context = {'title': instance.title, 'description': instance.description, 'cost': instance.cost,
                   'photos': instance.photos, 'zipcode': instance.zipcode, 'condition': instance.condition,
                   'distance': instance.distance, 'owner': instance.owner, 'postdate': instance.postdate, 'watched': False,
                   'id': instance.id, 'photo':extend_seller.photos, 'rating':seller.rate*12,'sold':instance.sold,
                    'json_pos':json_temp,
                    'mine':mine
                   }
        return render(request, 'ItemDetails.html', context)

    a_user = get_object_or_404(AdminUser, extended_user=e_user)
    if a_user == seller:
        mine = True
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
        'photo':extend_seller.photos, 'rating': seller.rate * 12,
        'sold':instance.sold,
        'json_pos':json_temp,
        'mine':mine
    }
    print(context)
    return render(request, 'ItemDetails.html', context)

def pay(request):

    stripe.api_key = "sk_test_BQokikJOvBiI2HlWgH4olfQ2"

    token = request.form['stripeToken']  # Using Flask

    charge = stripe.Charge.create(amount=999,
                                  currency='usd',
                                  description='Example charge',
                                  source=token, )

def welcome(request):
    return render(request,'welcome.html')