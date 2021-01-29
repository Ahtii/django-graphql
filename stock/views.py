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
    # result = {}
    # if request.method == 'POST':
    body_data = json.loads(request.body.decode("utf-8"))
    query = clean_query(body_data['query'])   
    variables = body_data.get('variables')
    print("variables: ")
    print(variables)
    print("query: ")
    print(query)   
    result = schema.execute(query, variables=variables, context_value=request, allow_subscriptions=True)
    print(result)  
    result = result.data            
    return result

# def query_graphql(request):
#     result = get_graphql_result_from(request)        
#     return JsonResponse(result, safe=False) 

class CustomGraphQLView(GraphQLCustomCoreBackend, View):

    def __init__(self, executor=None):
        # type: (Optional[Any]) -> None
        super(GraphQLCustomCoreBackend, self).__init__(executor)
        self.execute_params['allow_subscriptions'] = True        
# class CustomGraphQLView(GraphQLView, View):    

#     def __init__(self, executor=None):
#         # type: (Optional[Any]) -> None        
#         super(GraphQLView, self).__init__()
#         self.graphiql = False        
    
    def post(self, request):
        result = get_graphql_result_from(request)
        # result = None
        # data = self.parse_body(request)
        # print(data)
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




