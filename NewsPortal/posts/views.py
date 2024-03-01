from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (
	ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.contrib.auth.mixins import PermissionRequiredMixin
from .models import Post, Subscriber, Category
from .filters import PostsFIlter
from .forms import NewsForm, ArticleForm
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef


class PostsList(ListView):
	model = Post
	ordering = '-date'
	template_name = 'posts.html'
	context_object_name = 'posts'
	paginate_by = 10


class PostDetail(DetailView):
	model = Post
	template_name = 'post.html'
	context_object_name = 'post'


def posts_search(request):
	f = PostsFIlter(request.GET, queryset=Post.objects.all())
	return render(request, 'filter_posts.html', {'filter': f})


# ----- Представления для новостей -----

class NewsCreate(PermissionRequiredMixin, CreateView):
	permission_required = 'posts.add_post'
	form_class = NewsForm
	model = Post
	template_name = 'post_edit.html'

	def form_valid(self, form):
		news = form.save(commit=False)
		news.post_type = Post.news
		return super().form_valid(form)


class NewsUpdate(PermissionRequiredMixin, UpdateView):
	permission_required = 'posts.change_post'
	form_class = NewsForm
	model = Post
	template_name = 'post_edit.html'


class NewsDelete(PermissionRequiredMixin, DeleteView):
	permission_required = 'posts.delete_post'
	model = Post
	template_name = 'post_delete.html'
	success_url = reverse_lazy('posts_list')


# ----- Представления для статей -----

class ArticleCreate(PermissionRequiredMixin, CreateView):
	permission_required = 'posts.add_post'
	form_class = ArticleForm
	model = Post
	template_name = 'post_edit.html'

	def form_valid(self, form):
		article = form.save(commit=False)
		article.post_type = Post.article
		return super().form_valid(form)


class ArticleUpdate(PermissionRequiredMixin, UpdateView):
	permission_required = 'posts.change_post'
	form_class = ArticleForm
	model = Post
	template_name = 'post_edit.html'


class ArticleDelete(PermissionRequiredMixin, DeleteView):
	permission_required = 'posts.delete_post'
	model = Post
	template_name = 'post_delete.html'
	success_url = reverse_lazy('posts_list')


@login_required
@csrf_protect
def subscriptions(request):
	if request.method == 'POST':
		category_id = request.POST.get('category_id')
		category = Category.objects.get(id=category_id)
		action = request.POST.get('action')

		if action == 'subscribe':
			Subscriber.objects.create(user=request.user, category=category)
		elif action == 'unsubscribe':
			Subscriber.objects.filter(
				user=request.user,
				category=category,
			).delete()

	categories_with_subscriptions = Category.objects.annotate(
		user_subscribed=Exists(
			Subscriber.objects.filter(
				user=request.user,
				category=OuterRef('pk')
			)
		)
	).order_by('category_name')

	return render(
		request,
		'subscriptions.html',
		{'categories': categories_with_subscriptions}
	)
