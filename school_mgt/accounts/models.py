
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone

class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_staff', True)  
        return self.create_user(email, username, password, **extra_fields)

    
class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    full_name = models.CharField(max_length=200, blank=True)
    address = models.CharField(max_length=250, blank=True)
    contact_number = models.CharField(max_length=15, blank=True, null=True)
    is_admin = models.BooleanField(default=False)
    is_office_staff = models.BooleanField(default=False)
    is_librarian = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)  
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.email

    @property
    def is_superuser(self):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        """Check if the user has a specific permission."""
        if self.is_superuser:
            return True
        return self.user_permissions.filter(codename=perm).exists()

    def has_module_perms(self, app_label):
        """Check if the user has permissions for a specific app."""
        if self.is_superuser:
            return True
        return self.user_permissions.filter(content_type__app_label=app_label).exists()

    def get_group_permissions(self):
        """Return the permissions for a user's groups."""
        permissions = super().get_group_permissions()
        return permissions
    
    

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    roll_number = models.CharField(max_length=20, unique=True)
    class_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    guardian_name = models.CharField(max_length=100)
    guardian_contact = models.CharField(max_length=15)
    custom_id = models.CharField(max_length=20, unique=True, editable=False, blank=True)

    def save(self, *args, **kwargs):
        if not self.custom_id:
            self.custom_id = f'ST{self.user.id}'  
        super().save(*args, **kwargs)

    def full_name_with_custom_id(self):
        return f'{self.user.full_name} ({self.custom_id})'

    def __str__(self):
        return self.full_name_with_custom_id() 


# Library History Model
    
class LibraryHistory(models.Model):
    STATUS_CHOICES = [
        ('borrowed', 'Borrowed'),
        ('returned', 'Returned'),
        ('overdue', 'Overdue'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="library_histories")
    book_name = models.CharField(max_length=200)
    borrow_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='borrowed')

    def __str__(self):
        return f"{self.student.user.username} borrowed {self.book_name} ({self.status})"


# Fees History Model
class FeesHistory(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    fee_amount = models.DecimalField(max_digits=8, decimal_places=2)
    fee_status = models.CharField(max_length=50, choices=[('paid', 'Paid'), ('unpaid', 'Unpaid')])
    due_date = models.DateField()
    payment_date = models.DateField(null=True, blank=True)
    payment_method = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.student.user.username} - {self.fee_status} - {self.fee_amount}"




class OfficeStaff(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='office_staff')
    custom_id = models.CharField(max_length=20, unique=True, editable=False, blank=True)
    address = models.CharField(max_length=250, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.custom_id}"

    def save(self, *args, **kwargs):
        if not self.custom_id:
            self.custom_id = f'OS{self.user.id}'  
        super(OfficeStaff, self).save(*args, **kwargs)





class Librarian(models.Model):
   
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='librarian')
    custom_id = models.CharField(max_length=20, unique=True, editable=False, blank=True)
    address = models.CharField(max_length=250, blank=True, null=True)

    def __str__(self):
        return f"Librarian: {self.user.username} - {self.custom_id}"

    def save(self, *args, **kwargs):
        if not self.custom_id:
            self.custom_id = f'LIB{self.user.id}'  
        super(Librarian, self).save(*args, **kwargs)
   


       