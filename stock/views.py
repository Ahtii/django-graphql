from django.shortcuts import render
from django.http import JsonResponse
from stock.graphql.schema import schema
from graphene_django.views import GraphQLView
import json

def index(request):
    return render(request, "index.html")

def clean_query(query):
    return query.replace("\n","")    

def get_graphql_result_from(request):
    result = {}
    if request.method == 'POST':
        body_data = json.loads(request.body.decode("utf-8"))
        query = clean_query(body_data['query'])                
        result = schema.execute(query, context_value=request, allow_subscriptions=True)              
        print(result)
        print(result.data)
        result = result.data  
    return result

def query_graphql(request):
    result = get_graphql_result_from(request)        
    return JsonResponse(result)

def subscription_graphql(request):    
    result = get_graphql_result_from(request)        
    return JsonResponse(result, safe=False)    

# class Subscribe(GraphQLView):
    
    # def __init__(self):
    #     super(graphiql=False, **kwargs).__init__()
    # def __init__(self):
    #     super().__init__()
        
    # def post(self, request, *args, **kwargs):
    #     print(request.body)
    #     super().parse_body(self, request)
    #     result = super().execute_graphql_request(
    #         self, request=request, query=query
    #     )
    #     print(result)
        #result = {}get_graphql_result_from("subscription", request)
        # return JsonResponse(result)  




