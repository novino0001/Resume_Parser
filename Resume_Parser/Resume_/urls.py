from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
# from .views import graph_view

urlpatterns = [
    path('',  views.index_home , name ='index_home' ),
    path('home/',  views.home , name ='home' ),
    path('next/',  views.nextpage , name ='nextpage' ),
    path('user_data/',  views.user_data , name ='user_data' ),
    
    

    path('register/' , views.register , name='register'),
    path('login/' , views.login_page , name='login'),
    path('logout/' , views.logout_page , name='logout'),
    # path('candidate/',  views.candidate , name ='candidate' ),
   

    

    ]
