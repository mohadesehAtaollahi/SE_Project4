app_name = "detector"

from django.urls import path
from .views import *

urlpatterns = [
    path("form1/", form1_view, name="form1"),
    path("result1/", result1_view, name="result1"),
    path("form2/", form2_view, name="form2"),

]