from django.db import models
from django.contrib.auth.models import *
import uuid
# Create your models here.



class User(AbstractUser):
    STATUS = (
        ("DELETED", "User deleted"),
        ("ACTIVE", "Active user"),
        ("INACTIVE", "Inactive user"),
    )
    GENDER_STATUS =(
        ("MALE","user is male"),
        ("FEMALE","user is female"),
        ("NONE","user is female"),
            
    )
    id = models.UUIDField(primary_key=True,unique=True,default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=50, unique=True);
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True,)
    phone =models.CharField(max_length=20)
    blood_group=models.CharField(max_length=5,null=True)
    dob= models.DateTimeField(null=True)
    height = models.CharField(max_length=10 ,null=True)
    gender = models.CharField(max_length=10, choices=GENDER_STATUS,null=True, default='NONE')
    profile = models.ImageField(upload_to="uploads/", null=True, blank=True)
    profile_binary = models.TextField()
    
    USERNAME_FIELD ="email"
    
    
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table= 'user'
        