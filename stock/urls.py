
from django.urls import path
from graphene_django.views import GraphQLView
from . import views
from stock.graphql.schema import schema

urlpatterns = [    
    path('', views.index, name='index'),  
    path('graphql', GraphQLView.as_view(graphiql=True)),
    path('query', views.query_graphql, name='query')
]