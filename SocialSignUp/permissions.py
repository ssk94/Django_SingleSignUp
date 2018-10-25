from django.shortcuts import render
from .models import *
from .serializers import *

from django.http import JsonResponse
from django.contrib.auth import authenticate
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.core.mail import EmailMultiAlternatives

from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from annoying.functions import get_object_or_None
from datetime import date

from collections import namedtuple
import time
from datetime import datetime
from time import gmtime, strftime
from django.core.mail import send_mail

from django.http import HttpResponse
from django.template.loader import get_template

def check_permission(request, permission_to_be=[]):
	print(request)
	# if request.user.user_role.role_type=='Admin' and request.user.user_role.role_type=='SuperAdmin':
	# 	return True
	# role = RoleTypes.objects.filter(role_type=request.user.user_role.role_type).first()
	# allowed_permission = [i.permission for i in role.role_permission.permission.all()]
	# for i in permission_to_be:
	# 	if i in allowed_permission:
	# 		return True
	# 	else:
	# 		return False
	return True

class PermissionView(APIView):
	def post(self, request):
		if not check_permission(request, ['add_permission', 'delete_permission', 'edit_permission']):
			return JsonResponse({'messsage':'You are not allowed to do this operation', 'status':False}, status=401)
		if request.data:
			permission_serialize = PermissionSerializer(data=request.data)
			if permission_serialize.is_valid():
				permission_serialize.save()
				return JsonResponse({'messsage':'Permission Saved Successfully', 'status':True}, status=201)
			return JsonResponse({'messsage':'Something went wrong, Please try again', 'status':False, 'error':permission_serialize.errors}, status=400)
		return JsonResponse({'messsage':'Bad request', 'status':False}, status=400)

	def get(self, request):
		if not check_permission(request, ['view_permission', 'add_permission', 'delete_permission', 'edit_permission']):
			return JsonResponse({'messsage':'You are not allowed to do this operation', 'status':False}, status=401)
		permissions = Permission.objects.all()
		permission_serialize = PermissionSerializer(permissions, many=True)
		return Response(permission_serialize.data)

	def put(self, request):
		if not check_permission(request, ['add_permission', 'delete_permission', 'edit_permission']):
			return JsonResponse({'messsage':'You are not allowed to do this operation', 'status':False}, status=401)
		if request.data:
			id = request.data.get('id', None)
			if id:
				permission = Permission.objects.filter(id=id).first()
				if permission:
					permission_serialize = PermissionSerializer(permission, data=request.data)
					if permission_serialize.is_valid():
						permission_serialize.save()
						return JsonResponse({'messsage':'Permission Updated Successfully', 'status':True}, status=204)
					return JsonResponse({'messsage':'Invalid Data', 'status':False}, status=400)
				return JsonResponse({'messsage':'Invalid Permission', 'status':False}, status=400)
			return JsonResponse({'messsage':'Please Send Unique Id', 'status':False}, status=400)
		return JsonResponse({'messsage':'Bad Request', 'status':False}, status=400)

	def delete(self, request):
		if not check_permission(request, ['add_permission', 'delete_permission', 'edit_permission']):
			return JsonResponse({'messsage':'You are not allowed to do this operation', 'status':False}, status=401)
		if request.data:
			id = request.data.get('id', None)
			if id:
				permission = Permission.objects.filter(id=id).delete()
				return JsonResponse({'messsage':'Permission Deleted Succesfully', 'status':True}, status=400)
			return JsonResponse({'messsage':'Please Send Unique Id', 'status':False})
		return JsonResponse({'messsage':'Bad Request', 'status':False}, status=400)

class RolePermissionView(APIView):
	def post(self, request):
		if not check_permission(request, ['add_permission', 'delete_permission', 'edit_permission']):
			return JsonResponse({'messsage':'You are not allowed to do this operation', 'status':False}, status=401)
		if request.data:
			role_id = request.data.get('role_type', None)
			permission_id = request.data.get('permission', None)
			if role_id:
				role = RoleTypes.objects.filter(id=role_id).first()
				if role:
					role_permission_obj = RolePermission.objects.filter(role=role_id).first()
					permission_instance = Permission.objects.filter(id=permission_id).first()
					if role_permission_obj and permission_instance:
						role_permission_obj.permission.add(permission_instance)
						role_permission_obj.save()
						return JsonResponse({'messsage':'Permission Added to the Role', 'status':True}, status=200)
					elif permission_instance:
						role_permission_obj = RolePermission(role=role)
						role_permission_obj.save()
						role_permission_obj.permission.add(permission_instance)
						return JsonResponse({'messsage':'Permission added to the role', 'status':True}, status=200)
				return JsonResponse({'messsage':'Invalid Role', 'status':False}, status=404)
			return JsonResponse({'messsage':'Please provide valid Role Id', 'status':False}, status=404)
		return JsonResponse({'messsage':'Bad Request', 'status':False}, status=400)

	def delete(self, request):
		if not check_permission(request, ['add_permission', 'delete_permission', 'edit_permission']):
			return JsonResponse({'messsage':'You are not allowed to do this operation', 'status':False}, status=401)
		if request.data:
			role_id = request.data.get('role_type', None)
			permission_id = request.data.get('permission', None)
			if role_id:
				role=RolePermission.objects.filter(role=role_id).first()
				permission_instance = Permission.objects.filter(id=permission_id).first()
				if role:
					role.permission.remove(permission_instance)
					role.save()
					return JsonResponse({'messsage':'Permission has been removed from the role', 'status':True}, status=200)
				return JsonResponse({'messsage':'Invalid Role', 'status':False}, status=404)
			return JsonResponse({'messsage':'Please provide Valid Role Id', 'status':False}, status=404)
		return JsonResponse({'messsage':'Bad Request', 'status':False}, status=400)

	def get(self, request):
		if not check_permission(request, ['view_permission', 'add_permission', 'delete_permission', 'edit_permission']):
			 return JsonResponse({'messsage':'You are not allowed to do this operation', 'status':False}, status=401)
		role = RoleTypes.objects.all()
		print("rolling")
		serializer = RolePermissionSerializer(role, many=True)
		return Response(serializer.data)


@api_view(['POST'])
def checkingPerm(request):
	if not check_permission(request, ['can_create', 'can_update']):
		return JsonResponse({'messsage':'You are not allowed to do this operation', 'status':False}, status=401)
	print("Authorized")
	return JsonResponse({'messsage':'success', 'status':True}, status=200)


