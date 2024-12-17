from rest_framework.response import Response
from.serializers import *
from accounts.models import *
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.contrib.auth.hashers import make_password


class StudentsView(APIView):
    permission_classes = [IsAuthenticated]  
    def get(self,request):
        user = request.user
        if not user.is_office_staff:
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


class FeesHistoryAddView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        if not user.is_office_staff:
            return Response({"detail": "You dont have any permission to autherise"}, status=status.HTTP_403_FORBIDDEN)

        serializer = FeesHistorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Fees history created successfully.", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)       



        

class FeesHistoryUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        user = request.user
        if not user.is_office_staff:
            return Response({"detail": "You don't have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)

        student_id = request.data.get('student_id')

        if not student_id:
            return Response({"detail": "Student ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            fees_history = FeesHistory.objects.get(student__id=student_id)
            serializer = FeesHistorySerializer(fees_history, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response({"detail": "Fees history updated successfully.", "data": serializer.data}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except FeesHistory.DoesNotExist:
            return Response({"detail": "Fees history not found for the provided student."}, status=status.HTTP_404_NOT_FOUND)



class FeesHistoryDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user = request.user
        if not user.is_office_staff:
            return Response({"detail": "You don't have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)

        student_id = request.data.get('student_id')

        if not student_id:
            return Response({"detail": "Student ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            fees_history = FeesHistory.objects.get(student__id=student_id)
            fees_history.delete()
            return Response({"detail": "Fees history deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

        except FeesHistory.DoesNotExist:
            return Response({"detail": "Fees history not found for the provided student."}, status=status.HTTP_404_NOT_FOUND)

    


class LibraryHistoryDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        user = request.user
        if not user.is_office_staff:
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