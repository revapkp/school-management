from rest_framework.response import Response
from.serializers import *
from accounts.models import *
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from django.contrib.auth.hashers import make_password


                # officestaff list,create,update,delete

class OfficeStaffListView(APIView):
    permission_classes = [IsAuthenticated]  

    def get(self, request):
        user = request.user
        if not user.is_admin:
            return Response({"detail":"you have not permission to view this content"},status=status.HTTP_403_FORBIDDEN)
        
        custom_id = request.data.get('custom_id')  
        if custom_id:
            try:
                office_staff = OfficeStaff.objects.get(custom_id=custom_id)
                serializer = OfficeStaffSerializer(office_staff)
                return Response(serializer.data)
            except OfficeStaff.DoesNotExist:
                return Response({"detail": "Office Staff not found"}, status=404)
        else:
            office_staff = OfficeStaff.objects.all()
            serializer = OfficeStaffSerializer(office_staff, many=True)
            return Response(serializer.data,status=status.HTTP_201_CREATED)


class OfficeStaffCreateView(APIView):
    permission_classes = [IsAuthenticated]  
    def post(self, request):
        user = request.user
        if not user.is_admin:
            return Response({"detail": "You don't have permission to create office staff."}, status=status.HTTP_403_FORBIDDEN)
        email = request.data.get('email')
        username = request.data.get('username')
        password = request.data.get('password')
        full_name = request.data.get('full_name')
        contact_number = request.data.get('contact_number')
        address = request.data.get('address')

        if not email or not username or not password:
            return Response({"detail": "Email, username, and password are required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            
            if User.objects.filter(username=username).exists():
                return Response({"detail": "Username already exists."}, status=status.HTTP_400_BAD_REQUEST)
            
            if User.objects.filter(email=email).exists():
                return Response({"detail": "Email already exists."}, status=status.HTTP_400_BAD_REQUEST)

            # Create the User object
            user = User.objects.create(
                username=username,
                email=email,
                password=make_password(password),
                full_name=full_name,
                contact_number=contact_number
            )

           
            office_staff = OfficeStaff.objects.create(
                user=user,
                address=address
            )
            serializer = OfficeStaffSerializer(office_staff)
            return Response({"message":" user created successfully","data":serializer.data}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class OfficeStaffUpdateView(APIView):
    permission_classes = [IsAuthenticated]  
    def patch(self, request):
        user = request.user
        if not user.is_admin:
            return Response({"detail": "You don't have permission to create office staff."}, status=status.HTTP_403_FORBIDDEN)
        try:
            custom_id = request.data.get('custom_id')
            if not custom_id:
                return Response({"detail": "custom_id is required."}, status=status.HTTP_400_BAD_REQUEST)
            office_staff = OfficeStaff.objects.get(custom_id=custom_id)
            email = request.data.get('email')
            username = request.data.get('username')
            full_name = request.data.get('full_name')
            contact_number = request.data.get('contact_number')
            address = request.data.get('address')

            
            user = office_staff.user

            if email:
                user.email = email
            if username:
                user.username = username
            if full_name:
                user.full_name = full_name
            if contact_number:
                user.contact_number = contact_number
            user.save()
            if address:
                office_staff.address = address
            office_staff.save()

            serializer = OfficeStaffSerializer(office_staff)

            return Response({"message": "Office staff updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)

        except OfficeStaff.DoesNotExist:
            return Response({"detail": "Office staff not found with the given custom_id."}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class OfficeStaffDeleteView(APIView):
    permission_classes = [IsAuthenticated]  
    def delete(self, request):
       
        try:
            custom_id = request.data.get('custom_id')
            if not custom_id:
                return Response({"detail": "custom_id is required."}, status=status.HTTP_400_BAD_REQUEST)
            office_staff = OfficeStaff.objects.get(custom_id=custom_id)
            if not request.user.is_admin:
                return Response({"detail": "You don't have permission to delete office staff."}, status=status.HTTP_403_FORBIDDEN)

           
            user = office_staff.user  
            office_staff.delete() 
            return Response({"message": "Office staff deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

        except OfficeStaff.DoesNotExist:
            return Response({"detail": "Office staff not found with the given custom_id."}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
           

        #    librarian list,create,update,delete


class LibrarianListView(APIView):
    permission_classes =[IsAuthenticated]   
    def get(self,request):
        user = request.user
        if not user.is_admin:
            return Response({"detail":"you have not permission to autherise"},status = status.HTTP_403_FORBIDDEN)

        custom_id = request.query_params.get('custom_id')
        if custom_id:
            try:
                librarians = Librarian.objects.get(custom_id=custom_id)
                serializer = LibrarianSerializer(librarians)
                return Response(serializer.data,status=status.HTTP_201_CREATED)
            except librarian.DoesNotExist:
                return Response({"detail":"librarian not found"},status = status.HTTP_404_NOT_FOUND)
        else :
            librarians = Librarian.objects.all()   
            serializer = LibrarianSerializer(librarians,many = True)    
            return Response(serializer.data,status=status.HTTP_201_CREATED)


class LibrarianCreateView(APIView):
    permission_classes =[IsAuthenticated]  
    def post(self,request):
        user = request.user
        if not user.is_admin:
            return Response({"detail":"you have not permission to autherise"},status = status.HTTP_403_FORBIDDEN)
        email = request.data.get('email')
        username = request.data.get('username')
        password = request.data.get('password')
        full_name = request.data.get('full_name')
        contact_number = request.data.get('contact_number')
        address = request.data.get('address')

        if not email or not password or not username:
            return Response({"detail":'email,password,username must required'},status = status.HTTP_400_BAD_REQUEST)
        try:
            
            if User.objects.filter(username=username).exists():
                return Response({"detail": "Username already exists."}, status=status.HTTP_400_BAD_REQUEST)
            
            if User.objects.filter(email=email).exists():
                return Response({"detail": "Email already exists."}, status=status.HTTP_400_BAD_REQUEST)
            
            user = User.objects.create(
                email = email,
                username = username,
                password = make_password(password),
                full_name=full_name,
                contact_number=contact_number
                
            )
            librarians = Librarian.objects.create(
                user=user,
                address=address
            )
            serializer = LibrarianSerializer(librarians)
            return Response({"message":" user created successfully","data":serializer.data}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




class LibrarianUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    def patch(self,request):
        user = request.user
        if not user.is_admin:
            return Response({"detail":"you have not permission to autherise"},status = status.HTTP_403_FORBIDDEN)
        custom_id = request.data.get('custom_id')
        if not custom_id:
            return Response({"detail":"custom_id is required"})
        try:
            librarians =Librarian.objects.get(custom_id=custom_id)   
        except Librarian.DoesNotExist:
            return Response({"detail":"librarian not found"},status = status.HTTP_404_NOT_FOUND)   

        user = librarians.user
    
        email = request.data.get('email')
        username = request.data.get('username')
        full_name = request.data.get('full_name')
        contact_number = request.data.get('contact_number')
        address = request.data.get('address')

        if email:
            user.email = email
        if username:
            user.username = username
        if full_name:
            user.full_name = full_name
        if contact_number:
            user.contact_number = contact_number
            user.save()
        if address:
            librarians.address = address

            librarians.save()

        serializer = LibrarianSerializer(librarians)

        return Response({"message": "librarian updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)

       
        
       
class LibrarianDeleteView(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self,request):
        user = request.user
        if not user.is_admin:
            return Response({"detail":"you have not permission to autherise"},status = status.HTTP_403_FORBIDDEN)
        custom_id = request.data.get('custom_id') 
        if not custom_id:
            return Response({"detail":"custom_id is required"},status = status.HTTP_404_NOT_FOUND)   
        try:
            librarians =Librarian.objects.get(custom_id=custom_id)
        except Librarian.DoesNotExist:
            return Response({"detail":"librarian does not exist with the custom_id"}) 

        user = librarians.user  
        librarians.delete() 
        return Response({"message": "librarian deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

       
    #    student CRUD operation

class StudentListView(APIView):
    permission_classes =[IsAuthenticated]   
    def get(self,request):
        user = request.user
        if not user.is_admin:
            return Response({"detail":"you have not permission to autherise"},status = status.HTTP_403_FORBIDDEN)

        custom_id = request.query_params.get('custom_id')
        if custom_id:
            try:
                students= Student.objects.get(custom_id=custom_id)
                serializer = StudentSerializer(students)
                return Response(serializer.data,status=status.HTTP_201_CREATED)
            except Student.DoesNotExist:
                return Response({"detail":"student not found"},status = status.HTTP_404_NOT_FOUND)
        else :
            students = Student.objects.all()   
            serializer = StudentSerializer(students,many = True)    
            return Response(serializer.data,status=status.HTTP_201_CREATED)    

class StudentCreateView(APIView):
    permission_classes = [IsAuthenticated]   
    def post(self,request):
        user = request.user
        if not user.is_admin:
            return Response({"detail":"you cant permission to autherise"},status= status.HTTP_403_FORBIDDEN)

        email = request.data.get('email')
        username = request.data.get("username")
        password = request.data.get("password") 
        full_name = request.data.get("full_name")
        date_of_birth = request.data.get("date_of_birth")
        roll_number = request.data.get("roll_number")
        date_joined = request.data.get("date_joined")
        class_name = request.data.get("class_name")
        address = request.data.get("address")
        guardian_name = request.data.get("guardian_name"),
        contact_number = request.data.get("contact_number")

        if not email or not password or not username:
            return Response({"detail": 'Email, password, and username are required.'}, status=status.HTTP_400_BAD_REQUEST)

        
        if User.objects.filter(username=username).exists():
            return Response({"detail": "Username already exists."}, status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(email=email).exists():
            return Response({"detail": "Email already exists."}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create(
                email = email,
                username = username,
                password = make_password(password),
                full_name=full_name,
                contact_number=contact_number,
                address = address
                
            )
        students = Student.objects.create(
            user=user,
            roll_number = roll_number,
            class_name = class_name,
            date_of_birth =date_of_birth,
            guardian_name = guardian_name
         )   
        serializer = StudentSerializer(students)
        return Response({"message":" studentcreated successfully","data":serializer.data}, status=status.HTTP_201_CREATED)

   

class StudentUpdateView(APIView):
    permission_classes =[IsAuthenticated] 
    def patch(self,request):
        user = request.user
        if not user.is_admin:
            return Response({"detail":"you cant permission to autherise"},status= status.HTTP_403_FORBIDDEN)
        custom_id =request.data.get('custom_id')
        if not custom_id:
            return Response({"detail":"custom_id is required"})
        try:
            students = Student.objects.get(custom_id=custom_id)   
        except Student.DoesNotExist:
            return Response({"detail":"student not found with this id"},status = status.HTTP_404_NOT_FOUND) 

        user = students.user 
        email = request.data.get('email')
        username = request.data.get("username")
        password = request.data.get("password") 
        full_name = request.data.get("full_name")
        contact_number =request.data.get('contact_number')
        date_of_birth = request.data.get("date_of_birth")
        roll_number = request.data.get("roll_number")
        date_joined = request.data.get("date_joined")
        class_name = request.data.get("class_name")
        address = request.data.get("address")
        guardian_name = request.data.get("guardian_name")

        if email:
            user.email = email
        if username:
            user.username = username
        if full_name:
            user.full_name = full_name
        if contact_number:
            user.contact_number = contact_number
            user.save()
        if address:
            user.address = address
            user.save()
        if date_of_birth:
            students.date_of_birth = date_of_birth
            students.save()
        if roll_number:
            students.roll_number=roll_number
            student.save()  
        if class_name:
            students.class_name =class_name
            students.save()  
        if guardian_name:
            students.guardian_name = guardian_name
            students.save() 
        serializer = StudentSerializer(students)
        return Response({"message": "student updated successfully" }, status=status.HTTP_200_OK)

               
class StudentDeleteView(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self,request):
        user = request.user
        if not user.is_admin:
            return Response({"detail":"you have not permission to autherise"},status = status.HTTP_403_FORBIDDEN)
        custom_id = request.data.get('custom_id') 
        if not custom_id:
            return Response({"detail":"custom_id is required"},status = status.HTTP_404_NOT_FOUND)   
        try:
            students =Student.objects.get(custom_id=custom_id)
        except Student.DoesNotExist:
            return Response({"detail":"student does not exist with the custom_id"}) 

        user = students.user  
        students.delete() 
        return Response({"message": "student deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

        #  library history CRUD operation

class LibraryHistoryDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        user = request.user
        if not user.is_admin:
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
        
class LibraryHistoryCreateView(APIView):
    permission_classes = [IsAuthenticated ]
    def post(self,request):
        user= request.user
        if not user.is_admin:
            return Response({"detail":"you cant permission to autherise"},status=status.HTTP_403_FORBIDDEN)
        serializer = LibraryHistorySerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response({
                "detail": "Library history created successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LibraryHistoryUpdateView(APIView):
    permission_classes = [IsAuthenticated ]
    def patch(self,request):
        user= request.user
        if not user.is_admin:
            return Response({"detail":"you cant permission to autherise"},status=status.HTTP_403_FORBIDDEN)
        student_id = request.data.get('student_id')
        book_name = request.data.get('book_name')
        borrow_date = request.data.get('borrow_date')
        return_date = request.data.get('return_date')
        status = request.data.get('status')
        if not student_id:
            return Response({"detail": "Student ID is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            library_history = LibraryHistory.objects.get(student__id=student_id)
            if book_name:
                library_history.book_name = book_name
            if borrow_date:
                library_history.borrow_date = borrow_date
            if return_date:
                library_history.return_date = return_date
            if status:
                library_history.status = status
            library_history.save()

            serializer = LibraryHistorySerializer(library_history)
            return Response({
                "detail": "Library history updated successfully.",
                "data": serializer.data
            })

        except LibraryHistory.DoesNotExist:
            # If the student doesn't have any library history, return a 404 error
            return Response({"detail": "Library history not found for the provided student."}, status=status.HTTP_404_NOT_FOUND)
        
        
class LibraryHistoryDeleteView(APIView):
    permission_classes = [IsAuthenticated ]
    def delete(self,request):
        user= request.user
        if not user.is_admin:
            return Response({"detail":"you cant permission to autherise"},status=status.HTTP_403_FORBIDDEN)
        student_id = request.data.get('student_id')
        if not student_id:
            return Response({"detail": "Student ID is required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            library_history = LibraryHistory.objects.get(student__id=student_id)
            library_history.delete()
            return Response({"detail": "Library history record deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

        except LibraryHistory.DoesNotExist:
            return Response({"detail": "Library history not found for the provided student."}, status=status.HTTP_404_NOT_FOUND)

        # fees history CRUD opeartion



class FeesHistoryCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        if not user.is_admin:
            return Response({"detail": "You dont have any permission to autherise"}, status=status.HTTP_403_FORBIDDEN)

        serializer = FeesHistorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Fees history created successfully.", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)       


class FeesHistoryDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if not user.is_admin:
            return Response({"detail": "You don't have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)

        student_id = request.query_params.get('student_id')

        if student_id:
            try:
                history = FeesHistory.objects.filter(student__id=student_id)
                if not history.exists():
                    return Response({"detail": "No fees history found for this student."}, status=status.HTTP_404_NOT_FOUND)
                serializer = FeesHistorySerializer(history, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except FeesHistory.DoesNotExist:
                return Response({"detail": "Fees history not found."}, status=status.HTTP_404_NOT_FOUND)

        
        history = FeesHistory.objects.all()
        serializer = FeesHistorySerializer(history, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FeesHistoryUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        user = request.user
        if not user.is_admin:
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
        if not user.is_admin:
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
