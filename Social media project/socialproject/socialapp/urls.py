
from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'socialapp'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('welcome/', views.home_page.as_view(), name = 'welcome'),
    path('post/<int:pk>', views.Postdetail_page.as_view(), name="post-detail"),
    path('post/create/', views.Post_create.as_view(), name = 'create-post'),
    path('post/mypost/', views.My_post.as_view(), name = 'my-post'),
    path('post/update/<int:pk>', views.Postupdate_page.as_view(), name= 'post-update'),
    path('post/delete/<int:pk>', views.Postdelete_page.as_view(), name= 'post-delete'),
    path('accounts/', include('allauth.urls')),
    path('profile/<int:pk>', views.Profile_page.as_view(), name= 'profile'),
    path('profile/<int:pk>/followers/', views.Search_followers.as_view(), name = 'follower-list'),
    path('profile/edit/<int:pk>', views.Profileedit_page.as_view(), name ='profile-edit'),
    path('profile/<int:pk>/follower/add', views.Add_follower.as_view(), name = 'add-follower'),
    path('profile/<int:pk>/follower/remove', views.Remove_follower.as_view(), name = 'remove-follower'),
    path('post/<int:pk>/add/like/', views.Add_like.as_view(), name = 'add-like'),
    path('post/<int:pk>/add/dislike/', views.Add_dislike.as_view(), name = 'add-dislike'),
    path('search/user/', views.Search_user.as_view(), name = 'user-search'),
    path('post/comment/<int:pk>/like', views.Comment_like.as_view(), name = 'comment-like'),
    path('post/comment/<int:pk>/dislike', views.Comment_dislike.as_view(), name = 'comment-dislike'),
    
]
