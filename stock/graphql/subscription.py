import graphene
from rx import Observable
from stock.models import Vendor
from .types import *
from graphene_subscriptions.events import CREATED, DELETED, UPDATED

class BaseSubscriptions(graphene.ObjectType):
    
    vendor_updated = graphene.Field(VendorType)    
    vendor_deleted = graphene.Field(VendorType)

    category_updated = graphene.Field(CategoryType)    
    category_deleted = graphene.Field(CategoryType)

    vehicle_updated = graphene.Field(VehicleType)    
    vehicle_deleted = graphene.Field(VehicleType)
    
    def resolve_vendor_updated(root, info):  
        # print("root in updated")
        # print(info.context)
        return root.filter(
            lambda event:
                (event.operation == CREATED or event.operation == UPDATED) and
                isinstance(event.instance, Vendor)
        ).map(lambda event: event.instance) 

    def resolve_vendor_deleted(root, info):  
        print("root in deleted")
        print(info.context)
        return root.filter(
            lambda event:
                event.operation == DELETED and
                isinstance(event.instance, Vendor)
        ).map(lambda event: event.instance)        


    def resolve_category_updated(root, info):  
        return root.filter(
            lambda event:
                (event.operation == CREATED or event.operation == UPDATED) and
                isinstance(event.instance, Category)
        ).map(lambda event: event.instance) 

    def resolve_category_deleted(root, info):  
        return root.filter(
            lambda event:
                event.operation == DELETED and
                isinstance(event.instance, Category)
        ).map(lambda event: event.instance)        


    def resolve_vehicle_updated(root, info):  
        return root.filter(
            lambda event:
                (event.operation == CREATED or event.operation == UPDATED) and
                isinstance(event.instance, Vehicle)
        ).map(lambda event: event.instance) 

    def resolve_vehicle_deleted(root, info):  
        return root.filter(
            lambda event:
                event.operation == DELETED and
                isinstance(event.instance, Vehicle)
        ).map(lambda event: event.instance)                