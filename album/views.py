from django.shortcuts import render, redirect, get_object_or_404
from django.http import request, HttpResponse
from django.core.paginator import *
from .models import *

# the number of photos shown on every page
NUM_ON_EACH_PAGE = 16

def album(request):
    slide_pics = Slide.objects.all()
    galleries = Gallery.objects.all()
    context = {
        "slide_pics": slide_pics,
        "galleries": galleries,
        }
    return render(request, "album.html", context)

def gallery(request, name):
    gallery = get_object_or_404(Gallery, name=name)
    photos = Photo.objects.filter(gallery__name=name)

    """ beginning of pagination process """
    # set the number of articles shown on every page
    paginator = Paginator(photos, NUM_ON_EACH_PAGE)
    # set the page request variable
    page_request_var = "page"
    # get the page number in URL parameter
    page_num = request.GET.get(page_request_var)
    
    if None == page_num or "" == page_num:
        page_num = 1
    elif str == type(page_num):
        page_num = int(page_num)

    paginated_photos = paginator.get_page(page_num)

    # display range: [current_page - 2, current_page + 2]
    page_range = list(range(max(page_num - 2, 1), page_num)) + list(range(page_num, min(page_num + 2, paginator.num_pages) + 1))
    """ end of pagination process """

    context = {
        "gallery": gallery,
        "photos": paginated_photos,
        "page_range": page_range,
        "page_request_var": page_request_var,
        }
    return render(request, "gallery.html", context)
