import graphene
from stock.graphql.types import *
from django.db.models import Q


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
    vehicle_by_pagination = graphene.List(VehicleType,
                        first=graphene.Int(),
                        last=graphene.Int(),
                        offset=graphene.Int()                                              
                    )                                   

    # has_next = graphene.Boolean(VehicleType)
    # has_prev = graphene.Boolean(VehicleType)
    # num_of_pages = graphene.Int(VehicleType)                                          

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
    def resolve_vehicle_by_pagination(root, info, first=None, last=None, offset=None):

        if first and offset:                
            return Vehicle.objects.all()[first:first+offset]
        
        if first:                
            return Vehicle.objects.all()[:first]

        vehicles = Vehicle.objects.all()

        if last:            
            return vehicles[len(vehicles)-last:]          

        return vehicles    

    # def resolve_has_next(root, info):

    #     return Vehicle.objects.all()[first:first+offset]         
