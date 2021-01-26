from django.shortcuts import render
from django.http import JsonResponse
from stock.graphql.schema import schema
from graphene_django.views import GraphQLView
from django.views.generic import View
from .graphql.backend import GraphQLCustomCoreBackend
from graphql import GraphQLCoreBackend
from graphene_subscriptions.consumers import GraphqlSubscriptionConsumer
import json

def index(request):
    return render(request, "index.html")

def clean_query(query):
    return query.replace("\n","")    

def get_graphql_result_from(request):    
    body_data = json.loads(request.body.decode("utf-8"))
    query = clean_query(body_data['query'])                
    result = schema.execute(query, context_value=request)                      
    result = result.data  
    return result

class CustomGraphQLView(GraphQLCustomCoreBackend, View):

    def __init__(self, executor=None):        
        super(GraphQLCustomCoreBackend, self).__init__(executor)
        self.execute_params['allow_subscriptions'] = True        

    def post(self, request):
        result = get_graphql_result_from(request)        
        return JsonResponse(result, safe=False)  




