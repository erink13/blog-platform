from django.shortcuts import render, get_object_or_404
from .models import Post

#takes request as the only parameter
#this parameter is required by all views
def post_list(request):
    posts = Post.published.all() #all posts with published status
    return render(request, 'blog/post/list.html', {'posts': posts}) #render list of posts

#post detail - every post can be identified by date and slug
def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='published', publish__year=year, publish__month=month, publish__day=day)
    #if no object is found returns a 404 error
    return render(request, 'blog/post/detail.html', {'post': post})
