from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from . import views
app_name = "Accounts"


urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('password_change/', views.password_change, name='password_change'),
    path('password_change/done/', views.password_change_done, name='password_change_done'),

    path('password_reset/', views.password_reset, name='password_reset'),
    path('password_reset/sent/', views.password_reset_sent, name='password_reset_sent'),

    path("password_reset/<uidb64>/<token>/", 
        auth_views.PasswordResetConfirmView.as_view(
            template_name="Accounts/password_reset_confirm.html",
            success_url=reverse_lazy("Accounts:reset_complete")
        ),
        name="reset_confirm"
    ),
    path('reset/<uidb64>/<token>/', views.password_reset_confirm, name='reset_confirm'),
    path('reset/done/', views.password_reset_complete, name='reset_complete'),

    # path('profile/', views.profile, name='profile'),
    # path('profile/edit/', views.edit_profile, name='edit_profile'),
    # path('profile/change_password/', views.change_password, name='change_password'),
    # path('profile/delete/', views.delete_account, name='delete_account'),

    # path('verify_email/', views.verify_email, name='verify_email'),
    # path('verify_email/<str:token>/', views.verify_email_token, name='verify_email_token'),

    # path('resend_verification/', views.resend_verification, name='resend_verification')
]