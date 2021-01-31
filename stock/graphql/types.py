from graphene_django import DjangoObjectType
from stock.models import *
import graphene

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

class VehiclePaginatorType(DjangoObjectType):

    class Meta:
        model = Vehicle
        fields = ('__all__')

    has_next = graphene.Boolean()
    has_prev = graphene.Boolean()              