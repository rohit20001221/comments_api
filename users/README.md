# user_auth_django
a simple module which handles user authentication

steps to use the module


# settings.py
INSTALLED_APPS = [<br />
  ...<br />
  'users',<br />
  ...
<br />]

HOME_PAGE_NAME = <name_for_home_page><br />
LOGIN_REDIRECT_URL = <name_for_home_page><br />


# urls.py of project
<br />
from django.urls import path, include<br />

urlpatterns = [<br />
  path('auth/', include('users.urls')),
<br />]
