from .views import index, MemberListView, GroupListView, ServiceListView
from .views import MemberDetailView, ServiceDetailView, GroupDetailView
from .views import MemberCreateView, ServiceCreateView, load_services
from .views import MemberDeleteView, ServiceDeleteView
from .views import MemberUpdateView, ServiceUpdateView
from .views import CreateAccount
from .views import ResendActivationEmail, ActivateAccount
from django.views.generic import (RedirectView, TemplateView)
from django.urls import path, include, reverse_lazy
from django.contrib.auth.views import (LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView,
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView)
from django.contrib.auth.views import AuthenticationForm
# from django.contrib.auth.decorators import login_required
from .views import test_email

urlpatterns = [
    path('', index, name='member_index'),
    path('email', test_email),
    path('members/', MemberListView.as_view(), name='member_list'),
    path('member/create/', MemberCreateView.as_view(), name='member_create'),
    path('member/<slug>/detail', MemberDetailView.as_view(), name='member_detail'),
    path('member/<slug>/delete', MemberDeleteView.as_view(), name='member_delete'),
    path('member/<slug>/update', MemberUpdateView.as_view(), name='member_update'),

    path('groups/', GroupListView.as_view(), name='group_list'),
    path('group/<slug>', GroupDetailView.as_view(), name='group_detail'),

    path('services', ServiceListView.as_view(), name='service_list'),
    path('service/create/', ServiceCreateView.as_view(), name='service_create'),
    path('service/<slug>/detail', ServiceDetailView.as_view(), name='service_detail'),
    path('service/<slug>/delete', ServiceDeleteView.as_view(), name='service_delete'),
    path('service/<slug>/update', ServiceUpdateView.as_view(), name='service_update'),
    path('ajax/load-services/', load_services, name='ajax_load_services'),

]

password_urls = [
    path('change/', PasswordChangeView.as_view(
        template_name='catalog/password_change_form.html'),
         name='pw_change'),
    path('change/done/', PasswordChangeDoneView.as_view(
        template_name='catalog/password_change_done.html'),
         name='pw_change_done'),

    # reset
    path('reset/', PasswordResetView.as_view(
        template_name='catalog/password_reset_form.html',
        email_template_name='catalog/password_reset_email.txt',
        subject_template_name='catalog/password_reset_subject.txt'
    ),  name='pw_reset_start'),

    path('reset/sent/', PasswordResetDoneView.as_view(
        template_name='catalog/password_reset_sent.html'
    ),  name='password_reset_done'),

    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
        template_name='catalog/password_reset_confirm.html'
    ), name='pw_reset_confirm'),

    path('reset/done/',  PasswordResetCompleteView.as_view(
        template_name='catalog/password_reset_complete.html',
        extra_context={'form': AuthenticationForm},
    ), name='password_reset_complete'),
]

user_urlpatterns = [
    path('login/', LoginView.as_view(template_name='catalog/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='catalog/logout.html'),name='logout'),
    # create user
    path('create/', CreateAccount.as_view(), name='create'),
    path('create/done/',
         TemplateView.as_view(template_name='catalog/user_create_done.html'),
         name='create_done'),
    path('activate/<uidb64>/<token>/', ActivateAccount.as_view(), name='activate'),
    # path('activate', RedirectView.as_view(permanent=False)),
    path('activate/resend', ResendActivationEmail.as_view(), name='resend_activation'),

    # password
    path('password/', include(password_urls)),

]