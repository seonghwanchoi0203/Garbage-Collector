from django.shortcuts import render
from django.shortcuts import redirect
from garbage.models import Garbage, Watch
from django.contrib.auth.models import User
from userprof.models import ExtendedUser, AdminUser
from userprof.form import BioForm, ScoreAdd
from message.models import Inquiry, Offer
from django.shortcuts import get_object_or_404
import datetime
# import stripe


# Create your views here.
def rate(request):
    if not request.user.is_authenticated:
        return redirect('/home')

    current_user = request.user
    rater = get_object_or_404(ExtendedUser, user=current_user)

    if request.method == 'POST':
        form = ScoreAdd(request.POST)
        garbage_id = request.POST['edit']
        print(garbage_id)
        if form.is_valid():
            rate_gave = float(form.cleaned_data['rate'])
            print(rate_gave)
            garbage = get_object_or_404(Garbage, id=garbage_id)
            seller = garbage.owner
            seller.rate = (seller.rate * seller.numberOfRate + rate_gave)*1.0/(seller.numberOfRate +1)
            seller.numberOfRate = seller.numberOfRate + 1
            print("kakaka")
            seller.save()
            return render(request, "userprof.html")


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
    watch = Watch.objects.filter(user=m_user)
    print(watch)
    history = Inquiry.objects.filter(sender=m_user, accept=True)
    inquiry_out = list(Offer.objects.filter(receiver=m_user))
    print(inquiry_out)
    context = {
        "garbage": garbage,
        # "message" : message,
        # "message_type" : message_type,
        # "incoming_requests" : incoming_requests,
        # "outgoing_requests" : outgoing_requests,
        "watch":watch,
        "ongoing_message": inquiry_out,
        "extended_user": m_user,
        "history": history
    }
    return render(request, "userprof.html", context)


def admin_page(request, message=None, success=None):
    if not request.user.is_authenticated():
        return redirect('/home')
    current_user = request.user
    m_user = get_object_or_404(ExtendedUser, user=current_user)
    try:
        a_user = get_object_or_404(AdminUser, extended_user=m_user)
    except:
        return redirect('/home')
    garbage = Garbage.objects.filter(owner=a_user)
    context = dict(garbage=garbage)

    return render(request, "sellerProfile.html", context)


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
        instance = User.objects.get(email=request.user.email)
        form = BioForm(request.POST)
        print('form : ', form.as_p())
        print("Posted")

        if form.is_valid():
            e_user.bio = form.cleaned_data['bio']
            e_user.save()
            print("form is valid!!!")
            #form.save()
            message_type = True
            message = "Item created successfully."
            request.session['message'] = message
            request.session['message_type'] = message_type
            return redirect('/profile')
    elif request.method == 'GET':
        form = BioForm()

    return render(request, "bio.html", {'form': form})



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
    # messages = Message.objects.filter(receiver=current_user, is_reservation=False).order_by('-date')
    # outgoing_requests = ResMessage.objects.filter(message__sender=current_user).order_by('res_date')
    now = datetime.datetime.now()
    # history = ResMessage.objects.filter(message__sender=current_user, res_date__lte = now, is_approved=True).order_by('res_date')
    context = {
        "garbage": garbage,
        # "message" : message,
        # "message_type" : message_type,
        # "incoming_requests" : incoming_requests,
        # "outgoing_requests" : outgoing_requests,
        # "messages"  : messages,
        "admin_user": a_user,
        "extended_user": m_user,
        # "history": history
    }
    return render(request, "sell.html", context)


def userinfo(request):
    return render(request, 'userinfo.html')


def setting(request):
    return render(request, 'setting.html')
