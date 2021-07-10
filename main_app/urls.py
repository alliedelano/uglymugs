from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('mugs/', views.mugs_index, name='index'),
    path('mugs/<int:mug_id>/', views.mugs_detail, name='detail'),
    path('mugs/create/', views.MugCreate.as_view(), name='mugs_create'),
    path('mugs/<int:pk>/update/', views.MugUpdate.as_view(), name='mugs_update'),
    path('mugs/<int:pk>/delete/', views.MugDelete.as_view(), name='mugs_delete'),
    path('mugs/<int:mug_id>/add_use/', views.add_use, name='add_use'),
    path('mugs/<int:mug_id>/add_photo', views.add_photo, name='add_photo'),
    path('mugs/<int:mug_id>/assoc_inst/<int:instruction_id>/', views.assoc_inst, name='assoc_inst'),
    path('mugs/<int:mug_id>/unassoc_inst/<int:instruction_id>/', views.unassoc_inst, name='unassoc_inst'),
    path('instructions/', views.InstructionList.as_view(), name='instructions_index'),
    path('instructions/<int:pk>/', views.InstructionDetail.as_view(), name='instructions_detail'),
    path('instructions/create/', views.InstructionCreate.as_view(), name='instructions_create'),
    path('instructions/<int:pk>/update/', views.InstructionUpdate.as_view(), name='instructions_update'),
    path('instructions/<int:pk>/delete/', views.InstructionDelete.as_view(), name='instructions_delete'),
    path('accounts/signup/', views.signup, name='signup'),
]