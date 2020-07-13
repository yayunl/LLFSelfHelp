from django.views.generic import (RedirectView, TemplateView)
from django.urls import path, include, reverse_lazy
from django.contrib.auth.views import (LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView,
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView)
from django.contrib.auth.views import AuthenticationForm

from .views import UserListView, UserDetailView,  UserCreateView, UserDeleteView, UserUpdateView, CreateAccount
from .views import ResendActivationEmail, ActivateAccount
# from django.contrib.auth.decorators import login_required
from .views import user_export,  user_import

user_urls = [
    # url patterns:
    path('users/', UserListView.as_view(), name='user_list'),
    path('create/', UserCreateView.as_view(), name='user_create'),
    path('<slug>/detail', UserDetailView.as_view(), name='user_detail'),
    path('<slug>/delete', UserDeleteView.as_view(), name='user_delete'),
    path('<slug>/update', UserUpdateView.as_view(), name='user_update'),
    path('export', user_export, name='user_export'),
    path('import', user_import, name='user_import'),

]

_password_urls = [
    # url patterns: auth/password/change/, auth/password/change/done, etc

    # change password
    path('change/', PasswordChangeView.as_view(template_name='users/password_change_form.html'),
         name='pw_change'),
    path('change/done/', PasswordChangeDoneView.as_view(template_name='users/password_change_done.html'),
         name='pw_change_done'),

    # reset password
    path('reset/', PasswordResetView.as_view(
        template_name='users/password_reset_form.html',
        email_template_name='users/password_reset_email.txt',
        subject_template_name='users/password_reset_subject.txt'
    ),  name='pw_reset_start'),

    path('reset/sent/', PasswordResetDoneView.as_view(template_name='users/password_reset_sent.html'),
         name='password_reset_done'),

    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
         name='pw_reset_confirm'),

    path('reset/done/',  PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html',
                                                           extra_context={'form': AuthenticationForm},),
         name='password_reset_complete'),
]

auth_urls = [

    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='users/logout.html'),name='logout'),
    # create user
    path('create/', CreateAccount.as_view(), name='create'),
    path('create/done/',
         TemplateView.as_view(template_name='users/user_create_done.html'),
         name='create_done'),
    # activation
    path('activate/<uidb64>/<token>/', ActivateAccount.as_view(), name='activate'),
    # path('activate', RedirectView.as_view(permanent=False)),
    path('activate/resend', ResendActivationEmail.as_view(), name='resend_activation'),

    # Incorporate password_urls to password/
    path('password/', include(_password_urls)),

]