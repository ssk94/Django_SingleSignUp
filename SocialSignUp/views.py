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


from .permissions import *

# Create your views here.

@api_view(['POST'])
@permission_classes((AllowAny,))
def login(request):
	user = authenticate(username=request.data['username'], password=request.data['password'])
	if user:
		serializer = UserSerializer(user)
		current_time = timezone.now()
		token = Token.objects.get(user=user)
		return JsonResponse({"user":serializer.data,
							 "token": token.key,
							 "login_time": strftime("%H:%M:%S", time.localtime())
							}, status=200)
	else:
		return JsonResponse({"message": "invalid credentials"}, status=401)

@api_view(['GET'])
def logout(request):
	user = request.user
	if user:
		return JsonResponse({'message': 'User logged out successfully'})
	else:
		return JsonResponse({'message': 'Unauthorized User'})

@api_view(['POST'])
@permission_classes((AllowAny,))
def register(request):
	username = request.data.get('username', None)
	password = request.data.get('password', None)
	role = request.data.get('role', None)
	department = request.data.get('department', None)
	contact = request.data.get('contact', None)
	email = request.data.get('email', None)
	address = request.data.get('address', None)
	first_name = request.data.get('first_name', None)
	last_name = request.data.get('last_name', None)
	user = authenticate(username=username, password=password)
	if user is None:
		password = password
		user_save = User(
			username = username,
			first_name = first_name,
			last_name = last_name
			)
		user_save.set_password(password)
		user_save.save()
		user_role = Role(
			user = user_save,
			role_type = role,
			department = department
			)
		user_role.save()
		if role in ['SuperAdmin', 'Admin', 'Manager']:
			try:
				employee = Employees(
					user = user_save,
					email = email,
					address = address,
					contact = contact,
					approved = True
					)
				employee.save()
			except(Exception) as e:
				pass
		else:
			try:
				employee = Employees(
					user = user_save,
					email = email,
					address = address,
					contact = contact
					)
				employee.save()
			except(Exception) as e:
				pass
		return JsonResponse({'message': 'User registered successfully'}, status=201)
	return JsonResponse({'message': 'Username already Exists'})

###################------------Forgot Password-----------------################
@api_view(['POST'])
@permission_classes((AllowAny,))
def forgot_password(request):
	user = User.objects.filter(username=request.data['username']).first()
	if user:
		send_mail('subject', 'body of the message', 'saroj.therockingdude@gmail.com', ['kulkarnisaroj5@gmail.com'])
		return JsonResponse({'message':'User Exists'}, status=200)
	return JsonResponse({'message':'User Does Not Exist'}, status=400)


##########----------Add Roles----------------###################
class AddRoleView(APIView):
	permission_classes = (AllowAny,)
	def post(self, request):
		if not check_permission(request, ['add_role']):
			return JsonResponse({'messsage':'You are not allowed to do this operation', 'status':False}, status=401)
		if request.data:
			serializer = AddRoleSerializer(data=request.data)
			if serializer.is_valid():
				serializer.save()
				return JsonResponse({'message':'Role Added Successfully'}, status=200)
			return Response(serializer.errors)
		return JsonResponse({'message':'Bad Request'}, status=400)

	def get(self, request):
		if not check_permission(request, ['add_role', 'edit_role', 'view_role']):
			return JsonResponse({'messsage':'You are not allowed to do this operation', 'status':False}, status=401)
		roles = RoleTypes.objects.all()
		serializer = AddRoleSerializer(roles, many=True)
		return Response(serializer.data)

class AddDepartmentView(APIView):
	permission_classes = (AllowAny,)
	def post(self, request):
		if not check_permission(request, ['add_department', 'edit_department', 'delete_department']):
			return JsonResponse({'messsage':'You are not allowed to do this operation', 'status':False}, status=401)
		if request.data:
			serializer = AddDepartmentSerializer(data=request.data)
			if serializer.is_valid():
				serializer.save()
				return JsonResponse({'message':'Department Added Successfully'}, status=200)
			return Response(serializer.errors)
		return JsonResponse({'message':'Bad Request'}, status=400)

	def get(self, request):
		if not check_permission(request, ['add_department', 'edit_department', 'delete_department', 'view_department']):
			return JsonResponse({'messsage':'You are not allowed to do this operation', 'status':False}, status=401)
		department = Department.objects.all()
		serializer = AddDepartmentSerializer(department, many=True)
		return Response(serializer.data)




