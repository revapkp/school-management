from django.urls import path
from librarian.views import LibraryHistoryView,StudentsDetailsView

urlpatterns = [
    path('libraryhistoryview/',LibraryHistoryView.as_view(),name = 'libraryhistoryview'),
    path('studentdetailsview/',StudentsDetailsView.as_view(),name='studentdetailsview')
]