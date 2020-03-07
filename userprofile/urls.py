from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='landing'),
    path('home', views.home_view, name='home'),
    path('welcome/', views.welcome_view, name='welcome'), 
    path('@<username>', views.profile_view, name='profile'),
    path('@<username>/following', views.following_view, name='following'),
    path('@<username>/followers', views.following_view, name='followers'),
    path('ajax/follow/<user>', views.follow, name='follow'),
    path('ajax/unfollow/<user>', views.unfollow, name='unfollow'),
    path('ajax/bookmark/<poem>', views.bookmark, name='bookmark'),
    path('ajax/unbookmark/<poem>', views.unbookmark, name='unbookmark'),
    path('ajax/like/<int:poem>', views.like, name='like'),
    path('ajax/unlike/<int:poem>', views.unlike, name='unlike'),
    path('ajax/upload_picture', views.upload_picture, name='upload_picture'),
    path('ajax/delete_picture', views.delete_picture, name='delete_picture'),
    path('settings/edit-profile', views.edit_profile, name='edit_profile'),
    path('about', views.about_view, name='about'),
    path('contact', views.contact_view, name='contact'),
]