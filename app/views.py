from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from .forms import *
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, UpdateView, DeleteView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from .forms import UserUpdateForm
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.views import LoginView
from .forms import CustomUserCreationForm




class HomeView(ListView):
    model = Movie
    template_name = 'home.html'
    context_object_name = 'movies'

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            print(f"Search query: {query}") 
            queryset = queryset.filter(
                Q(title__icontains=query) | Q(description__icontains=query) | Q(actors__icontains=query)
            ).distinct()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['search_query'] = self.request.GET.get('q', '')
        return context

class CategoryView(ListView):
    model = Movie
    template_name = 'category.html'
    context_object_name = 'movies'

    def get_queryset(self):
        return Movie.objects.filter(category__id=self.kwargs['category_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['current_category'] = Category.objects.get(id=self.kwargs['category_id'])
        return context
    

class CustomLoginView(LoginView):
    template_name = 'login.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"Welcome back, {self.request.user.username}!")
        return response

class RegisterView(FormView):
    template_name = 'register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        # Send welcome email
        self.send_welcome_email(user)
        messages.success(self.request, f"Welcome, {user.username}! Your registration was successful.")
        return super().form_valid(form)

    # def send_welcome_email(self, user):
    #     subject = 'Welcome to Movie Website'
    #     message = f'Hi {user.username},\n\nThank you for registering at Movie Website!'
    #     from_email = settings.EMAIL_HOST_USER
    #     recipient_list = [user.email]
    #     send_mail(subject, message, from_email, recipient_list)

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('home')

class AddMovieView(LoginRequiredMixin, CreateView):
    model = Movie
    form_class = MovieForm
    template_name = 'addmovie.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.added_by = self.request.user
        return super().form_valid(form)

class ReviewMovieView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'review.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.movie_id = self.kwargs['pk']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('movie_detail', kwargs={'pk': self.kwargs['pk']})
    
class MovieDetailView(DetailView):
    model = Movie
    template_name = 'movie_detail.html'
    context_object_name = 'movie'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = Review.objects.filter(movie=self.object)
        return context


class ProfileView(DetailView):
    model = User
    template_name = 'profile.html'
    context_object_name = 'user'

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        context['movies'] = Movie.objects.filter(added_by=user)
        return context

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'profile_update.html'
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        return self.request.user
    

class MovieUpdateView(UpdateView):
    model = Movie
    form_class = MovieForm
    template_name = 'edit_movie.html'  # Create a template for editing movies
    success_url = reverse_lazy('profile')  # Redirect back to the profile page after editing

    def form_valid(self, form):
        form.instance.added_by = self.request.user
        return super().form_valid(form)

class MovieDeleteView(DeleteView):
    model = Movie
    template_name = 'delete_movie.html'  # Template for deleting movies
    success_url = reverse_lazy('profile')  # Redirect back to profile page after deleting

class AddFavoriteView(View):
    def post(self, request, pk):
        movie = Movie.objects.get(pk=pk)
        favorite, created = FavoriteMovie.objects.get_or_create(user=request.user, movie=movie)
        return redirect('movie_detail', pk=pk)