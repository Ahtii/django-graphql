import graphene
from stock.models import *

'''
    Module to show all mutation operations
    on each model
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