from django.contrib import admin
from django.urls import path, include
from viz import views as viz_views
from django.contrib.auth.views import LoginView, LogoutView,PasswordResetDoneView

urlpatterns = [
    path('',viz_views.home,name='home'),
    path('login/', LoginView.as_view(template_name='viz/login.html'), name="login"),
    path('logout/',LogoutView.as_view(template_name='viz/logout.html'),name="logout"),
    path('admin', admin.site.urls),
    path('viz/', include('viz.urls')),
]
