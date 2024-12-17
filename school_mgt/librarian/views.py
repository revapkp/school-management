from rest_framework.response import Response
from.serializers import *
from accounts.models import *
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.contrib.auth.hashers import make_password



class LibraryHistoryView(APIView):
    def get(self,request):
        user = request.user
        if not user.is_librarian:
            return Response({"detail":"you cant permission to autherise"},status=status.HTTP_403_FORBIDDEN)
        student_id = request.data.get('student_id')  
        try:
            if student_id:
                
                histories = LibraryHistory.objects.filter(student__id=student_id)
                if not histories.exists():
                    return Response({"detail": "No library history found for the provided student."}, status=status.HTTP_404_NOT_FOUND)
            else:
                histories = LibraryHistory.objects.all()
            serializer = LibraryHistorySerializer(histories, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            # Handle any potential issues with filtering or database queries
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    



class StudentsDetailsView(APIView):
    permission_classes = [IsAuthenticated]  
    def get(self,request):
        user = request.user
        if not user.is_librarian:
            return Response({"detail":"you cant permission to autherise"},status=status.HTTP_403_FORBIDDEN)
        custom_id = request.query_params.get('custom_id')
        if custom_id:
            try:
                students= Student.objects.get(custom_id=custom_id)
                serializer = StudentSerializer(librarians)
                return Response(serializer.data,status=status.HTTP_201_CREATED)
            except Student.DoesNotExist:
                return Response({"detail":"student not found"},status = status.HTTP_404_NOT_FOUND)
        else :
            students = Student.objects.all()   
            serializer = StudentSerializer(students,many = True)    
            return Response(serializer.data,status=status.HTTP_201_CREATED)    
    

    