from django.urls import path
# Импортируем созданное нами представление
from .views import *


urlpatterns = [
   # path('', AuthorList.as_view()),
   path('', PostList.as_view(), name='post_list'),
   path('<int:pk>', PostDetail.as_view(), name='post_detail'),
   path('create/', PostCreate.as_view(), name='post_create'),
   path('<int:pk>/edit/', PostEdit.as_view(), name='post_edit'),
   path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
   path('search/', PostSearch.as_view(), name='post_search'),
   path('subscriptions/', subscriptions, name='subscriptions'),

   path('create/', ArticlesCreate.as_view(), name='articles_create'),
   path('<int:pk>/edit', ArticlesEdit.as_view(), name='articles_edit'),
   path('<int:pk>/delete/', ArticlesDelete.as_view(), name='articles_delete')
]