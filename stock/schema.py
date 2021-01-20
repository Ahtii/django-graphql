import graphene
from graphene_django import DjangoObjectType
from .models import Vehicle, Vendor

class VendorType(DjangoObjectType):
    class Meta:
        model = Vendor
        fields = ("id", "name", "vehicles")       

class VehicleType(DjangoObjectType):
    class Meta:
        model = Vehicle
        fields = ("id","name", "price", "launch_date", "vendor")

class Query(graphene.ObjectType):

    all_vehicles = graphene.List(VehicleType)
    vendor_by_name = graphene.Field(VendorType, name=graphene.String(required=True))

    def resolve_all_vehicles(root, info):
        return Vehicle.objects.select_related("vendor").all()

    def resolve_vendor_by_name(root, info, name):
        try:
            return Vendor.objects.get(name=name)    
        except Vendor.DoesNotExist:
            return None    

schema = graphene.Schema(query=Query)    