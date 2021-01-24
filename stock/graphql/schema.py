import graphene
from stock.graphql.mutation import BaseMutation
from stock.graphql.query import BaseQuery
from stock.graphql.subscription import BaseSubscriptions
from django.db.models import Q 

'''
    Module to define the GraphQL Schema
'''

class Query(BaseQuery):
    pass     
   
class Mutation(BaseMutation):   
    pass 

class Subscription(BaseSubscriptions):
    pass    

schema = graphene.Schema(
    query=Query, 
    mutation=Mutation,
    subscription=Subscription
)  