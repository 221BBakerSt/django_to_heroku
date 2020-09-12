from django.shortcuts import render, redirect, get_object_or_404
from django.http import request, HttpResponse, JsonResponse
from django.db.models import Count, Q

from .models import *
from django.core.paginator import *
from comment.models import *
# for Ckeditor to show on front-end
from comment.forms import CommentForm
# to deal with cache API
from django.core.cache import cache
# to deal with cache decorator
from django.views.decorators.cache import cache_page

# markdown related libraries
import markdown
import pymdownx
from functools import wraps
from pymdownx.superfences import SuperFencesBlockPreprocessor, highlight_validator


# the number of articles shown on every page
NUM_ON_EACH_PAGE = 10

# process sidebar part
def sidebar(request):
    # get all the categories
    category = Category.objects.all()
    # global the variable so can be called in other functions
    global categories
    # the dictionary is to store key-value pairs of cate_name and cate_count
    categories = {}
    for cate in category:
        # get the number of each category in Article table
        cate_count = Article.objects.filter(category=cate).count()
        # the dictionary contains cate_name and cate_count as key-value pairs
        categories[cate.cate_name] = cate_count
    # reverse sort based on the values of the dict
    # then we get a list like [("Python", 5), ("Django", 2), ("Network", 1)]
    categories = sorted(categories.items(), key=lambda item:item[1], reverse=True)

    # get all the tags
    tag = Tag.objects.all()
    # global the variable so can be called in other functions
    global tags
    # the dictionary is to store key-value pairs of tag_name and tag_count
    tags = {}
    for t in tag:
        # get the number of each tag in Article table
        tag_count = Article.objects.filter(tag=t).count()
        # the dictionary contains tag_name and tag_count as key-value pairs
        tags[t.tag_name] = tag_count
    # reverse sort based on the values of the dict
    # then we get a list like [("Python", 5), ("Django", 2), ("Network", 1)]
    tags = sorted(tags.items(), key=lambda item:item[1], reverse=True)

    # to load links in Userful Links module
    global links
    links = []
    global colors
    colors = ["btn-primary", "btn-warning", "btn-danger", "btn-success", "btn-info", "btn-inverse", "btn-theme", "btn-primary", "btn-warning", "btn-danger"]
    
    link_list = Max_10_Links.objects.all()
    for (link, color) in zip(link_list, colors):
        links.append([link.href, color, link.name])


# preview all blog posts
def post(request):
    # get all featured articles
    articles = Article.objects.filter(featured=True)

    """ beginning of pagination process """
    # set the number of articles shown on every page
    paginator = Paginator(articles, NUM_ON_EACH_PAGE)
    # set the page request variable
    page_request_var = "page"
    # get the page number in URL parameter
    page_num = request.GET.get(page_request_var)

    if None == page_num or "" == page_num:
        page_num = 1
    elif str == type(page_num):
        page_num = int(page_num)
        
    paginated_articles = paginator.get_page(page_num)

    # display range: [current_page - 2, current_page + 2]
    page_range = list(range(max(page_num - 2, 1), page_num)) + list(range(page_num, min(page_num + 2, paginator.num_pages) + 1))
    """ end of pagination process """

    # put category and tag parameters in sidebar
    sidebar(request)

    context = {
        # render the articles on that certain page
        "article_list": paginated_articles,
        "page_range": page_range,
        "last_page": paginator.num_pages,
        "page_request_var": page_request_var,
        "categories": categories,
        "tags": tags,
        "links": links,
        }
    
    return render(request, "blog.html", context)


# check the exact article according to the article_id
def article(request, article_id):
    # receive the article_id parameter from URL, and get the exact article
    # article = Article.objects.filter(featured=True).get(article_id=article_id)
    article = get_object_or_404(Article, article_id=article_id)

    # render html syntax in the form of markdown
    article.body = markdown.markdown(article.body,
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

    # put category and tag parameters in sidebar
    sidebar(request)

    # to show comments of each article
    comments = Comment.objects.filter(article__article_id=article_id)
    # for Ckeditor to show on front-end
    comment_form = CommentForm()

    context = {
        "article": article,
        "user": request.user,
        "categories": categories,
        "tags": tags,
        "links": links,
        "comments": comments,
        "comment_form": comment_form,
        }
    return render(request, "article.html", context)


""" beginning of markdown related module operations """
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
""" end of markdown related module operations """


def search(request):
    # get all featured articles
    articles = Article.objects.filter(featured=True)
    # get the search query after "q=""
    search_query = request.GET.get("q")

    if search_query:
         # pipeline | means OR. distinct means don't show repetitive results
        articles = articles.filter(
            Q(title__icontains=search_query) |
            Q(overview__icontains=search_query) |
            Q(body__icontains=search_query)
            ).distinct()

    """ beginning of pagination process """
    # set the number of articles shown on every page
    paginator = Paginator(articles, NUM_ON_EACH_PAGE)
    # set the page request variable
    page_request_var = "page"
    # get the page number in URL parameter
    page_num = request.GET.get(page_request_var)
    
    if None == page_num or "" == page_num:
        page_num = 1
    elif str == type(page_num):
        page_num = int(page_num)
        
    paginated_articles = paginator.get_page(page_num)

    # display range: [current_page - 2, current_page + 2]
    page_range = list(range(max(page_num - 2, 1), page_num)) + list(range(page_num, min(page_num + 2, paginator.num_pages) + 1))
    """ end of pagination process """

    # put category and tag parameters in sidebar
    sidebar(request)

    context = {
        # render the articles on that certain page
        "article_list": paginated_articles,
        "page_range": page_range,
        "last_page": paginator.num_pages,
        "page_request_var": page_request_var,
        "search_query": search_query,
        "categories": categories,
        "tags": tags,
        "links": links,
        }

    return render(request, "blog.html", context)


def author_filter(request, au):
    # receive the article_id parameter from URL, and get the exact article
    articles = Article.objects.filter(featured=True, author__author_name=au)
    # articles = articles.filter()
    
    """ beginning of pagination process """
    # set the number of articles shown on every page
    paginator = Paginator(articles, NUM_ON_EACH_PAGE)
    # set the page request variable
    page_request_var = "page"
    # get the page number in URL parameter
    page_num = request.GET.get(page_request_var)
    
    if None == page_num or "" == page_num:
        page_num = 1
    elif str == type(page_num):
        page_num = int(page_num)
        
    paginated_articles = paginator.get_page(page_num)

    # display range: [current_page - 2, current_page + 2]
    page_range = list(range(max(page_num - 2, 1), page_num)) + list(range(page_num, min(page_num + 2, paginator.num_pages) + 1))
    """ end of pagination process """

    # put category and tag parameters in sidebar
    sidebar(request)

    context = {
        # render the articles on that certain page
        "article_list": paginated_articles,
        "page_range": page_range,
        "last_page": paginator.num_pages,
        "page_request_var": page_request_var,
        "categories": categories,
        "tags": tags,
        "links": links,
        }

    return render(request, "blog.html", context)


def category_filter(request, cate):
    # receive the article_id parameter from URL, and get the exact article
    articles = Article.objects.filter(featured=True, category__cate_name__in=[cate,])
    
    """ beginning of pagination process """
    # set the number of articles shown on every page
    paginator = Paginator(articles, NUM_ON_EACH_PAGE)
    # set the page request variable
    page_request_var = "page"
    # get the page number in URL parameter
    page_num = request.GET.get(page_request_var)
    
    if None == page_num or "" == page_num:
        page_num = 1
    elif str == type(page_num):
        page_num = int(page_num)
        
    paginated_articles = paginator.get_page(page_num)
    
    # display range: [current_page - 2, current_page + 2]
    page_range = list(range(max(page_num - 2, 1), page_num)) + list(range(page_num, min(page_num + 2, paginator.num_pages) + 1))
    """ end of pagination process """

    # put category and tag parameters in sidebar
    sidebar(request)

    context = {
        # render the articles on that certain page
        "article_list": paginated_articles,
        "page_range": page_range,
        "last_page": paginator.num_pages,
        "page_request_var": page_request_var,
        "categories": categories,
        "tags": tags,
        "links": links,
        }

    return render(request, "blog.html", context)


def tag_filter(request, t):
    # receive the article_id parameter from URL, and get the exact article
    articles = Article.objects.filter(featured=True, tag__tag_name__in=[t,])
    
    """ beginning of pagination process """
    # set the number of articles shown on every page
    paginator = Paginator(articles, NUM_ON_EACH_PAGE)
    # set the page request variable
    page_request_var = "page"
    # get the page number in URL parameter
    page_num = request.GET.get(page_request_var)
    
    if None == page_num or "" == page_num:
        page_num = 1
    elif str == type(page_num):
        page_num = int(page_num)
        
    paginated_articles = paginator.get_page(page_num)

    # display range: [current_page - 2, current_page + 2]
    page_range = list(range(max(page_num - 2, 1), page_num)) + list(range(page_num, min(page_num + 2, paginator.num_pages) + 1))
    """ end of pagination process """

    # put category and tag parameters in sidebar
    sidebar(request)

    context = {
        # render the articles on that certain page
        "article_list": paginated_articles,
        "page_range": page_range,
        "last_page": paginator.num_pages,
        "page_request_var": page_request_var,
        "categories": categories,
        "tags": tags,
        "links": links,
        }

    return render(request, "blog.html", context)
