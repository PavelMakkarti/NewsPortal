from django.urls import path
from .views import *
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('', PostList.as_view()),
    # path('<int:pk>', cache_page(60*10)(PostDeteil.as_view(), name='post_details'),
    path('create/', PostCreate.as_view(), name='post_create'),
    path('<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),

    path('create/', ArticlesCreate.as_view(), name='articles_create'),
    path('<int:pk>/edit', ArticlesEdit.as_view(), name='articles_edit'),
    path('<int:pk>/delete/', ArticlesDelete.as_view(), name='articles_delete'),

    path('subscriptions/', subscriptions, name='subscriptions'),

]