from django.db import models
from enums.roles import Role


class User(models.Model):
    id = models.BigAutoField(primary_key = True)
    username = models.TextField(unique = True)
    email = models.TextField(unique = True)
    password = models.TextField()
    role = models.CharField(max_length = 20, default = Role.MASON)

    class Meta:
        db_table = 'users'
        managed = False



class InvitedUser(models.Model):
    id = models.BigAutoField(primary_key = True)
    email = models.TextField(unique = True)

    class Meta:
        db_table = 'invited_users'
        managed = False
