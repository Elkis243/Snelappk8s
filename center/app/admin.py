from django.contrib import admin
from .models import *

admin.site.register([Center, Agent, Subscriber, Invoice])