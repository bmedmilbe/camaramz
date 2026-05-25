from rest_framework_nested import routers
from . import views  # CustomersViewSet, OrdersViewSet, OrderItemsViewSet
from django.urls import path

router = routers.DefaultRouter()


router.register("email_reset", views.PasswordViewSet, basename="password")
router.register("reset_password_confirm", views.PasswordConfirmViewSet, basename="password_confirm")


# customers_router.register(r"parcels", views.ParcelsViewSet, basename="customer-parcels")
# customers_router.register(r"fligths", views.FligthsViewSet, basename="customer-fligths")


urlpatterns = (
    router.urls

    # + titles_router.urls
    # + sub_collection_router.urls
    # + shop_router.urls
)
# ) + [path('itemsinshop/<str:cart_id>/', views.get_product_in_shop)]


# router.register("customers", views.CustomersViewSet, basename='customers')


# /domain/ <- Domains list
# /domain/{pk}/ <- One domain, from {pk}
# /domain/{domain_pk}/nameservers/ <- Nameservers of domain from {domain_pk}
# /domain/{domain_pk}/nameservers/{pk} <- Specific nameserver from {pk}, of domain from {domain_pk}
