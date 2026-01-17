from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:year>/<int:month>/', views.index, name='index'),
    
    # events urls ==============================
    path('events_list/', views.events_list, name='events-list'),
    path('event_create/', views.event_create, name='event-create'),
    path('event_create/<int:venue_id>', views.event_create, name='event-create'),
    path('event_details/<int:event_id>', views.event_details, name='event-details'),
    path('event_update/<int:event_id>', views.event_update, name='event-update'),
    path('event_delete/<int:event_id>', views.event_delete, name='event-delete'), # type: ignore
    
    # favorite urls ==============================
    path('favorites_list/', views.favorites_list, name='favorites-list'),
    path('favorite_create/', views.favorite_create, name='favorite-create'),
    path('favorite_details/<int:favorite_id>', views.favorite_details, name='favorite-details'),
    path('favorite_update/<int:favorite_id>', views.favorite_update, name='favorite-update'),
    path('favorite_delete/<int:favorite_id>', views.favorite_delete, name='favorite-delete'), # type: ignore
    
    # venue urls ==============================
    path('venues_list/', views.venues_list, name='venues-list'),
    path('venue_create/', views.venue_create, name='venue-create'),  # type: ignore
    path('venue_details/<int:pk>/', views.venue_details, name='venue-details'),
    path('venue_update/<int:venue_id>/', views.venue_update, name='venue-update'),
    path('venue_delete/<int:venue_id>/', views.venue_delete, name='venue-delete'), # type: ignore
    
    path('venue_text/', views.venue_text, name='venue-text'),
    path('venue_csv/', views.venue_csv, name='venue-csv'),
    path('venue_pdf/', views.venue_pdf, name='venue-pdf'),
]
