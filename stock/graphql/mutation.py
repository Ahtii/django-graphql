import graphene
from stock.graphql.types import *
from stock.models import *

'''
    Module to define all mutation operations
    on each model.
'''

# VENDOR MUTATION

class AddVendor(graphene.Mutation):

    class Arguments:
        name = graphene.String(required=True) 

    vendor = graphene.Field(VendorType) 

    @classmethod
    def mutate(cls, root, info, name):
        vendor = Vendor(name=name)
        vendor.save()
        return AddVendor(vendor=vendor) 

class EditVendor(graphene.Mutation):

    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String(required=True)

    vendor = graphene.Field(VendorType)

    @classmethod
    def mutate(cls, root, info, id, name):
        vendor = Vendor.objects.get(id=id)
        vendor.name = name
        vendor.save()
        return EditVendor(vendor=vendor)

class RemoveVendor(graphene.Mutation):

    class Arguments:
        id = graphene.ID(required=True)

    vendor = graphene.Field(VendorType)

    @classmethod
    def mutate(cls, root, info, id):
        vendor = Vendor.objects.get(id=id)        
        vendor.delete()
        return RemoveVendor(vendor=vendor)        

# CATEGORY MUTATION

class AddCategory(graphene.Mutation):

    class Arguments:
        name = graphene.String(required=True)

    category = graphene.Field(CategoryType)    

    @classmethod
    def mutate(cls, root, info, name):
        category = Category(name=name)
        category.save()
        return AddCategory(category=category)      

class EditCategory(graphene.Mutation):

    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String(required=True)

    category = graphene.Field(CategoryType)

    @classmethod
    def mutate(cls, root, info, id, name):
        category = Category.objects.get(id=id)
        category.name = name
        category.save()
        return EditCategory(category=category)

class RemoveCategory(graphene.Mutation):

    class Arguments:
        id = graphene.ID(required=True)

    category = graphene.Field(CategoryType)

    @classmethod
    def mutate(cls, root, info, id):
        category = Category.objects.get(id=id)        
        category.delete()
        return RemoveCategory(category=category)   


def get_vendor(vendor_id):
    return Vendor.objects.get(id=vendor_id)

def get_category(category_id):
    return Category.objects.get(id=category_id)    

# VEHICLE MUTATION

class AddVehicle(graphene.Mutation):

    class Arguments:
        name = graphene.String(required=True)
        price = graphene.Decimal(required=True)
        launch_date = graphene.Date(required=True)
        vendor = graphene.ID(required=True)
        category = graphene.ID(required=True)

    vehicle = graphene.Field(VehicleType) 

    @classmethod
    def mutate(cls, root, info, name, price, launch_date, vendor, category):

        vehicle = Vehicle(
                name=name,
                price=price,
                launch_date=launch_date,
                vendor=get_vendor(vendor),
                category=get_category(category)
            )
        vehicle.save()
        return AddVehicle(vehicle=vehicle)

class EditVehicle(graphene.Mutation):

    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String()
        price = graphene.Decimal()
        launch_date = graphene.Date()
        vendor = graphene.ID()
        category = graphene.ID()

    vehicle = graphene.Field(VehicleType)

    @classmethod
    def mutate(
            cls, root, info, 
            id, name=None, price=None, launch_date=None, 
            vendor=None, category=None
        ):
        
        vehicle = Vehicle.objects.get(id=id)
        
        if name is not None:
            vehicle.name = name
        
        if price is not None:
            vehicle.price = price

        if launch_date is not None:
            vehicle.launch_date = launch_date

        if vendor is not None:
            vehicle.vendor = get_vendor(vendor)

        if category is not None:
            vehicle.category = get_category(category)        
        
        vehicle.save()

        return EditVehicle(vehicle=vehicle)  

class RemoveVehicle(graphene.Mutation):

    class Arguments:
        id = graphene.ID(required=True)

    vehicle = graphene.Field(VehicleType)

    @classmethod
    def mutate(cls, root, info, id):
        vehicle = Vehicle.objects.get(id=id)        
        vehicle.delete()
        return RemoveVehicle(vehicle=vehicle)                