"""
URL configuration for movies project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from app.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
     path('', HomeView.as_view(), name='home'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('add_movie/', AddMovieView.as_view(), name='add_movie'),
    path('movie/<int:pk>/', MovieDetailView.as_view(), name='movie_detail'),
    path('movie/<int:pk>/review/', ReviewMovieView.as_view(), name='review_movie'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/update/', ProfileUpdateView.as_view(), name='profile_update'),
    path('category/<int:category_id>/', CategoryView.as_view(), name='category'),
     path('movie/edit/<int:pk>/', MovieUpdateView.as_view(), name='edit_movie'),
    path('delete_movie/<int:pk>/', MovieDeleteView.as_view(), name='delete_movie'),
     path('movie/<int:pk>/favorite/', AddFavoriteView.as_view(), name='add_favorite'),
      path('logout/', logout_view, name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
