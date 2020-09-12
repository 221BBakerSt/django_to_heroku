from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import models

# about the authority of each user
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt


@login_required(login_url="/accounts/login/") # decorator, only for logged in users
def profile(request):
    user = request.user
    if request.method == 'POST':
        if request.FILES.get("avatar"):
            user.avatar = request.FILES["avatar"]
            user.save()

            return redirect("/accounts/profile")
        else:
            return HttpResponse("Modification failed. Please step back and try again.")

    elif request.method == 'GET':
        context = {"user": user}
        return render(request, "profile.html", context)
    else:
        return HttpResponse("Use GET or POST to make a request.")
