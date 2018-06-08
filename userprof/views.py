from django.shortcuts import render
from django.shortcuts import redirect
from garbage.models import Garbage, Watch
from django.contrib.auth.models import User
from userprof.models import ExtendedUser, AdminUser
from userprof.form import BioForm, ScoreAdd
from message.models import Inquiry, Offer
from django.shortcuts import get_object_or_404
import datetime
from uszipcode import ZipcodeSearchEngine
from django.conf import settings
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY



# Create your views here.
def rating(request):
    if not request.user.is_authenticated:
        return redirect('/home')

    current_user = request.user
    rater = get_object_or_404(ExtendedUser, user=current_user)

    if request.method == 'POST':
        form = ScoreAdd(request.POST)
        if form.is_valid():
            garbage_id = request.POST['edit']
            print(garbage_id)
            rate_gave = float(form.cleaned_data['rate'])
            print(rate_gave)
            garbage = get_object_or_404(Garbage, id=garbage_id)
            garbage.isRated = True
            garbage.save(force_update = True)
            seller = garbage.owner
            seller.rate = (seller.rate * seller.numberOfRate + rate_gave)*1.0/(seller.numberOfRate +1)
            seller.numberOfRate = seller.numberOfRate + 1
            seller.save()
    return redirect('/profile')


def profile(request):
    # message = request.session.pop('message', None)
    # message_type = request.session.pop('message_type', None)
    if not request.user.is_authenticated:
        return redirect('/home')
    current_user = request.user
    garbage = []
    # incoming_requests = []
    admin_user = False
    m_user = get_object_or_404(ExtendedUser, user=current_user)
    try:
        a_user = get_object_or_404(AdminUser, extended_user=m_user)
        garbage = Garbage.objects.filter(owner=a_user)
        #incoming_requests = ResMessage.objects.filter(message__receiver=current_user, has_responded=False).order_by('res_date')
        admin_user = True
    except:
        pass
    # messages = Message.objects.filter(receiver=current_user, is_reservation=False).order_by('-date')
    # outgoing_requests = ResMessage.objects.filter(message__sender=current_user).order_by('res_date')
    now = datetime.datetime.now()
    watch = []
    history =[]
    watchList = []
    watch = Watch.objects.filter(user=m_user)
    for w in  watch:
        watchList.append(w.garbage)
    history = Garbage.objects.filter(buyer=m_user, sold=True)
    decline_message = list(Offer.objects.filter(receiver=m_user, decline=True,continueMessage=False))
    success_message = list(Inquiry.objects.filter(sender=m_user))
    inquiry_out = list(Offer.objects.filter(receiver=m_user,decline = False))
    context = {
        "garbage": garbage,
        "decline_message" : decline_message,
        "success_message" : success_message,
        "watch":watchList,
        "ongoing_message": inquiry_out,
        "extended_user": m_user,
        "history": history
    }
    return render(request, "userprof.html", context)


def editBio(request):
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
        e_user = ExtendedUser.objects.get(user=current_user)
        form = BioForm(request.POST, request.FILES, instance=e_user)
        if form.is_valid():
            e_user.bio = form.cleaned_data['bio']
            e_user.first = True
            zipcode_in = form.cleaned_data['zipcode']
            e_user.zipcode = zipcode_in
            search = ZipcodeSearchEngine()
            zipcode = search.by_zipcode(str(zipcode_in))  # type: object
            print(zipcode['City'] == None)
            if(zipcode['City'] == None):
                return render(request, "bio.html", {'form': form, 'instance': e_user, 'error': 'invalidzipcode'})
            e_user.city = zipcode['City']
            e_user.state = zipcode['State']
            e_user.photos = form.cleaned_data['photos']
            e_user.save(force_update = True)
            message_type = True
            message = "User update successfully."
            request.session['message'] = message
            request.session['message_type'] = message_type
            return redirect('/userinfo')
    elif request.method == 'GET':
        form = BioForm(instance=e_user)
    return render(request, "bio.html", {'form': form,'instance':e_user})



def sell(request):
    # message = request.session.pop('message', None)
    # message_type = request.session.pop('message_type', None)
    if not request.user.is_authenticated:
        return redirect('/home')

    current_user = request.user
    garbage = []
    # incoming_requests = []
    admin_user = False
    m_user = get_object_or_404(ExtendedUser, user=current_user)
    try:
        a_user = get_object_or_404(AdminUser, extended_user=m_user)
        garbage = Garbage.objects.filter(owner=a_user)
        #incoming_requests = ResMessage.objects.filter(message__receiver=current_user, has_responded=False).order_by('res_date')
        admin_user = True
    except:
        pass
    history = Garbage.objects.filter(owner=a_user, sold=True)
    inquiry_received = Inquiry.objects.filter(receiver=a_user,withdraw=False)
    send_offer = Offer.objects.filter(sender=a_user)
    withdraw_message = Inquiry.objects.filter(receiver=a_user,withdraw=True)
    garbage = Garbage.objects.filter(owner=a_user,sold=False)
    context = {
        "garbage": garbage,
        "withdraw_message" : withdraw_message,
        "ongoing_message" : inquiry_received,
        "send_offer"  : send_offer,
        "admin_user": a_user,
        "extended_user": m_user,
        "history": history
    }
    return render(request, "sell.html", context)


def userinfo(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')
    current_user = request.user
    e_user = ExtendedUser.objects.get(user=current_user)
    a_user = get_object_or_404(AdminUser, extended_user=e_user)
    return render(request, 'userinfo.html',{'extended_user': e_user,'admin': a_user})


def setting(request):
    return render(request, 'setting.html')

def payment_form(request):
    context = { "stripe_key": settings.STRIPE_PUBLIC_KEY }
    return render(request, "userprof.html", context)

def checkout(request):
    return redirect("profile")
    '''
    new_user = ExtendedUser(
        #model = "Honda Civic",
        #year  = 2017
    )

    if request.method == "POST":
        print("???????")
        token = request.POST.get("stripeToken")



    try:
        charge  = stripe.Charge.create(
            amount      = 2000,
            currency    = "usd",
            source      = token,
        )

        print("ajsdkaskdjjk")

        #new_user.charge_id   = charge.id

    except stripe.error.CardError as ce:
        return False, ce

    else:
        new_user.save()
        return redirect("profile")
        # The payment was successfully processed, the user's card was charged.
        # You can now redirect the user to another page or whatever you want
    '''
