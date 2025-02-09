from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import TalentRegistrationForm, ParentalConsentForm
from .models import TalentProfile, ParentalConsent, BlogPost
from .decorators import role_required
import stripe
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import PayPerView

def register(request):
    if request.method == 'POST':
        form = TalentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            talent = TalentProfile.objects.create(
                user=user,
                full_name=form.cleaned_data['full_name'],
                age=form.cleaned_data['age'],
                portfolio=form.cleaned_data['portfolio'],
                bio=form.cleaned_data['bio'],
                skills=form.cleaned_data['skills'],
                is_minor=form.cleaned_data['age'] < 18
            )
            if talent.is_minor:
                return redirect('parental_consent', talent_id=talent.id)
            login(request, user)
            return redirect('profile')
    else:
        form = TalentRegistrationForm()
    return render(request, 'register.html', {'form': form})

def parental_consent(request, talent_id):
    talent = TalentProfile.objects.get(id=talent_id)
    if request.method == 'POST':
        form = ParentalConsentForm(request.POST)
        if form.is_valid():
            consent = form.save(commit=False)
            consent.talent = talent
            consent.save()
            talent.consent_given = True
            talent.save()
            login(request, talent.user)
            return redirect('profile')
    else:
        form = ParentalConsentForm()
    return render(request, 'parental_consent.html', {'form': form, 'talent': talent})

def profile(request):
    talent = TalentProfile.objects.get(user=request.user)
    return render(request, 'profile.html', {'talent': talent})

def blog(request):
    posts = BlogPost.objects.all()
    return render(request, 'blog.html', {'posts': posts})

@role_required('CASTING')
def casting_dashboard(request):
    return render(request, 'casting_dashboard.html')

@role_required('ADMIN')
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

from .forms import SubscriptionForm

@role_required('TALENT')
def subscribe(request):
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            subscription = form.save(commit=False)
            subscription.user = request.user
            subscription.save()
            return redirect('profile')
    else:
        form = SubscriptionForm()
    return render(request, 'subscribe.html', {'form': form})



def pay_per_view(request, id):
    video = PayPerView.objects.get(id=id)
    return render(request, 'pay_per_view.html', {'video': video})

@csrf_exempt
def create_checkout_session(request, id):
    video = PayPerView.objects.get(id=id)
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': video.title,
                },
                'unit_amount': int(video.price * 100),
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=request.build_absolute_uri('/success/'),
        cancel_url=request.build_absolute_uri('/cancel/'),
    )
    return JsonResponse({'id': session.id})


def homepage(request):
    return render(request, 'homepage.html')