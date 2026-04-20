from rest_framework_nested import routers
from . import views

"""
URL Configuration for the 'Troca' API module.
Uses the DefaultRouter to automatically generate RESTful endpoints
for Customers and Transactions.
"""

router = routers.DefaultRouter()

# Endpoint: /troca/customers/
router.register("customers", views.CustomerViewSet, basename="customers")

# Endpoint: /troca/transactions/
router.register("transactions", views.TransactionViewSet, basename="transactions")

urlpatterns = router.urls
