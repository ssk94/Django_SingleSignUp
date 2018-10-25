import uuid

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings
import datetime
from django.db.models import Sum

# Create your models here.
@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
	if created:
		Token.objects.create(user=instance)

class RoleTypes(models.Model):
	role_type = models.CharField(max_length=20)

class Role(models.Model):
	user = models.OneToOneField(User, related_name='user_role', on_delete=models.CASCADE)
	role_type = models.CharField(max_length=20, null=True)
	department = models.CharField(max_length=50, null=True)

class Permission(models.Model):
	permission = models.CharField(max_length=200, unique=True)

	def __str__(self):
		return self.permission

class RolePermission(models.Model):
	role = models.OneToOneField(RoleTypes, related_name='role_permission', on_delete=models.CASCADE)
	permission = models.ManyToManyField(Permission)

	def __str__(self):
		return self.role.role_type

class Employees(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee_other_details')
	contact = models.CharField(max_length=13, null=True, blank=True)
	email = models.CharField(max_length=200, null=True, blank=True)
	address = models.CharField(max_length=200, null=True, blank=True)
	city = models.CharField(max_length=50, null=True, blank=True)
	pincode = models.IntegerField(null=True, blank=True)
	father_name = models.CharField(max_length=50, null=True, blank=True)
	mother_name = models.CharField(max_length=50, null=True, blank=True)
	pan_no = models.CharField(max_length=100, null=True, blank=True)
	approved = models.BooleanField(default=False)
	created_on = models.DateTimeField(auto_now_add=True)
	approved_on = models.DateTimeField(auto_now=True)
	senior_employee = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='senior_employee', null=True)

	def __str__(self):
		return self.user.first_name+' '+self.user.last_name

class Department(models.Model):
    name = models.CharField(max_length=20)