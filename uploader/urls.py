from django.urls import path

from .views import home, AddOriginal, image_form

urlpatterns = [

    path('', home, name='home'),
    path('post/', AddOriginal.as_view(), name='add_post'),
    path('image/', image_form, name='image_form'),
]
