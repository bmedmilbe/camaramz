from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()

router.register("customers", views.CustomerViewSet,
                basename="customers")
router.register("transactions", views.TransactionViewSet,
                basename="transactions")

urlpatterns = router.urls
