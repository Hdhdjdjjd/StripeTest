import uuid

import stripe
from StripeTest import settings
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .models import Stripe

import json
from django.http import HttpResponse, JsonResponse


def buy_view(request):
    return render(request, 'main.html')


def success(request):
    return render(request, "success.html")


def cancel(request):
    return render(request, "cancel.html")


@csrf_exempt
def stripe_session(request):
    if request.method == "GET":
        domain_url = "http://localhost:4242/"
        stripe.api_key = settings.STRIPE_KEY
        user = User.objects.create(username=uuid.uuid4().hex)
        try:
            session = stripe.checkout.Session.create(
                client_reference_id=user.username,
                success_url=domain_url + "success/",
                cancel_url=domain_url + "cancel/",
                mode="subscription",
                line_items=[
                    {
                        "price": 'price_1NwoWqGwSA2rWxXGLqHcBLW1',
                        "quantity": 1,
                    }
                ]
            )

            return redirect(session.url)
        except Exception as e:
            return JsonResponse({"error": str(e)})


@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_KEY
    payload = request.body

    try:
        event = stripe.Event.construct_from(
            json.loads(payload), stripe.api_key
        )
    except ValueError:
        return HttpResponse(status=400)

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]

        client_reference_id = session.get('client_reference_id')
        stripe_customer_id = session.get('customer')
        stripe_subscription_id = session.get("subscription")

        user = User.objects.get(username=client_reference_id)
        Stripe.objects.create(
            user=user,
            customer_id=stripe_customer_id,
            subscription_id=stripe_subscription_id,
        )

    return HttpResponse(status=200)
