from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from stock.graphql.schema import schema
import json

def index(request):
    return render(request, "index.html")

def clean_query(query):
    return query.replace("\n","")    

@csrf_exempt
def query_graphql(request):
    result = {}
    if request.method == 'POST':
        query = json.loads(request.body.decode("utf-8"))
        query = clean_query(query['query'])        
        result = schema.execute(query, context_value=request)                
    return JsonResponse(result.data)