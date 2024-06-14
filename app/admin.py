from django.contrib import admin
from .models import Movie, Review, Category

admin.site.register(Movie)
admin.site.register(Review)
admin.site.register(Category)
