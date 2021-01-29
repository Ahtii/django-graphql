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

# class VendorInput(graphene.InputObjectType):
#     name = graphene.String(required=True)

# class AddVendor(graphene.Mutation):

#     class Arguments:
#         #name = graphene.String(required=True) 
#         vendor_data = VendorInput(required=True)

#     vendor = graphene.Field(Vendor) 

#     #@classmethod
#     def mutate(cls, root, info, vendor_data=None):
#         # vendor = Vendor(name=name)
#         # vendor.save()
#         vendor = Vendor(
#             name = vendor_data.name
#         )
#         return AddVendor(vendor=vendor) 

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


def get_vendor(vendor):
    return Vendor.objects.get(name=vendor)

def get_category(category):
    return Category.objects.get(name=category)    

# VEHICLE MUTATION

class AddVehicle(graphene.Mutation):

    class Arguments:
        name = graphene.String(required=True)
        price = graphene.Decimal(required=True)
        launch_date = graphene.Date(required=True)
        vendor = graphene.String(required=True)
        category = graphene.String(required=True)

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
        vendor = graphene.String()
        category = graphene.String()

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

class BaseMutation(graphene.ObjectType):

    add_vendor = AddVendor.Field()
    edit_vendor = EditVendor.Field()
    remove_vendor = RemoveVendor.Field()

    add_category = AddCategory.Field()
    edit_category = EditCategory.Field()
    remove_category = RemoveCategory.Field()

    add_vehicle = AddVehicle.Field()
    edit_vehicle = EditVehicle.Field()
    remove_vehicle = RemoveVehicle.Field()        