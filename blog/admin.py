from django.contrib import admin
from .models import Post

#tell the django admin site that our model is registered into the admin site using
#custom class that inherits from model admin
class PostAdmin(admin.ModelAdmin):
    #set fields of model we want to display
    list_display = ('title', 'slug', 'author', 'publish', 'status')
    list_filter = ('status', 'created', 'publish', 'author')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    #specify default order
    ordering = ['status', 'publish']

#registered this model with the admin site -appears on the admin page now
admin.site.register(Post, PostAdmin)
