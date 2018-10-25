from django.contrib.auth.models import User
from rest_framework import serializers
from .models import *
from django.conf import settings
from collections import namedtuple

class AddRoleSerializer(serializers.ModelSerializer):
	class Meta:
		model = RoleTypes
		fields = '__all__'

class AddDepartmentSerializer(serializers.ModelSerializer):
	class Meta:
		model = Department
		fields = '__all__'

class RoleSerializer(serializers.ModelSerializer):
	class Meta:
		model = Role
		exclude = ('user',)

class UserSerializer(serializers.ModelSerializer):
	user_role = RoleSerializer()

	class Meta:
		model = User
		fields = ('id', 'username', 'first_name', 'email', 'user_role')

##############----------------Permission Serializers---------------########################
class PermissionSerializer(serializers.ModelSerializer):
	class Meta:
		model = Permission
		fields = '__all__'

class PermissionRoleReadSerializer(serializers.ModelSerializer):
	permission = PermissionSerializer(many=True)

	class Meta:
		model = RolePermission
		fields = '__all__'

class RolePermissionSerializer(serializers.ModelSerializer):
	role_permission = PermissionRoleReadSerializer()

	class Meta:
		model = RoleTypes
		fields = ['id', 'role_type', 'role_permission']

