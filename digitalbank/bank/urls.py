# bank/urls.py
# bank/urls.py
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('deposit/',views.deposit_view, name='deposit'),
    path('withdraw/',views.withdraw_view, name='withdraw'),
    path('logout/', views.logout_user, name='logout'),
    path('transactions/', views.transaction_history, name='transactions'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('signup/', views.signup_view, name='signup'),
    # सिर्फ temporary fix के लिए
    path('accounts/profile/', views.dashboard, name='profile'),
    path('profile/', views.profile_view, name='profile'),
    # urls.py
    path('profile/update/', views.update_profile, name='update_profile'),



]
