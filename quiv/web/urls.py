from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'blog'

urlpatterns = [
    path('signup/', views.AddUserView.as_view(), name='add_user'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('like/post/', views.LikePost.as_view(), name='like_post'),
    path('contact-us/', views.ContactUsView.as_view(), name='contact_us'),
    path('search/', views.Search.as_view(), name="search"),
    path('comment/', views.CommentView.as_view(), name="comment_add"),
    path('detail/<slug>/', views.PostDetailView.as_view(), name='detail'),
    path('category/posts/<slug>/', views.CategoryPostView.as_view(), name='category_posts'),
    path('tag/posts/<slug>', views.TagPostView.as_view(), name='tag_posts'),
    path('', views.HomeView.as_view(), name='home'),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



