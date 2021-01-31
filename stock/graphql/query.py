import graphene
from stock.graphql.types import *
from django.db.models import Q
import math
from django.core.paginator import Paginator

class BaseQuery(graphene.ObjectType):

    vehicles = graphene.List(VehicleType)
    vendors = graphene.List(VendorType)
    vendor_by_name = graphene.Field(VendorType, name=graphene.String(required=True))
    vehicle_by_category = graphene.List(VehicleType, category=graphene.String(required=True))        
    vehicle_by = graphene.List(VehicleType, 
                    vendor=graphene.String(required=True), 
                    category=graphene.String(required=True)
                )

    # Pagination example    

    vehicle_by_pagination = graphene.List(VehiclePaginatorType,                        
                        offset=graphene.Int(required=True),
                        limit=graphene.Int(required=True)                                              
                    )                                                                        

    def resolve_vehicles(root, info):
        return Vehicle.objects.select_related("vendor").all()

    def resolve_vendors(root, info):
        return Vendor.objects.prefetch_related("vehicles").all()    
        
    def resolve_vendor_by_name(root, info, name):
        try:
            return Vendor.objects.get(name=name)    
        except Vendor.DoesNotExist:
            return None

    def resolve_vehicle_by_category(root, info, category):
        try:
            return Vehicle.objects.filter(category__name=category)
        except Vehicle.DoesNotExist:
            return None        

    def resolve_vehicle_by(root, info, vendor, category):
        try:
            return Vehicle.objects.filter(Q(category__name=category) & Q(vendor__name=vendor))
        except Vehicle.DoesNotExist:
            return None  

    # Pagination example
    def resolve_vehicle_by_pagination(root, info, offset, limit):
        #count = Vehicle.objects.count()                        
        #pages = math.ceil(count / limit)        
        vehicles = Vehicle.objects.all()[offset:offset+limit]                                     
        return vehicles        
