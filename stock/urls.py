
from django.urls import path
from graphene_django.views import GraphQLView
from .graphql.backend import GraphQLCustomCoreBackend
from django.views.decorators.csrf import csrf_exempt
from . import views
from stock.graphql.schema import schema

urlpatterns = [    
    path('', views.index, name='index'),  
    path('graphql', GraphQLView.as_view(graphiql=True)),
    path('custom_graphql', views.CustomGraphQLView.as_view(), name='custom_graphql'),    
]