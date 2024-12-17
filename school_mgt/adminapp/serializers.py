from rest_framework import serializers
from accounts.models import *

class OfficeStaffSerializer(serializers.ModelSerializer):
    email = serializers.CharField(source='user.email', read_only=True)
    full_name = serializers.CharField(source='user.full_name', read_only=True)
    contact_number = serializers.CharField(source='user.contact_number', read_only=True)  # Make sure this field exists
    date_joined =  serializers.CharField(source='user.date_joined', read_only=True)

    class Meta:
        model = OfficeStaff
        fields = ['id', 'email', 'full_name','contact_number','address','custom_id','date_joined']

class LibrarianSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email',read_only=True)   
    full_name = serializers.CharField(source='user.full_name',read_only=True)  
    contact_number = serializers.CharField(source ='user.contact_number',read_only=True)   
    
    class Meta:
        model = Librarian
        fields = ['custom_id','email','full_name','contact_number','address']


class StudentSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email',read_only=True)   
    full_name = serializers.CharField(source='user.full_name',read_only=True)  
    contact_number = serializers.CharField(source ='user.contact_number',read_only=True)
    address = serializers.CharField(source ='user.address',read_only=True)
    
    class Meta:
        model = Student
        fields = ['email','full_name','contact_number','address','roll_number','class_name','date_of_birth','guardian_name','guardian_contact','custom_id',]  
    
class LibraryHistorySerializer(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all())
    
    class Meta:
        model = LibraryHistory
        fields = ['student', 'book_name', 'borrow_date', 'return_date', 'status']

    def validate(self, data):
        """
        Custom validation to ensure that return_date is after borrow_date.
        """
        borrow_date = data.get('borrow_date')
        return_date = data.get('return_date')

        # If return_date is provided, validate it
        if return_date and return_date < borrow_date:
            raise serializers.ValidationError("Return date cannot be earlier than borrow date.")
        
        return data


class FeesHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FeesHistory
        fields = ['student', 'fee_amount', 'fee_status', 'due_date', 'payment_date', 'payment_method']

    def validate(self, data):
        """
        Custom validation to ensure that payment_date is not earlier than the due_date.
        """
        due_date = data.get('due_date')
        payment_date = data.get('payment_date')

        if payment_date and payment_date < due_date:
            raise serializers.ValidationError("Payment date cannot be earlier than the due date.")
        
        return data       
