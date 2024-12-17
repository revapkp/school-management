from rest_framework import serializers
from accounts.models import *

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