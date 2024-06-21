from django.urls import path     
from . import views
urlpatterns = [
    path('', views.loginPage,name='loginPage'),	
    path('log', views.login,name='login'),	 	   
    path('register', views.register,name='register'),   
    path('dashboard', views.dashboard,name='dashboard'),
    path('trip/new', views.new,name='new'),  
    path('trip/newTrip', views.newTrip,name='newTrip'), 
    path('trip/edit/<int:Tid>', views.edit,name='edit'),  
    path('trip/editTrip/<int:Tid>', views.editTrip,name='editTrip'),  
    path('trip/deleteTrip/<int:Tid>', views.deleteTrip,name='deleteTrip'), 
    path('trip/details/<int:Tid>', views.details,name='details'), 
    path('trip/myTrips', views.myTrips,name='myTrips'), 
    path('trip/joinTrip/<int:Tid>', views.joinTrip,name='joinTrip'), 
    path('trip/cancelTrip/<int:Tid>', views.cancelTrip,name='cancelTrip'),
]