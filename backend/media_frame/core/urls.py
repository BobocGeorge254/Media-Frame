from django.contrib import admin
from django.urls import path, include
from processor.api import urls as processor_urls
from authentication.api import urls as auth_urls
from payments.api import urls as payments_urls

urlpatterns = [
    path('api/processor/', include(processor_urls)),
    path('api/auth/', include(auth_urls)),
    path('api/payments/', include(payments_urls)),
]
