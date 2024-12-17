from django.urls import path
from adminapp.views import OfficeStaffListView,OfficeStaffCreateView,OfficeStaffUpdateView,OfficeStaffDeleteView,LibrarianListView,LibrarianCreateView,LibrarianUpdateView,LibrarianDeleteView,StudentCreateView,StudentUpdateView,StudentDeleteView,StudentListView,LibraryHistoryDetailView,LibraryHistoryCreateView,LibraryHistoryUpdateView,LibraryHistoryDeleteView,FeesHistoryCreateView,FeesHistoryDetailView,FeesHistoryUpdateView,FeesHistoryDeleteView




urlpatterns = [
    path('officestafflist/',OfficeStaffListView.as_view(),name='officestafflist'),
    path('officestaffcreate/',OfficeStaffCreateView.as_view(),name ='officestaffcreate'),
    path('officestaffupdate/',OfficeStaffUpdateView.as_view(),name ='officestaffupdate'),
    path('officestaffdelete/',OfficeStaffDeleteView.as_view(),name ='officestaffdelete'),
    path('librarianlist/',LibrarianListView.as_view(),name='librarianlist'),
    path('librariancreate/',LibrarianCreateView.as_view(),name ='librariancreate'),
    path('librarianupdate/',LibrarianUpdateView.as_view(),name ='librarianupdate'),
    path('librariandelete/',LibrarianDeleteView.as_view(),name ='librariandelete'),
    path('studentslist/',StudentListView.as_view(),name='studentlist'),
    path('studentscreate/',StudentCreateView.as_view(),name='studentcreate'),
    path('studentsupdate/',StudentUpdateView.as_view(),name='studentupdate'),
    path('studentsdelete/',StudentDeleteView.as_view(),name='studentdelete'),
    path('libraryhistory/details/',LibraryHistoryDetailView.as_view(),name='libraryhistory'),
    path('libraryhistory/create/',LibraryHistoryCreateView.as_view(),name='libraryhistorycreate'),
    path('libraryhistory/update/',LibraryHistoryUpdateView.as_view(),name='libraryhistoryupdate'),
    path('libraryhistory/delete/',LibraryHistoryDeleteView.as_view(),name='libraryhistorydelete'),
    path('feeshistory/create/',FeesHistoryCreateView.as_view(),name = 'fesshistorycreate'),
    path('feeshistory/detail/',FeesHistoryDetailView.as_view(),name = 'fesshistorydetail'),
    path('feeshistory/update/',FeesHistoryUpdateView.as_view(),name = 'fesshistoryupdate'),
     path('feeshistory/delete/',FeesHistoryDeleteView.as_view(),name = 'fesshistorydelete'),











]




