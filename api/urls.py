from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from Zipin import settings
from . import views

urlpatterns = [
    path('', views.homepage),
    path('getroutes/', views.getRoutes),
    path('homepage/', views.homepage),
    path('users/', views.getUsers),
    path('notedetail/<int:pk>/', views.getDetail),
    path('notes/', views.getNotes),
    path('note/create/', views.create),
    path('note/update/<str:pk>/', views.update),
    path('signup/', views.createUser),
    path('checkmail/',views.checkmail),
    path('login/', views.login),
    path('logout/', views.logout),
    path('note/spci/<str:pk>/', views.getNote),
    path('delete/<int:pk>/',views.delete),
    path('<int:pk>/maincommon/', views.createMaincomn),
    path('<int:pk>/subcommon/', views.createSubcomn),

    path('getnote/<int:pk>/',views.getNote),
    path('getmaincomn/<int:pk>/',views.getMaincomn),
    path('getsubcomn/<int:pk>/',views.getSubcomn),
    path('collect/<int:pk>/',views.collect),
    path('identify',views.identify),
              ]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)