1) Copy the folder named frontend into your project:
   C:\Users\SAGHI\Documents\restaurant_order_system\frontend

2) Open restaurant_system/settings.py
   Find INSTALLED_APPS and add 'frontend', at the end:
   'accounts','restaurant','orders','payments','frontend',

3) Open restaurant_system/urls.py
   Add this import if not already present:
   from django.urls import path, include

   Add this line at the beginning of urlpatterns:
   path('', include('frontend.urls')),

   Or replace the full file with restaurant_system_urls.py from this patch.

4) Restart server:
   CTRL + BREAK in CMD, then:
   python manage.py runserver

5) Open customer UI:
   http://127.0.0.1:8000/
