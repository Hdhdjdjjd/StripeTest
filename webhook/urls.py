from django.urls import path
from .views import stripe_webhook, buy_view,stripe_session,success,cancel

urlpatterns = [
    path('buy/', buy_view),
    path('success/', success),
    path('cancel/', cancel),
    path('buy/redirect/', stripe_session),
    path('webhook/', stripe_webhook),

]
