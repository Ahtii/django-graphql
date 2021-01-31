from graphene_django import DjangoObjectType
from stock.models import *
import graphene

# For relay pagination
from graphene import relay

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


# Relay Pagination Type

class VehicleNode(DjangoObjectType):
    class Meta:
        model = Vehicle
        filter_fields = ['vendor', 'category']
        interfaces = (relay.Node, )

class VendorNode(DjangoObjectType):
    class Meta:
        model = Vendor
        filter_fields = {'name': ['istartswith']}
        interfaces = (relay.Node, )        


class VehiclePaginatorType(DjangoObjectType):

    class Meta:
        model = Vehicle
        fields = ('__all__')

    has_next = graphene.Boolean()
    has_prev = graphene.Boolean()              