
from django.urls import path
from graphene_django.views import GraphQLView
from .graphql.backend import GraphQLCustomCoreBackend
from django.views.decorators.csrf import csrf_exempt
from . import views
from stock.graphql.schema import schema

urlpatterns = [    
    path('', views.index, name='index'),  
    path('graphql', GraphQLView.as_view(graphiql=True)),
    #path('query', views.query_graphql, name='query')  
    #path('query', CustomGraphQLView.as_view(), name="query")
    path('custom_graphql', views.CustomGraphQLView.as_view(), name='custom_graphql'),
    #path('custom_graphql', csrf_exempt(GraphQLView.as_view(graphiql=True, backend=GraphQLCustomCoreBackend())), name='custom_graphql'),
]