from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='chess_app_home'),
    path('load_data', views.load_data, name='load_data'),
    path('create_group', views.create_group, name='create_group'),
    path('group_stats', views.group_stats, name='group_stats'),
    path('<int:game_id>/game_details/', views.game_details, name='game_id_details'),
    path('<int:group_id>/group_edit/', views.group_edit, name='group_id_edit'),
    path('<int:group_id>/group_edit/save', views.group_save, name='group_save'),
    path('<int:group_id>/group_edit/delete', views.group_delete, name='group_save'),
    path('news', views.chess_news, name='chess_news'),
]
