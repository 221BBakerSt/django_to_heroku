from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import request, HttpResponse

from post.models import Article
from .models import *
from .forms import CommentForm
from django.conf import settings
# Google reCAPTCHA replated libraries
import urllib
import json


@login_required(login_url="/accounts/login/")
def post_comment(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    # get attributes of the comment
    if request.method == "POST":
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():

            """ Begin reCAPTCHA validation """
            recaptcha_response = request.POST.get("g-recaptcha-response")
            url = "https://www.google.com/recaptcha/api/siteverify"
            values = {
                "secret": settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                "response": recaptcha_response
            }
            data = urllib.parse.urlencode(values).encode()
            req = urllib.request.Request(url, data=data)
            response = urllib.request.urlopen(req)
            result = json.loads(response.read().decode())
            """ End reCAPTCHA validation """

            if result["success"]:
                new_comment = comment_form.save(commit=False)
                new_comment.article = article
                new_comment.user = request.user
                new_comment.save()
                return redirect(article)
            else:
                return HttpResponse("reCAPTCHA authentication failed. Please try again.")
        # false requests
        else:
            return HttpResponse("Error in forms. Please try again.")
    # false request methods
    else:
        return HttpResponse("POST requests only.")


@login_required(login_url="/accounts/login/")
def delete_comment(request, article_id, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    comment.delete()
    article = get_object_or_404(Article, article_id=article_id)
    return redirect(article)
