from django.conf.urls import url 
from . import views
from . import permissions

urlpatterns=[
	url(r'^register/', views.register, name='register'),
	url(r'userLogin', views.login, name='userlogin'),
	url(r'^logout/', views.logout, name='logout'),

	url(r'^forgot_password$', views.forgot_password, name='forgot_password'),

	url (r'^role$', views.AddRoleView.as_view(), name='role'),
	url(r'^department', views.AddDepartmentView.as_view(), name='department'),


	#############################Permission Urls##########################

	url(r'^permission$', permissions.PermissionView.as_view(), name='permission_view'),
	
	url(r'^role/permissions$', permissions.RolePermissionView.as_view(), name='role_permission'),

	url(r'^check_permission$', permissions.checkingPerm, name='check_permission'),
]