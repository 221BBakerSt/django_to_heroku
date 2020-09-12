from django.shortcuts import render
from django.http import request, HttpResponse
from .models import *
from django.conf import settings
# markdown related libraries
import markdown
import pymdownx
from functools import wraps
from pymdownx.superfences import SuperFencesBlockPreprocessor, highlight_validator
# Google reCAPTCHA replated libraries
import urllib
import json


# render the about page
def about(request):

    owners = Owner.objects.all()
    bulletins = Bulletin.objects.all()

    for bulletin in bulletins:
        # render html syntax in the form of markdown
        bulletin.body = markdown.markdown(bulletin.body,
            extensions=[
            # frequently used syntax extension
            "markdown.extensions.extra",
            # syntax highlight extension
            "markdown.extensions.codehilite",
            "markdown.extensions.admonition",
            "markdown.extensions.fenced_code",
            "markdown.extensions.toc",
            "markdown.extensions.nl2br",
            "pymdownx.superfences",
            "pymdownx.extra",
            "pymdownx.magiclink",
            "pymdownx.tasklist",
            "pymdownx.tilde",
            "pymdownx.caret",
            "pymdownx.tabbed",
            "pymdownx.highlight",
            "pymdownx.inlinehilite",
            ])

    context = {
        "owners": owners,
        "bulletins": bulletins,
    }

    if "GET" == request.method:
        return render(request, "about.html", context)

    # receive info from guest board message
    elif "POST" == request.method:
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
            # instantiate an object
            guest_board = Board()
            guest_board.nickname = request.POST["nickname"]
            guest_board.email = request.POST["email"]
            guest_board.subject = request.POST["subject"]
            guest_board.message = request.POST["message"]
            # record the time and date
            time = __import__("time")
            guest_board.timestamp = time.ctime()
            # save the info above
            guest_board.save()
            return render(request, "about.html", context)
        else:
            return HttpResponse("Failed to leave your message. Please try again.")

    else:
        return HttpResponse("Please use GET or POST to send requests.")


# below are markdown related module operations
def _highlight_validator(language, options):
    filename = options.pop("filename", "")
    okay = highlight_validator(language, options)
    if filename != "":
        options["filename"] = filename
    return okay


def _highlight(method):
    @wraps(method)
    def wrapper(self, src, language, options, md, classes=None, id_value="", **kwargs):
        filename = options.get("filename", "")
        code = method(self, src, language, options, md, classes=classes, id_value=id_value, **kwargs)
        if filename == "":
            return code
        return '<div class="literal-block"><div class="code-block-caption">{}</div>{}</div>'.format(filename, code)
    return wrapper

# Monkey patch pymdownx.superfences for code block caption purpose
pymdownx.superfences.highlight_validator = _highlight_validator
SuperFencesBlockPreprocessor.highlight = _highlight(SuperFencesBlockPreprocessor.highlight)


def music(request):

    songs = Song.objects.all()
    context = {"songs": songs}

    return render(request, "music.html", context)