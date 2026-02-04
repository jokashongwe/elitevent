from django.urls import path
from . import views
from invitation.views import view_invitation

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('dashboard/', views.dashboard_home, name='dashboard_home'),
    path('dashboard/event/new/', views.create_event, name='create_event'),
    path('dashboard/event/<int:event_id>/', views.manage_event, name='manage_event'),
    path('dashboard/event/<int:event_id>/settings/', views.event_settings, name='event_settings'),
    path('invitation/<uuid:uuid>/', view_invitation, name='view_invitation'),
    path('checkin/<uuid:uuid>/', views.checkin_guest, name='checkin_guest'),
]