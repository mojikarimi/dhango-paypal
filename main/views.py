from django.shortcuts import render, redirect
import paypalrestsdk
from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse

paypalrestsdk.configure({
    "mode": "sandbox",  # Change to "live" for production
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_SECRET,
})


# Create your views here.
def index(request):
    if request.method == 'POST':
        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal",
            },
            "redirect_urls": {
                "return_url": request.build_absolute_uri(reverse('success')),
                "cancel_url": request.build_absolute_uri(reverse('cancel')),
            },
            "transactions": [
                {
                    "amount": {
                        "total": "1000.00",  # Total amount in USD
                        "currency": "USD",
                    },
                    "description": "Payment for Product/Service",
                }
            ],
        })

        if payment.create():
            return redirect(payment.links[1].href)  # Redirect to PayPal for payment
        else:
            return render(request, 'index.html')
    return render(request, 'index.html')


def success(request):
    return render(request, 'success.html')


def cancel(request):
    return render(request, 'cancel.html')
