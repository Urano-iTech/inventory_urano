from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.http import HttpResponse
import xlwt
import datetime
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, UpdateView, DetailView, View
from django.contrib.messages.views import SuccessMessageMixin
from django.core.files.storage import FileSystemStorage
from django.contrib.messages.views import messages
from django.db.models import Q
from core.models import *
from core.forms import *

def home(request):
    return render(request,  "customer_template/home.html")


def demoPage(request):
    return HttpResponse("demo Page")

