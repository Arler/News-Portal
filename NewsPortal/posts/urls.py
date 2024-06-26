from django.urls import path
from django.views.decorators.cache import cache_page
from .views import (
	PostsList, PostDetail, posts_search, NewsCreate, NewsUpdate, NewsDelete,
	ArticleCreate, ArticleUpdate, ArticleDelete
)

urlpatterns = [
	path('', cache_page(0)(PostsList.as_view()), name='posts_list'),
	path('<int:pk>', cache_page(0)(PostDetail.as_view()), name='posts_detail'),
	path('search/', posts_search, name='posts_search'),
	path('news/create/', NewsCreate.as_view(), name='news_create'),
	path('news/<int:pk>/edit', NewsUpdate.as_view(), name='news_update'),
	path('news/<int:pk>/delete', NewsDelete.as_view(), name='news_delete'),
	path('articles/create', ArticleCreate.as_view(), name='articles_create'),
	path('articles/<int:pk>/edit', ArticleUpdate.as_view(), name='articles_update'),
    path('articles/<int:pk>/delete', ArticleDelete.as_view(), name='articles_delete'),
]
