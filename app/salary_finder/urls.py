"""salary_finder URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include
from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response


# Api Root View
class ApiRootViewSet(viewsets.ViewSet):
    def list(self, request):
        apidocs = {
                   'wage-estimation': request.build_absolute_uri('wage-estimation/'),
                   }
        return Response(apidocs)


admin.site.site_header = 'Salary Finder'
admin.site.site_title = "Salary Admin Portal"
admin.site.index_title = "Welcome to Salary Finder"


def redirect_view(request):
    # redirect to api page
    response = redirect('/api/')
    return response

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include("wage_estimation.urls")),
]
