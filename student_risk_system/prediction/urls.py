# urls.py

from django.urls import path   # to define URL routes
from .views import signup,login_view,predict,home,form,logout_view  # import our view

urlpatterns = [
    path('', home, name='home'),
    path('form/', predict, name='form'),  
    path("signup/", signup, name="signup"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    # when user opens page → call predict_view
]