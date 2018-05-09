from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from taggit.managers import TaggableManager

class PublishedManager(models.Manager):
    #method that returns the queryset to be executed - used to include our custom list_filter
    #define it and add it to the post model
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')

class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    #field for the post title - varchar column in SQL database
    title = models.CharField(max_length=250)
    #use for urls - short label containing only letters, numbers, underscores, hyphens
    #fordate - build url for post using date - cant have same slug for same date
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    #many to one relationship - each post written by one user, one user can write many posts
    author = models.ForeignKey(User, related_name='blog_posts')
    #body of post - textfield which translates to text column in database
    body = models.TextField()
    #when post was published
    publish = models.DateTimeField(default=timezone.now)
    #when post was created - date will be saved automatically when creating an object
    created = models.DateTimeField(auto_now_add=True)
    #last time post was updated - updated when saving object automatically
    updated = models.DateTimeField(auto_now=True)
    #choices - can only be set to one of the given choices
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    objects = models.Manager() #default manager
    published = PublishedManager() #Dahl specific manager

    tags = TaggableManager()

    # contains metadata
    class Meta:
        #sort results by publish field by descending order (negative prefix)
        ordering = ('-publish',)

    #default human readable representation of object
    def __str__(self):
        return self.title

#canonical url for post object - add this method to the model to return the canonical url of the model
    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.publish.year, self.publish.strftime('%m'), self.publish.strftime('%d'), self.slug])

#comment model
class Comment(models.Model):
    #contains foreign key to associate comment w single post (post can have multiple comments)
    post = models.ForeignKey(Post, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.name, self.post)
