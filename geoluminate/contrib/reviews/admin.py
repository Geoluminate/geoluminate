from django.contrib import admin
from literature.models import Literature

# from jazzmin import templatetags
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    pass


# @admin.register(Literature)
# class
