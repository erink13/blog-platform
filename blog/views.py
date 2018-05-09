from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.core.mail import send_mail
from .models import Post, Comment
from .forms import EmailPostForm, CommentForm
from django.db.models import Count
from taggit.models import Tag


#takes request as the only parameter
#this parameter is required by all views
def post_list(request, tag_slug=None):
    object_list = Post.published.all() #all posts with published status

    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

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
    return render(request, 'blog/post/list.html', {'page': page,'posts': posts,'tag': tag}) #render list of posts

class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'

#post detail - every post can be identified by date and slug - display post and comments
def post_detail(request, year, month, day, post):
    #get post by ID and makes sure it is published
    post = get_object_or_404(Post, slug=post, status='published', publish__year=year, publish__month=month, publish__day=day)
    #if no object is found returns a 404 error

    # Query set to return all active comments for this post
    comments = post.comments.filter(active=True)
    if request.method == 'POST':
        # A comment was posted (instantiate form using submitted data)
        comment_form = CommentForm(data=request.POST)
        #validate the data
        if comment_form.is_valid():
            # Create Comment object with save method - creates instance of model the form is linked to! but don't save to database yet because commit=False
            #we want to modify the object before saving it!
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment (the modification before saving it to the database)
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        # A comment was posted (build a form instance) - GET REQUEST
        comment_form = CommentForm()

    # List of similar posts
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]

    return render(request, 'blog/post/detail.html', {'post': post,
                                                     'comments': comments,
                                                     'comment_form': comment_form})

def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False

    #form was submitted and needs to be processed (why we use POST not get)
    #get - get request - we should display an empty form
    if request.method == 'POST':
        # Form was submitted
        #1. when view is loaded with get request, create new form instance used to display empty form
        form = EmailPostForm(request.POST)
        #2. user fills and submits by post - create form instance using submitted data

        #3. validate form using this method - true if all fields contain valid data
        if form.is_valid():
            #5. Form fields passed validation - retrieve data with the cleaned_data method
            #cleaned-data only returns valid fields!
            cd = form.cleaned_data
            #build complete URL including HTTP schema and hostname
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{} ({}) recommends you reading "{}"'.format(cd['name'], cd['email'], post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title, post_url, cd['name'], cd['comments'])
            send_mail(subject, message, 'admin@myblog.com', [cd['to']])
            sent = True
    else:
        #4. if not valid, render the form in the template again with validation errors
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post,
                                                    'form': form,
                                                    'sent': sent})
