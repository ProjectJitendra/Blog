from django.contrib import admin
from web.models import Category, Tag, Post, Comment, ContactUs
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Comment)
admin.site.register(ContactUs)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',), }
    list_display = ['title', 'slug']


