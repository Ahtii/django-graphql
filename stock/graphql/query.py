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

    # GraphQL Filter with Relay

    vehicle = relay.Node.Field(VehicleNode)
    all_vehicles = DjangoFilterConnectionField(VehicleNode)                                     

    # GraphQL Filter without Relay

    vehicle_filter = graphene.List(VehicleType,
                    contains_name=graphene.String(),
                    vendor_by_name=graphene.String(),
                    price_gt=graphene.Decimal(),
                    price_lt=graphene.Decimal(),
                    category_by_name=graphene.String(),
                    order_by=graphene.String()
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
    def resolve_vehicle_by_offset_paginator(root, info, offset, limit):
        
        count = Vehicle.objects.count()                        
        vehicles = Vehicle.objects.all()[offset:offset+limit]                                     
        
        total = math.ceil(count / limit)

        has_next = False if offset >= (count - limit) else True            
        has_prev = False if offset == 0 else True
        
        return OffsetPagination(
            vehicles = vehicles,
            total_pages = total,            
            has_next = has_next,
            has_prev = has_prev
        )   

    def resolve_vehicle_filter(root, info, 
                    contains_name=None,
                    vendor_by_name=None,
                    price_gt=None,
                    price_lt=None,
                    category_by_name=None,
                    order_by=None            
                ):

        if contains_name:
            return Vehicle.objects.filter(name__contains=contains_name)

        elif vendor_by_name:
            return Vehicle.objects.filter(vendor__name=vendor_by_name)

        elif price_gt:
            return Vehicle.objects.filter(price__gt=price_gt)

        elif price_lt:
            return Vehicle.objects.filter(price__lt=price_lt)
        
        elif category_by_name:
            return Vehicle.objects.filter(category__name=category_by_name)  

        elif category_by_name and price_lt:
            return Vehicle.objects.filter(
                    Q(category__name=category_by_name) &
                    Q(price__lt=price_lt)
                )   

        elif order_by:
            return Vehicle.objects.all().order_by(order_by)

        elif vendor_by_name and order_by:
            return Vehicle.objects.filter(
                    vendor__name=vendor_by_name
                ).order_by(order_by)

        return Vehicle.objects.all()                    
