from graphene_django import DjangoObjectType
from stock.models import *

# Module to Map each django model to graphql type

class VendorType(DjangoObjectType):
    class Meta:
        model = Vendor
        fields = ("id", "name", "vehicles")       

class VehicleType(DjangoObjectType):
    class Meta:
        model = Vehicle
        fields = ("id", "name", "price", "launch_date", "vendor", "category")

class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ("id", "name")       