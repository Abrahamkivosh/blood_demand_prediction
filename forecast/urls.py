from django.urls import path, include
from . import views
from django.contrib.auth.decorators import login_required 

app_name = 'forecast'
urlpatterns = [
    # Other URL patterns for your app
    path('', views.IndexView.as_view() , name='index'),
    path('login/', views.LoginView.as_view() , name='login'),
    path('', include('forecast.password_url')),

    path('logout/', views.LogoutView.as_view() , name='logout'),

    path('dashboard/', login_required( views.DashboardView.as_view())  , name='dashboard'),
    path('blood-types/', login_required( views.BloodTypeView.as_view())  , name='blood-types-list'),
    path('blood-types/add', login_required(views.BloodTypeAddView.as_view() )  , name='blood-types-add'),
    path('blood-types/<int:bloodTypeId>/edit', login_required(views.BloodTypeUpdateView.as_view() )  , name='blood-types-edit'),
    path('blood-types/<int:bloodTypeId>/delete', login_required( views.BloodTypeDeleteView.as_view())  , name='blood-types-delete'),

    path('blood-predictions', login_required(views.bloodDemandPredictionIndex )  , name='blood-predictions-list'),
    path('blood-predictions/sync', login_required(views.bloodDemandPredictionStore )  , name='blood-predictions-sync'),

    path('users', login_required(views.usersIndex  ) , name='users-list'),
    path('users/add', login_required(views.usersCreate  ) , name='users-create'),
    path('users/store', login_required(views.usersStore )  , name='users-store'),
    path('users/<str:username>/edit', login_required( views.UserUpdateView.as_view()  ) , name='users-update'),

    path('blood-supplies/', login_required( views.BloodSupplyView.as_view())  , name='blood-supplies-list'),
    path('blood-supplies/add', login_required(views.BloodSupplyAddView.as_view() )  , name='blood-supplies-add'),
    path('blood-supplies/<int:bloodSupplyId>/edit', login_required(views.BloodSupplyUpdateView.as_view() )  , name='blood-supplies-edit'),
    path('blood-supplies/<int:bloodSupplyId>/delete', login_required( views.BloodSupplyDeleteView.as_view())  , name='blood-supplies-delete'),

    
]
