from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .models import Post

#takes request as the only parameter
#this parameter is required by all views
def post_list(request):
    object_list = Post.published.all() #all posts with published status
    paginator = Paginator(object_list, 3) # instantiate paginator object with 3 posts in each page
    page = request.GET.get('page') # get page get parameter to indicate curr page number
    try:
        posts = paginator.page(page) #obtain objects for desired page with page method
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
        #pass page number and retrieved objects to the template
    return render(request, 'blog/post/list.html', {'page': page,'posts': posts}) #render list of posts

#post detail - every post can be identified by date and slug
def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='published', publish__year=year, publish__month=month, publish__day=day)
    #if no object is found returns a 404 error
    return render(request, 'blog/post/detail.html', {'post': post})
