from django.conf.urls import url
from django.urls import path, re_path
from nova_poshta import views


urlpatterns = [
    url(r'^delivery/(?P<delivery_id>\d+)/$', views.get_delivery_by_id),
    re_path(r'^delivery/$', views.handle_delivery),
    re_path(r'^delivery/cities/$', views.get_city_list_by_name),
    re_path(r'^delivery/warehouses/$', views.get_warehouse_list_by_city_name),
]


