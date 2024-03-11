from django.shortcuts import render
from .models import Farm, Farmer, Schedule
from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime, date, timedelta
# Create your views here.


def schedule_due(request):
    farms_with_schedule=Farm.objects.prefetch_related('schedule_set').all()
    due_farmer=[]
    
    for farm in farms_with_schedule:
        for schedules in farm.schedule_set.all():
            date_after_sowing=farm.sowing_date+timedelta(days=schedules.days_after_sowing)
            curr_day=date.today()
            
            if date_after_sowing==curr_day or date_after_sowing==curr_day+timedelta(days=1):
                due_farmer.append({
                    'farmer_id': farm.farmer.id,
                    'phone_number': farm.farmer.phone_number,
                    'name': farm.farmer.name,
                    'language': farm.farmer.language
                })
                
    return JsonResponse({'due_farmers': due_farmer})


def growingcrop(request):
    farms_with_schedule=Farm.objects.prefetch_related('schedule_set').all()
    farmer_growing=[]
    for farm in farms_with_schedule:
        for schedules in farm.schedule_set.all():
            date_after_sowing=farm.sowing_date+timedelta(days=schedules.days_after_sowing)
            curr_day=date.today()
            
            if date_after_sowing>curr_day:
                farmer_growing.append({
                    'farmer_id': farm.farmer.id,
                    'phone_number': farm.farmer.phone_number,
                    'name': farm.farmer.name,
                    'language': farm.farmer.language,
                    'sowing_end_date':date_after_sowing         
                })
                
    return JsonResponse({'ongoing_farmers': farmer_growing})
    

def calculatebill(request, farmer_id):
    try:
        farmer=Farmer.objects.get(pk=farmer_id)
        schedules=Schedule.objects.filter(farm__farmer=farmer)
        total_cost=0
        details=[]
        
        for schedule in schedules:
            equivalent_quantity=1
            if schedule.quantity_unit.lower() in ["kg", "kilogram"]:
                equivalent_quantity=1
                total_price=schedule.fertiliser*schedule.quantity*equivalent_quantity
                total_cost+=total_price
                
            elif schedule.quantity_unit.lower() in ["g","gram"]:
                equivalent_quantity=0.001
                total_price=schedule.fertiliser*schedule.quantity*equivalent_quantity
                total_cost+=total_price
                
            elif schedule.quantity_unit.lower() in ['ton']:
                equivalent_quantity=1000
                total_price=schedule.fertiliser*schedule.quantity*equivalent_quantity
                total_cost+=total_price
                
            elif schedule.quantity_unit.lower() in ['litre', 'l']:
                equivalent_quantity=1
                total_price=schedule.fertiliser*schedule.quantity*equivalent_quantity
                total_cost+=total_price
            
            elif schedule.quantity_unit.lower() in ['ml', 'millilitre']:
                equivalent_quantity=0.001
                total_price=schedule.fertiliser*schedule.quantity*equivalent_quantity
                total_cost+=total_price
                
            
            details.append({
                'farmer_id':farmer_id,
                'name':farmer.name,
                'phone_number':farmer.phone_number,
                'language':farmer.language,
                'price per kg/l':schedule.fertiliser,
                'quantity':schedule.quantity,
                'quantity unit':schedule.quantity_unit,
                'bill':total_cost
            })
            
        return JsonResponse( {'invoice_data': details})

    except Farmer.DoesNotExist:
        return JsonResponse({'error': 'farmer not found'}, status=404)
        
        



    

