import graphene
from rx import Observable
from stock.models import Vendor
from .types import VendorType
from graphene_subscriptions.events import CREATED

class MySubscription(graphene.ObjectType):
    hello = graphene.String()

    def resolve_hello(root, info):
        return Observable.interval(3000).map(lambda i: "hello world!")

class VendorSubscription(graphene.ObjectType):
    
    vendor_created = graphene.Field(VendorType)

    @classmethod
    def resolve_vendor_created(cls, root, info):  
        print(root.filter(lambda event: event.operation == CREATED).map(lambda i: "got created :D"))              
        return root.filter(
            lambda event:
                event.operation == CREATED and
                isinstance(event.instance, Vendor)
        ).map(lambda event: event.instance)