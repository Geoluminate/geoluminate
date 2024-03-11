from django.contrib import admin

# from jazzmin import templatetags
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    pass


# @admin.register(Literature)
# class
