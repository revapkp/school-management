from django.urls import path
from officestaff.views import StudentsView,FeesHistoryAddView,FeesHistoryUpdateView,FeesHistoryDeleteView,LibraryHistoryDetailView

urlpatterns =[
    path('studentsview/', StudentsView.as_view(),name ='studentsview'),
    path('feeshistory/add/',FeesHistoryAddView.as_view(),name = 'feesaddview'),
    path('feeshistory/update/',FeesHistoryUpdateView.as_view(),name = 'feesupdateview'),
    path('feeshistory/delete/',FeesHistoryDeleteView.as_view(),name = 'feesdeleteview'),
    path('libraryhistoryview/',LibraryHistoryDetailView.as_view(),name='libraryhistoryview')

    


]
