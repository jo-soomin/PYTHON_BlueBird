#서브앱 urls

from django.contrib import admin
from django.urls import path, include
from . import views



urlpatterns = [
    path('', views.index, name='index'),
    path('main', views.main, name='main'),
    path('test', views.test, name='test'),
    path('login', views.login, name='login'),
    path('loginRes', views.loginRes, name='loginRes'),
    path('logout', views.logout, name='logout'),
    path('boar', views.boar, name='boar'),
    path('board_detail/<int:board_id>', views.board_detail, name='board_detail'),
    path('signup', views.signup, name='signup'),
    path('signupRes', views.signupRes, name='signupRes'),
    path('pwConfirm/<int:board_id>', views.pwConfirm, name='pwConfirm'),
    path('pwConfirmRes/<int:board_id>', views.pwConfirmRes, name='pwConfirmRes'),

    path('create/', views.create, name='create'),
    path('createRes/', views.createRes, name='createRes'),
    path('update/<int:board_id>', views.update, name='update'),
    path('delete/<int:board_id>', views.delete, name='delete'),
    path('adminDelete/<int:board_id>', views.adminDelete, name='adminDelete'),

    path('adminBoard', views.adminBoard, name='adminBoard'),
    path('adminBoardBack', views.adminBoardBack, name='adminBoardBack'),
    path('AdmincreateRes/', views.AdmincreateRes, name='AdmincreateRes'),
    path('commentWrite/<int:boar_pk>',views.commentWrite, name='commentWrite'),
    path('commentDelete/<int:board_id>/<int:comment_id>', views.commentDelete, name='commentDelete'),

    ]
