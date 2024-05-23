from django.urls import path
from . import views

urlpatterns = [
    path('',views.home_view, name='home'),
    path('register/',views.register_view, name='register'),
    path('login/',views.login_view, name='login'),
    path('logout/',views.logout_view, name='logout'),
    path('dashboard/',views.dashboard_view, name='dashboard'),
    path('bookticket/',views.bookticket_view, name='bookticket'),
    path('saveticket/',views.saveticket, name='saveticket'),
    path('ticketgenerate/',views.print_user_tickets, name='ticketgenerate'),
    path('cancelticket/',views.cancelticket_view, name='cancelticket'),
    path('search/', views.search_pnr, name='search_pnr'),
    path('searcha/', views.search_trains, name='search_trains'),
    path('booknow/<str:train_no>/', views.booknow, name='booknow'),
    path('about/', views.about_us_view, name='about_us'),
    path('contact/', views.contact_us_view, name='contact_us'),
]