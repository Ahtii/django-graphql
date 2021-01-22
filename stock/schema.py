import graphene
from graphene_django import DjangoObjectType
from .models import Vehicle, Vendor, Category

# interface between vendor django object with graphql object
class VendorType(DjangoObjectType):
    class Meta:
        model = Vendor
        fields = ("id", "name", "vehicles")       

# interface between vehicle django object with graphql object
class VehicleType(DjangoObjectType):
    class Meta:
        model = Vehicle
        fields = ("id","name", "price", "launch_date", "vendor", "category")

# define the structure of graphql query
class Query(graphene.ObjectType):

    vehicles = graphene.List(VehicleType)
    vendors = graphene.List(VendorType)
    vendor_by_name = graphene.Field(VendorType, name=graphene.String(required=True))
    vehicle_by_category = graphene.List(VehicleType, category=graphene.String(required=True))

    # get all vehicles present in the stock
    def resolve_vehicles(root, info):
        return Vehicle.objects.select_related("vendor").all()

    # get all vendors
    def resolve_vendors(root, info):
        return Vendor.objects.prefetch_related("vehicles").all()    
    
    # get vehicle vendor by name
    def resolve_vendor_by_name(root, info, name):
        try:
            return Vendor.objects.get(name=name)    
        except Vendor.DoesNotExist:
            return None

    # get vehicle by category
    def resolve_vehicle_by_category(root, info, category):
        try:
            return Vehicle.objects.filter(category__vehicle_type=category)
        except Vehicle.DoesNotExist:
            return None        

schema = graphene.Schema(query=Query)    