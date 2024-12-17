
# from rest_framework.permissions import BasePermission

# class IsLibrarian(BasePermission):
#     """
#     Custom permission to check if the user has the 'librarian' role.
#     Assumes a 'role' field exists in the User model.
#     """
#     def has_permission(self, request, view):
#         # Adjust this check according to your user model's role or permission system
#         return request.user.role == 'librarian'  # or check for group membership, etc.
