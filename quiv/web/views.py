from django.contrib.auth import authenticate, login, logout
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView
from django.views.generic.base import View, TemplateView
from web.models import Post, Category, Tag, Comment
from web.forms import UserForm, CommentForm, ContactUsForm
from django.contrib import messages
from user.models import User

class HomeView(ListView):
    queryset = Post.objects.all()
    template_name = 'index.html'
    paginate_by = 10


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        user = authenticate(email=request.POST.get('email'), password=request.POST.get('password'))
        if user is not None:
            login(request, user)
            return redirect('blog:home')
        messages.error(request, "The Email and Password didn't match")
        return redirect('blog:home')


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse('blog:home'))


class AddUserView(CreateView):
    form_class = UserForm
    model = User
    template_name = 'signup.html'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
        else:
            messages.error(request, 'Email is already exists')
            return redirect(reverse('blog:home'))
        return redirect(reverse('blog:home'))


class LikePost(View):
    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, id=self.request.POST.get('post_id'))
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
        return HttpResponseRedirect(post.get_absolute_url())


class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['User'] = User.objects.all()
        context['comment'] = Comment.objects.all()
        return context


class CommentView(CreateView):
    form_class = CommentForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.save()
        return redirect(reverse('blog:home'))


class ContactUsView(CreateView):
    template_name = 'contact.html'
    form_class = ContactUsForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.save()
        else:
            return render(request, 'contact.html', {'form': form})
        return redirect(reverse('blog:contact_us'))


class Search(FormView):
    def get(self, request, *args, **kwargs):
        queryset = Post.objects.all()
        query = request.GET.get("search")
        if query:
            queryset = queryset.filter(title__contains=query)|queryset.filter(tag__name__contains=query)|queryset.filter(category__name__contains=query)
        context = {
            'object_list': queryset,
        }
        return render(request, 'index.html', context)


class CategoryPostView(ListView):
    model = Post
    template_name = 'category.html'
    # paginate_by = 1

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = Post.objects.filter(category__name=self.kwargs['slug'])
        return context


class TagPostView(ListView):
    model = Post
    template_name = 'tag.html'
    # paginate_by = 1

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = Post.objects.filter(tag__name=self.kwargs['slug'])
        return context