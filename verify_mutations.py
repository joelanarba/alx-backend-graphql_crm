import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alx_backend_graphql_crm.settings')
django.setup()

from django.test import RequestFactory
from graphene_django.views import GraphQLView

def run_query(query):
    factory = RequestFactory()
    request = factory.post('/graphql', data={'query': query}, content_type='application/json')
    view = GraphQLView.as_view(graphiql=False)
    response = view(request)
    return response.content.decode()

# 1. Create a single customer
mutation1 = '''
mutation {
  createCustomer(input: {
    name: "Alice",
    email: "alice@example.com",
    phone: "+1234567890"
  }) {
    customer {
      id
      name
      email
      phone
    }
    message
  }
}
'''
print("Mutation 1 (Create Customer):")
print(run_query(mutation1))

# 2. Bulk create customers
mutation2 = '''
mutation {
  bulkCreateCustomers(input: [
    { name: "Bob", email: "bob@example.com", phone: "123-456-7890" },
    { name: "Carol", email: "carol@example.com" }
  ]) {
    customers {
      id
      name
      email
    }
    errors
  }
}
'''
print("\nMutation 2 (Bulk Create Customers):")
print(run_query(mutation2))

# 3. Create a product
mutation3 = '''
mutation {
  createProduct(input: {
    name: "Laptop",
    price: "999.99",
    stock: 10
  }) {
    product {
      id
      name
      price
      stock
    }
  }
}
'''
print("\nMutation 3 (Create Product):")
print(run_query(mutation3))

# 4. Create an order with products
# We need IDs from previous steps. Assuming Alice is ID 1 and Laptop is ID 1 if DB was empty.
# In a real test we might query first, but since we just migrated, IDs should be 1.
mutation4 = '''
mutation {
  createOrder(input: {
    customerId: "1",
    productIds: ["1"]
  }) {
    order {
      id
      customer {
        name
      }
      products {
        name
        price
      }
      totalAmount
      orderDate
    }
  }
}
'''
print("\nMutation 4 (Create Order):")
print(run_query(mutation4))
