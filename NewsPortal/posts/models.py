from django.contrib.auth.models import User
from django.core.cache import cache
from django.db import models
from django.db.models import Sum
from django.urls import reverse


class Author(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	rating = models.IntegerField(default=0)

	def update_rating(self):
		posts_rating = Post.objects.filter(author=self.id).aggregate(rating=Sum('rating'))
		comments_rating = Comment.objects.filter(user_id=self.user.id).aggregate(rating=Sum('rating'))
		author_posts_comments_rating = Comment.objects.filter(post_id__author=self.id).aggregate(rating=Sum('rating'))

		self.rating = (posts_rating['rating'] * 3) + comments_rating['rating'] + author_posts_comments_rating['rating']
		self.save()


class Category(models.Model):
	category_name = models.CharField(max_length=255, unique=True)
	subscribers = models.ManyToManyField(User, through='Subscriber')

	def __str__(self):
		return self.category_name.title()


class Post(models.Model):
	news = 'News'
	article = 'Article'
	POST_TYPES = [(news, 'Новость'),
				  (article, 'Статья')]

	author = models.ForeignKey(Author, on_delete=models.CASCADE)
	post_type = models.CharField(max_length=255, choices=POST_TYPES)
	date = models.DateTimeField(auto_now_add=True)
	categories = models.ManyToManyField(Category, through='PostCategory')
	title = models.CharField(max_length=255)
	text = models.TextField()
	rating = models.IntegerField(default=0)

	def like(self):
		self.rating += 1
		self.save()

	def dislike(self):
		if self.rating > 0:
			self.rating -= 1
			self.save()

	def preview(self):
		return f'{self.text[:124]}...'

	def __str__(self):
		return f'{self.title.title()}: {self.text}'

	def get_absolute_url(self):
		return reverse('posts_detail', args=[str(self.id)])

	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)
		cache.delete(f'product-{self.pk}')


class PostCategory(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	text = models.TextField()
	date = models.DateTimeField(auto_now_add=True)
	rating = models.IntegerField(default=0)

	def like(self):
		self.rating += 1
		self.save()

	def dislike(self):
		if self.rating > 0:
			self.rating -= 1
			self.save()


class Subscriber(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
	category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subscriptions')