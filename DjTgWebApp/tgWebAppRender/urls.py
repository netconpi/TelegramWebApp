
from django.urls import path, include
from . import views

urlpatterns = [
    # path('register/', views.RegisterUser.as_view(), name='register'),
    # Admin part
    # Unregistred flow
    path('add_company/', views.AddCompany.as_view(), name='add-company'),
    path('404/', views.NotFound.as_view(), name='not_found'),
    # Only registred user flow
    # LK
    path('lk-subscribed/', views.LkSubscribed.as_view(), name='lk-subscribed'),
    path('lk/', views.Lk.as_view(), name='lk'),
    path('client-profile/', views.ClientProfile.as_view(), name='client-profile'),
    # Events pages
    path('calendar-task-list/', views.CalendarTaskList.as_view(), name='calendar-task-list'),
    path('client-free-times/', views.ClientFreeTimes.as_view(), name='client-free-times'),
    # Subscribe
    path('card-add/', views.CardAdd.as_view(), name='card-add'),
    path('card-choose/', views.CardChoose.as_view(), name='card-choose'),
    path('subscribe-choose/', views.SubscribeChoose.as_view(), name='subscribe-choose'),
    # Notifications
    path('notifications/', views.Notifications.as_view(), name='notifications'),

    # Unused
    path('components/', views.Components.as_view(), name='components'),
    path('index/', views.index.as_view(), name='index'),
    path('login-home/', views.LoginHome.as_view(), name='login-home'),
    path('login-in/', views.LoginIn.as_view(), name='login-in'),
]