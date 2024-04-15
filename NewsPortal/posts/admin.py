from django.contrib import admin
from .models import Post, Category, PostCategory


def nullfy_rating(modeladmin, request, queryset):
	# queryset - набор элементов выделенный галочками
	queryset.update(rating=0)


nullfy_rating.short_description = 'Обнулить рейтинг'


class PostAdmin(admin.ModelAdmin):
	list_display = ('title', 'author', 'post_type', 'date', 'category', 'rating')
	list_filter = ('author', 'post_type', 'rating', 'categories__category_name')
	search_fields = ('title', 'categories__category_name')
	actions = [nullfy_rating]

	def category(self, obj):
		return ", ".join([category.category_name for category in obj.categories.all()])


admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(PostCategory)
