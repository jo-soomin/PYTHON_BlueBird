from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('board.urls')),
    path('main', include('board.urls')),
    path('test', include('board.urls')),
    path('login', include('board.urls')),
    path('loginRes', include('board.urls')),
    path('logout', include('board.urls')),
    path('signup', include('board.urls')),
    path('signupRes', include('board.urls')),
    path('boar', include('board.urls')),
    path('board_detail/<int:board_id>', include('board.urls')),
    path('create/', include('board.urls')),
    path('createRes/', include('board.urls')),
    path('update/<int:board_id>', include('board.urls')),
    path('delete/<int:board_id>', include('board.urls')),
    path('pwConfirm/<int:board_id>', include('board.urls')),
    path('pwConfirmRes/<int:board_id>', include('board.urls')),
    path('adminBoard', include('board.urls')),
    path('adminBoardBack', include('board.urls')),
    path('AdmincreateRes/', include('board.urls')),
    path('commentWrite/<int:boar_pk>', include('board.urls')),
    path('commentDelete/<int:board_id>/<int:comment_id>', include('board.urls')),
    path('adminDelete/<int:board_id>', include('board.urls')),

]



