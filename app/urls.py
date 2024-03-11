from django.urls import path
from .views import schedule_due,growingcrop, calculatebill

urlpatterns = [
    path('due_schedule/', schedule_due, name='due_schedule'),
    path('ongoing/', growingcrop, name='ongoing'),
    path('invoice/<int:farmer_id>/', calculatebill, name='invoice'),

]
