import graphene
from stock.graphql.types import *
from stock.graphql.mutation import *
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
    edit_vendor = EditVendor.Field()
    remove_vendor = RemoveVendor.Field()

    add_category = AddCategory.Field()
    edit_category = EditCategory.Field()
    remove_category = RemoveCategory.Field()

    add_vehicle = AddVehicle.Field()
    edit_vehicle = EditVehicle.Field()
    remove_vehicle = RemoveVehicle.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)  