<<<<<<< HEAD
from django.db import models
# --------------------------------------------------------------   Create database name "project_user"  ----------------------------------------------------------------------------
# create table Query

# CREATE TABLE signup_data (
#     id SERIAL PRIMARY KEY,
#     firstname CharField,
#     lastname CharField,
#     mobileno CharField,
#     email CharField,
#     username CharField,
#     password CharField
# );

# CREATE TABLE contact_data (
#     id SERIAL PRIMARY KEY,
#     name CharField,
#     email CharField,
#     message CharField
# );

# CREATE TABLE payment (
#     id SERIAL PRIMARY KEY,
#     card_name CharField,
#     card_no CharField,
#     date CharField,
#     cvv CharField
# );

class Sign_up(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(blank=True, null=True)
    last_name = models.CharField(blank=True, null=True)
    mobile = models.CharField(blank=True, null=True)
    username = models.CharField(blank=True, null=True)
    password = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sign_up'

class Contact_us(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(blank=True, null=True)
    email = models.CharField(blank=True, null=True)
    message = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'contact_us'

from .fields import CustomTimeField

class Payment(models.Model):
    id = models.AutoField(primary_key=True)
    card_name = models.CharField(blank=True,null=True)
    card_no = models.CharField(blank=True, null=True)
    date = models.CharField(blank=True, null=True)
    cvv = models.CharField(blank=True, null=True)
    time = CustomTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'payment'
    
# class IMAGE(models.Model):
#     id = models.AutoField(primary_key=True)
#     image = models.TextField(blank=True,null=True)
#     title = models.TextField(blank=True,null=True)
#     description = models.TextField(blank=True,null=True)

#     class Meta:
#         managed = False
#         db_table = 'image'
=======
from django.db import models

# -------------------------------------------   Create database name "project_user"  ------------------------------------
# create table Query

# CREATE TABLE signup_data (
#     id SERIAL PRIMARY KEY,
#     firstname CharField,
#     lastname CharField,
#     mobileno CharField,
#     email CharField,
#     username CharField,
#     password CharField
# );

# CREATE TABLE contact_data (
#     id SERIAL PRIMARY KEY,
#     name CharField,
#     email CharField,
#     message CharField
# );

# CREATE TABLE payment (
#     id SERIAL PRIMARY KEY,
#     card_name CharField,
#     card_no CharField,
#     date CharField,
#     cvv CharField
# );

class Sign_up(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(blank=True, null=True)
    last_name = models.CharField(blank=True, null=True)
    mobile = models.CharField(blank=True, null=True)
    username = models.CharField(blank=True, null=True)
    password = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sign_up'

class Contact_us(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(blank=True, null=True)
    email = models.CharField(blank=True, null=True)
    message = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'contact_us'

from .fields import CustomTimeField

class Payment(models.Model):
    id = models.AutoField(primary_key=True)
    card_name = models.CharField(blank=True,null=True)
    card_no = models.CharField(blank=True, null=True)
    date = models.CharField(blank=True, null=True)
    cvv = models.CharField(blank=True, null=True)
    time = CustomTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'payment'
    
class IMAGE(models.Model):
    id = models.AutoField(primary_key=True)
    image = models.TextField(blank=True,null=True)
    title = models.TextField(blank=True,null=True)
    description = models.TextField(blank=True,null=True)

    class Meta:
        managed = False
        db_table = 'image'

# class MENU(models.Model):
#     id = models.AutoField(primary_key=True)
#     image = models.TextField(blank=True,null=True)
#     title = models.TextField(blank=True,null=True)
#     price = models.TextField(blank=True,null=True)

#     class Meta:
#         managed = False
#         db_table = 'menu'
>>>>>>> 591af9b (Initial commit)
