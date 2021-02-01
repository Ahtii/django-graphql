import graphene
from stock.graphql.types import *
from django.db.models import Q
import math
#from django.core.paginator import Paginator

# For Relay Pagination
from graphene_django.filter import DjangoFilterConnectionField

class OffsetPagination(graphene.ObjectType):

    vehicles = graphene.List(VehicleType)    
    total_pages = graphene.Int() 
    total_records = graphene.Int()   
    has_next = graphene.Boolean()
    has_prev = graphene.Boolean()

class BaseQuery(graphene.ObjectType):

    vehicles = graphene.List(VehicleType)
    vendors = graphene.List(VendorType)
    vendor_by_name = graphene.Field(VendorType, name=graphene.String(required=True))
    vehicle_by_category = graphene.List(VehicleType, category=graphene.String(required=True))        
    vehicle_by = graphene.List(VehicleType, 
                    vendor=graphene.String(required=True), 
                    category=graphene.String(required=True)
                )

    # Pagination example (Offset pagination)

    vehicle_by_offset_paginator = graphene.Field(OffsetPagination,
                        offset=graphene.Int(required=True),
                        limit=graphene.Int(required=True)
                    )                                                 

    # Relay pagination example (Cursor pagination)

    vehicle = relay.Node.Field(VehicleNode)
    all_vehicles = DjangoFilterConnectionField(VehicleNode)    

    vendor = relay.Node.Field(VendorNode)
    all_vendors = DjangoFilterConnectionField(VendorNode)    


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
    def resolve_vehicle_by_offset_paginator(root, info, offset, limit):
        
        vehicles = Vehicle.objects.all()
        count = len(vehicles)                        
        vehicles = vehicles[offset:offset+limit]                                     
        
        total = math.ceil(count / limit)        

        has_next = False if offset >= (count - limit) else True            
        has_prev = False if offset == 0 else True
        
        return OffsetPagination(
            vehicles = vehicles,
            total_pages = total,
            total_records = count,            
            has_next = has_next,
            has_prev = has_prev
        )        
            
