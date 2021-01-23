import graphene
from . import types, mutation
from django.db.models import Q 

'''
    Module to define the GraphQL Schema
'''

class Query(graphene.ObjectType):

    vehicles = graphene.List(VehicleType)
    vendors = graphene.List(VendorType)
    vendor_by_name = graphene.Field(VendorType, name=graphene.String(required=True))
    vehicle_by_category = graphene.List(VehicleType, category=graphene.String(required=True))        
    vehicle_by = graphene.List(VehicleType, 
                    name=graphene.String(required=True), 
                    category=graphene.String(required=True)
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
            return Vehicle.objects.filter(category__vehicle_type=category)
        except Vehicle.DoesNotExist:
            return None        

    def resolve_vehicle_by(root, info, name, category):
        try:
            return Vehicle.objects.filter(Q(category__vehicle_type=category) & Q(vendor__name=name))
        except Vehicle.DoesNotExist:
            return None        
   

class Mutation(graphene.ObjectType):

    add_vendor = AddVendor.Field()
    add_category = AddCategory.Field()
    add_vehicle = AddVehicle.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)  