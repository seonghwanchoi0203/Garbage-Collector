from django.shortcuts import render
from userprof.models import ExtendedUser, AdminUser
from message.models import Inquiry, Offer
from message.form import InquiryAdd, OfferAdd
from django.shortcuts import redirect
import datetime
# Create your views here.


def inquiry(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')
    current_user = request.user
    e_user = ExtendedUser.objects.get(user=current_user)
    if request.method == 'POST':
        form = InquiryAdd(request.POST)
        if form.is_valid():
            inquiry_out = Inquiry(sender=e_user)
            print('hahaha')
            garbage = form.cleaned_data['garbage']
            inquiry_out.receiver = form.cleaned_data['receiver']
            inquiry_out.title = form.cleaned_data['title']
            inquiry_out.content = form.cleaned_data['content']
            inquiry_out.garbage = garbage
            inquiry_out.date = datetime.date.today()
            inquiry_out.accept = form.cleaned_data['accept']
            inquiry_out.read = False
            inquiry_out.withdraw = form.cleaned_data['withdraw']
            inquiry_out.save()
        return redirect('/profile')


def offer(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')
    current_user = request.user
    e_user = ExtendedUser.objects.get(user=current_user)
    a_user = AdminUser.objects.get(extendeduser=e_user)
    if request.method == 'POST':
        form = OfferAdd(request.POST)
        if form.is_valid():
            instance = Offer(sender=a_user)
            instance.inquiry = form.cleaned_data['inqury']
            instance.title = form.cleaned_data['title']
            instance.content = form.cleaned_data['content']
            #instance.garbage = garbage
            instance.res_date = datetime.date.today()
            instance.read = False;
            instance.continueMessage = form.cleaned_data['continueMessage']
            instance.decline = form.cleaned_data['decline']
            instance.negotiate_price = form.cleaned_data['neigotiate_price']
            instance.save();
    return redirect('/profile')


def withdraw(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')
    current_user = request.user
    e_user = ExtendedUser.objects.get(user=current_user)
    if request.method == 'POST':
        form = InquiryAdd(request.POST)
        if form.is_valid():
            inquiry_out = Inquiry(sender=e_user)
            garbage = form.cleaned_data['garbage']
            inquiry_out.receiver = garbage.owner
            inquiry_out.garbage = garbage
            inquiry_out.title = "Withdraw"
            inquiry_out.content = "The Inquiry has been Withdrawed"
            inquiry_out.res_date = datetime.date.today()
            inquiry_out.read = False;
            inquiry_out.continueMessage = form.cleaned_data['continueMessage']
            inquiry_out.decline = form.cleaned_data['decline']
            inquiry_out.save()
    return redirect('/profile')


def decline(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')
    current_user = request.user
    e_user = ExtendedUser.objects.get(user=current_user)
    a_user = AdminUser.objects.get(extendeduser=e_user)
    if request.method == 'POST':
        form = OfferAdd(request.POST)
        if form.is_valid():
            instance = Offer(sender=a_user)
            receiver = form.cleaned_data['receiver']
            instance.receiver= receiver
            instance.title = "Withdrawed"
            instance.content = "The offer has been declined"
            instance.res_date = datetime.date.today()
            instance.read = False;
            instance.decline = form.cleaned_data['decline']
            instance.save()
    return redirect('/profile')


def reserve(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')
    current_user = request.user
    e_user = ExtendedUser.objects.get(user=current_user)
    if request.method == 'POST':
        form = InquiryAdd(request.POST)
        if form.is_valid():
            garbage = form.cleaned_data['garbage']
            inquiry_out = Inquiry(sender=e_user, receiver=garbage.owner)

            inquiry_out.res_date = datetime.date.today()
            if garbage.sold:
                inquiry_out.title = "It is Sold"
                inquiry_out.content = "The Item has been Sold"
                inquiry_out.save()
                print('not accept by seller ')
                return redirect('/profile')
            else:
                garbage.sold = True
                garbage.buyer = e_user
                inquiry_out.title = "Success"
                inquiry_out.content = "The Item has been successfully reserved"
                inquiry_out.save()
                offer_out = Offer(sender=garbage.owner, receiver=e_user, inquiry=inquiry_out)
                offer_out.title = "Success"
                offer_out.content = "The Item has been successfully reserved"
                offer_out.save()
    return redirect('/profile')




