import graphene
from graphene_django import DjangoObjectType
from .models import Vehicle

class VehicleType(DjangoObjectType):
    class Meta:
        model = Vehicle
        fields = ("id","name", "price", "launch_date")


class Query(graphene.ObjectType):

    all_vehicles = graphene.List(VehicleType) 

    def resolve_all_vehicles(root, info):
        return Vehicle.objects.all()


schema = graphene.Schema(query=Query)    