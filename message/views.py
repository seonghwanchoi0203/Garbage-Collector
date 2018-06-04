from django.shortcuts import render
from userprof.models import ExtendedUser, AdminUser
from message.models import Inquiry, Offer
from message.form import InquiryAdd, OfferAdd,WithdrawForm,DeclineForm,AcceptForm
from django.shortcuts import redirect
import datetime
from garbage.models import Garbage
from django.shortcuts import get_object_or_404
# Create your views here.

# front end should, At the first time, write the cost of item to negotiate_price
# Later write the price of offer to the negotiate_price

#TODO : Front end work
'''
1. When this function is first called [from item page], the 'negotiate_price' should set to the initial garbage price.
2. When actual negotiation is happening [which is in the profile page], the 'negotiate_price' should
   be set to the buyer's offering price.
'''
def inquiry(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')
    current_user = request.user
    e_user = ExtendedUser.objects.get(user=current_user)
    if request.method == 'POST':
        form = InquiryAdd(request.POST)
        if form.is_valid():
            inquiry_out = Inquiry(sender=e_user)
            garbage = get_object_or_404(Garbage, id=form.cleaned_data['garbage_id'])
            inquiry_out.receiver = garbage.owner
            inquiry_out.title = form.cleaned_data['title']
            inquiry_out.content = form.cleaned_data['content']
            inquiry_out.garbage = garbage
            inquiry_out.date = datetime.date.today()
            inquiry_out.negotiate_price = form.cleaned_data['negotiate_price']
            inquiry_out.accept = False
            inquiry_out.read = False
            inquiry_out.withdraw = False
            inquiry_out.transaction_id = 0
            inquiry_out.save()
        return redirect('/profile')


def offer(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')
    current_user = request.user
    e_user = ExtendedUser.objects.get(user=current_user)
    print(e_user)
    a_user = AdminUser.objects.get(extended_user=e_user)
    if request.method == 'POST':
        form = OfferAdd(request.POST)
        print(form)
        if form.is_valid():
            instance = Offer(sender=a_user)
            instance.receiver = get_object_or_404(ExtendedUser, id= form.cleaned_data['extended_user_id'])
            inquiry_from_buyer = get_object_or_404(Inquiry, id= form.cleaned_data['inquiry_id'])
            instance.inquiry = inquiry_from_buyer
            instance.title = form.cleaned_data['title']
            instance.content = form.cleaned_data['content']
            instance.garbage = inquiry_from_buyer.garbage
            instance.res_date = datetime.date.today()
            instance.read = False
            instance.continueMessage = True
            instance.decline = False
            instance.negotiate_price = form.cleaned_data['negotiate_price']
            instance.save()
    return redirect('/sell')

#TODO : Front end work
'''
1. When actual negotiation is happening [which is in the profile page], the 'negotiate_price' should
   be set to the buyer's offering price.
'''
def withdraw(request): ## BUYER to SELLER DECLINE AN INQUIRY
    if not request.user.is_authenticated:
        return redirect('/accounts/login')
    current_user = request.user
    e_user = ExtendedUser.objects.get(user=current_user)
    if request.method == 'POST':
        form = WithdrawForm(request.POST)
        if form.is_valid():
            inquiry_out = Inquiry(sender=e_user)
            garbage = get_object_or_404(Garbage, id=form.cleaned_data['garbage_id'])
            inquiry_out.receiver = garbage.owner
            inquiry_out.title = "The buyer withdrawed the request"
            inquiry_out.content = "The Inquiry has been withdrawed"
            inquiry_out.garbage = garbage
            inquiry_out.date = datetime.date.today()
            inquiry_out.accept = False
            inquiry_out.read = False
            inquiry_out.withdraw = True
            inquiry_out.negotiate_price = form.cleaned_data['negotiate_price']
            inquiry_out.save()
    return redirect('/profile')

#TODO : Front end work
'''
1. When seller declines (basically when seller doesn't not wish to change the price) 
'''
def decline(request): ## SELLER to BUYER DECLINE AN INQUIRY
    if not request.user.is_authenticated:
        return redirect('/accounts/login')
    current_user = request.user
    print("??????")
    e_user = ExtendedUser.objects.get(user=current_user)
    a_user = AdminUser.objects.get(extended_user=e_user)
    if request.method == 'POST':
        form = DeclineForm(request.POST)
        print(form)
        if form.is_valid():
            print("!!!!!")
            instance = Offer(sender=a_user)
            instance.receiver = get_object_or_404(ExtendedUser, id=form.cleaned_data['extended_user_id'])
            inquiry_from_buyer = get_object_or_404(Inquiry, id=form.cleaned_data['inquiry_id'])
            instance.inquiry = inquiry_from_buyer
            instance.title = "Seller declined the inquiry"
            instance.content = "The inquiry has been declined"
            instance.garbage = inquiry_from_buyer.garbage
            instance.res_date = datetime.date.today()
            instance.read = False
            instance.continueMessage = False
            instance.decline = True
            instance.negotiate_price = form.cleaned_data['negotiate_price']
            instance.save()
    return redirect('/sell')

#TODO : Front end work
'''
1. When actual reservation (transaction) is happening [which is in the profile page], the 'negotiate_price' should
   be set to the buyer's offering price.
'''

'''
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    inquiry = models.ForeignKey(Inquiry,on_delete=models.CASCADE,related_name='inquiry')
    sender = models.ForeignKey(ExtendedUser, on_delete=models.CASCADE, related_name='ExtendedUser')
    receiver = models.ForeignKey(AdminUser, on_delete=models.CASCADE, related_name='AdminUser')
    garbage = models.ForeignKey(Garbage,on_delete=models.CASCADE)
    res_date = models.DateTimeField(blank=True, null=True)
    title = models.CharField(max_length=80, blank=True)
    content = models.CharField(max_length=1000, blank=True)
    negotiate_price = models.FloatField(default=0)
    continueMessage = models.BooleanField(blank=True,default=True)
    decline = models.BooleanField(blank=True,default=False)
    read = models.BooleanField(default=False)
'''


def buyer_accept(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')
    current_user = request.user
    e_user = ExtendedUser.objects.get(user=current_user)
    if request.method == 'POST':
        form = AcceptForm(request.POST)

        if form.is_valid():
            ## Get data from form
            garbage = get_object_or_404(Garbage, id=form.cleaned_data['garbage_id'])
            print(garbage)
            inquiry_from_buyer = get_object_or_404(Inquiry, id=form.cleaned_data['inquiry_id'])
            transaction_id = form.cleaned_data['transaction_id']
            negotiate_price = form.cleaned_data['negotiate_price']

            ## Message to BUYER
            offer_out = Offer(sender=garbage.owner, receiver=e_user)
            offer_out.res_date = datetime.date.today()
            offer_out.inquiry = inquiry_from_buyer
            offer_out.garbage = inquiry_from_buyer.garbage
            offer_out.read = False
            offer_out.decline = True
            offer_out.continueMessage = False
            if garbage.sold:
                offer_out.title = "It is Sold"
                offer_out.content = "The Item has been Sold"
                offer_out.negotiate_price = -1
                offer_out.save()
                print('not accept by seller ')
                return redirect('/profile')
            else:
                ## another If here to do actual payment
                garbage.sold = True
                garbage.buyer = e_user
                garbage.save(force_update=True)
                offer_out.title = "Success"
                offer_out.content = "The Item has been successfully reserved"
                offer_out.negotiate_price = negotiate_price
                offer_out.save()
            #Message to Seller
                inquiry_out = Inquiry(sender=e_user,receiver= garbage.owner)
                inquiry_out.read = False
                inquiry_out.garbage = garbage
                inquiry_out.date = datetime.date.today()
                inquiry_out.negotiate_price = negotiate_price
                inquiry_out.accept = True
                inquiry_out.withdraw = False
                #inquiry_out.transaction_id = e_user.stripeID
                inquiry_out.title = "Successfully Sold"
                inquiry_out.content = "The Item has been successfully reserved"
                inquiry_out.save()

        return redirect('/profile')





