from django.http.response import HttpResponse, HttpResponseRedirect
from email.utils import parseaddr
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from apps.DaneUsers.models import UserProfile
User = get_user_model()

def user_registered(request):
    return HttpResponse("Your user has been created")    

def user_notActive(request):
    return render(request, "DaneUsers/deletedAccount.html")

def tryEmail_delete(request):
    return render(request, "DaneUsers/password_reset_email.html")

def user_modified(request):
    return render(request, "DaneUsers/userModified.html")

def recover_account(request, user = ""):
    email_tuple = parseaddr(user)   
    print user
    print email_tuple
    if email_tuple[-1] == "":
        return HttpResponseRedirect(reverse("DaneUsers:login"))
    return HttpResponse("Recover Account")

def isUsernameRegistered(request):
    is_user_in_database = User.objects.filter(email=request.GET.get("username")).exists()
    return HttpResponse(is_user_in_database)

def confirm(request, activation_key):
    user = get_object_or_404(User, activation_key=activation_key)
    user.is_confirmed = True
    user.save()
    return render(request, "DaneUsers/validatedAccount.html")



