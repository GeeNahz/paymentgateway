from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.conf import settings
from django.contrib import messages

from . import forms
from .models import Payment



# Create your views here.

def initiate_payment(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        payment_form = forms.PaymentForm(request.POST)
        if payment_form.is_valid():
            payment = payment_form.save()

            context = {
                'payment': payment,
                'paystack_public_key': settings.PAYSTACK_PUBLIC_KEY
            }
            return render(request, 'make_payment.html', context)
    else:
        payment_form = forms.PaymentForm()
    return render(request, 'initiate_payment.html', {'payment_form': payment_form})

# verify the payment
def verify_payment(request: HttpRequest, ref: str) -> HttpResponse:
    payment = get_object_or_404(Payment, ref=ref)
    verified = payment.verified_payment()
    if verified:
        messages.success(request, "Verification successful")
    else:
        messages.error(request, "Verification failed")
    return redirect('initial-payment')