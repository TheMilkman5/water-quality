from django.conf.urls import url

from . import views

app_name = 'dashboard'

urlpatterns = [
	url(r'^home/$', views.home, name='home_page'),
	url(r'^history/$', views.HistoryListView.as_view(), name='history_page-list'),
	url(r'^systemtest/$', views.systemtest, name='systemtest_page'),
	url(r'^ajax/get_sensordata/$', views.get_sensordata, name='get_sensordata'),
	url(r'^ajax/close_flow/$', views.close_flow_water, name='close_flow'),
	url(r'^ajax/open_flow/$', views.open_flow_water, name='open_flow'),
	url(r'^ajax/testemail/$', views.send_testemail, name='test_email'),
]