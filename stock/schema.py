import graphene
from graphene_django import DjangoObjectType
from .models import Vehicle, Vendor, Category
from django.db.models import Q

# Map Vendor django model to graphql Vendor type
class VendorType(DjangoObjectType):
    class Meta:
        model = Vendor
        fields = ("id", "name", "vehicles")       

# Map Vendor django model to graphql Vendor type
class VehicleType(DjangoObjectType):
    class Meta:
        model = Vehicle
        fields = ("id","name", "price", "launch_date", "vendor", "category")

# Map Category django model to graphql Category type
class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ("id", "name")        

# Define the root node structure as Query
class Query(graphene.ObjectType):

    vehicles = graphene.List(VehicleType)
    vendors = graphene.List(VendorType)
    vendor_by_name = graphene.Field(VendorType, name=graphene.String(required=True))
    vehicle_by_category = graphene.List(VehicleType, category=graphene.String(required=True))        
    vehicle_by = graphene.List(VehicleType, 
                    name=graphene.String(required=True), 
                    category=graphene.String(required=True)
                )

    # Get all vehicles present in the stock
    def resolve_vehicles(root, info):
        return Vehicle.objects.select_related("vendor").all()

    # Get all vendors
    def resolve_vendors(root, info):
        return Vendor.objects.prefetch_related("vehicles").all()    
    
    # Get vehicle vendor by name
    def resolve_vendor_by_name(root, info, name):
        try:
            return Vendor.objects.get(name=name)    
        except Vendor.DoesNotExist:
            return None

    # Get vehicle by category
    def resolve_vehicle_by_category(root, info, category):
        try:
            return Vehicle.objects.filter(category__vehicle_type=category)
        except Vehicle.DoesNotExist:
            return None        

    # Get vehicle by vendor name and category
    def resolve_vehicle_by(root, info, name, category):
        try:
            return Vehicle.objects.filter(Q(category__vehicle_type=category) & Q(vendor__name=name))
        except Vehicle.DoesNotExist:
            return None        

class AddVendor(graphene.Mutation):

    class Arguments:
        name = graphene.String(required=True) 

    vendor = graphene.Field(VendorType) 

    @classmethod
    def mutate(cls, root, info, name):
        vendor = Vendor(name=name)
        vendor.save()
        return AddVendor(vendor=vendor) 

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

# Define the root node as Mutation
class Mutation(graphene.ObjectType):

    add_vendor = AddVendor.Field()

    add_category = AddCategory.Field()

    add_vehicle = AddVehicle.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)  