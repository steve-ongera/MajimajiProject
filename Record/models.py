from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser


class Month(models.Model):
    TERM_CHOICES = [
        ('January', 'January'),
        ('Febuary', 'Febuary'),
        ('March', 'March'),
        ('April', 'April'),
        ('May', 'May'),
        ('June', 'June'),
        ('July', 'July'),
        ('August', 'August'),
        ('September', 'September'),
        ('October', 'October'),
        ('November', 'November'),
        ('December', 'December'),
    ]
    name = models.CharField(max_length=10, choices=TERM_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.name
    

class Profile(models.Model):
    USER_TYPE_CHOICES = [
        ('guest', 'Guest'),
        ('admin', 'Admin'),
        ('developer', 'Developer'),
        
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)

    def __str__(self):
        return f"{self.user.username} - {self.get_user_type_display()}"
    


    
class Payment_Year(models.Model):
    name = models.CharField(max_length=100)
    month = models.ManyToManyField(Month )

    def __str__(self):
        return self.name


class House(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return f" {self.name}"



class Tenant(models.Model):
  
    user_name = models.CharField(max_length=100)
    identification_number = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    avatar = models.ImageField(upload_to='media', default='media/avatar.svg')
    house = models.ForeignKey(House,  on_delete=models.CASCADE)
    tap_no = models.CharField(max_length=100 , null=True, blank=True)
   
    

    def __str__(self):
        return f"{self.first_name} {self.last_name}~{self.identification_number}--{self.house.name}"



class tenants_database(models.Model):
    username = models.CharField(max_length=100 )
    identification_number = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=20)
    avatar = models.ImageField(upload_to='avatars/', default='avatars/avatar.svg')
  
    

    def __str__(self):
        return f"{self.username} ~ {self.first_name} {self.last_name} - {self.identification_number}"
    


class MonthlySignOff(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    month = models.ForeignKey(Month, on_delete=models.CASCADE)
    signed_off = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('tenant', 'month')

    def __str__(self):
        return f"{self.tenant.first_name} {self.tenant.last_name} - {self.month.name}"
    

class Payment(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    month = models.ForeignKey(Month, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    mpesa_code=models.CharField(max_length=100)
    date_paid = models.DateField()

    class Meta:
        unique_together = ('tenant', 'month')

    def __str__(self):
        return f"{self.tenant} - {self.month} - {self.amount}"
    


class MaintenanceRequest(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ], default='pending')
    date_created = models.DateTimeField(auto_now_add=True)
    date_completed = models.DateTimeField(null=True, blank=True)
    response = models.TextField(blank=True)
    
    def __str__(self):
        return f"Request from {self.tenant.first_name} {self.tenant.last_name} - {self.date_created}"


class QnAResponse(models.Model):
    question = models.CharField(max_length=255)
    response = models.TextField()

    def __str__(self):
        return self.question