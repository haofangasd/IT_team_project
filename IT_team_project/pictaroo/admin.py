from django.contrib import admin
from pictaroo.models import Category, Image
from pictaroo.models import UserProfile


class ImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url')

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}


# Register your models here.
admin.site.register(Category, CategoryAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(UserProfile)