import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alx_backend_graphql.settings')
django.setup()

from django.test import RequestFactory
from graphene_django.views import GraphQLView

def run_query(query):
    factory = RequestFactory()
    request = factory.post('/graphql', data={'query': query}, content_type='application/json')
    view = GraphQLView.as_view(graphiql=False)
    response = view(request)
    return response.content.decode()

# 1. Filter customers
# Note: createdAtGte format needed. YYYY-MM-DD usually works if configured, or ISO.
query1 = '''
query {
  allCustomers(name_Icontains: "Ali") {
    edges {
      node {
        id
        name
        email
        createdAt
      }
    }
  }
}
'''
# Note: Checkpoint used "nameIcontains" which implies camelCase conversion or specific naming.
# DjangoFilterConnectionField + FilterSet usually exposes `name_Icontains` (underscore) unless `camel_case=True` (default in some versions) or if we configured it.
# Graphene-Django often expects `name_Icontains` unless we manually specified fields with overrides.
# BUT, `django-filter` uses `lookup_expr`.
# Standard `django-filter` + graphene usually results in argument `name_Icontains` if field is `name` and lookup is `icontains`.
# However, the user prompt checkpoint says: `filter: { nameIcontains: "Ali" }`?
# OR `allCustomers(name_Icontains: "Ali")`?
# The prompt checkpoint: 
# `allCustomers(filter: { nameIcontains: "Ali", createdAtGte: "2025-01-01" })`
# This syntax `filter: { ... }` implies `DjangoFilterConnectionField` is defaulting to a helper input type OR the user Prompt is generic.
# `DjangoFilterConnectionField` behavior depends on version. Typically it lifts filters to top level args: `allCustomers(name_Icontains: "...")`.
# But newer `graphene-django` might support `filter` argument if specific settings are on.
# Given I used `DjangoFilterConnectionField(CustomerType)`, it usually flattens args.
# I will try flat args first `name_Icontains`. If user insisted on `filter: {}` object, I might need `graphene-django-filter` specific config or it's a documentation mismatch.
# Wait, `CustomerType` has `filterset_class`.
# Graphene-Django maps `name` filter to `name` argument. `lookup_expr='icontains'` might map to `name_Icontains` or just `name` if we named the filter `name`.
# In `filters.py`: `name = django_filters.CharFilter(lookup_expr='icontains')`. The filter name is `name`. So argument should be `name`.
# If I had `name__icontains` in fields list, it would generate `name_Icontains`. But I defined a class attribute `name`.
# So the argument is likely `name`.
# Let's try `allCustomers(name: "Ali")` which maps to `name` filter which does `icontains`.
# For `createdAt`: Checkpoint says `createdAtGte`. My filter is `created_at = DateFromToRangeFilter`.
# `DateFromToRangeFilter` usually creates `created_at_after` and `created_at_before` args.
# Or `createdAt_Gte` if camelCase.
# I will try to inspect the schema or just guess.
# Let's try to query introspection to be sure, or just run a simple query first.

print("Query 1 (Customers - Name Ali):")
print(run_query(query1))

# Let's try the Checkpoint style if my assumption fails.
query1_checkpoint = '''
query {
  allCustomers(name: "Ali") {
    edges {
      node {
        name
      }
    }
  }
}
'''
print("Query 1b (Customers - Name Ali - Flat):")
print(run_query(query1_checkpoint))

# 2. Products
query2 = '''
query {
  allProducts(price_Gte: 100) {
    edges {
      node {
        name
        price
      }
    }
  }
}
'''
print("\nQuery 2 (Products - Price >= 100):")
print(run_query(query2))

# 3. Orders
query3 = '''
query {
  allOrders(customerName: "Alice") {
    edges {
      node {
        totalAmount
        customer { name }
      }
    }
  }
}
'''
print("\nQuery 3 (Orders - Customer Name 'Alice'):")
print(run_query(query3))
