import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alx_backend_graphql.settings')
django.setup()

from django.test import RequestFactory
from graphene_django.views import GraphQLView

query = '''
{
  hello
}
'''

factory = RequestFactory()
request = factory.post('/graphql', data={'query': query}, content_type='application/json')
view = GraphQLView.as_view(graphiql=False)
response = view(request)
print(response.content.decode())
