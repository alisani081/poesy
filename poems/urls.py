from django.urls import path

from . import views

urlpatterns = [    
    path('<username>/poem/<slug:slug>', views.poem_view, name='poem'),
    path('topic/<topic>', views.poems_view, name='topic'),
    path('search', views.search_view, name='search'),
    path('new-poem', views.add_poem_view, name='add_poem'),
    path('topics', views.explore_view, name='topics'),
    path('new-poems', views.explore_view, name='new-poems'),
    path('edit/<slug>', views.edit_poem_view, name='edit_poem'),
    path('<username>/bookmarks', views.bookmarks_view, name='bookmarks'),
    path('top-poems', views.explore_view, name='explore'),
    path('search/', views.search_engine, name='search_engine'),
]