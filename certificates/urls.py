"""URL routing configuration for the certificates application.

Configures REST API endpoints for certificate-related resources including
customers, locations, certificates, persons, and related entities.
Uses nested routers to support hierarchical API routes.
"""

from rest_framework_nested import routers
from . import views
from django.urls import path

# Initialize the base router
router = routers.DefaultRouter(trailing_slash=False)

# Register all base API endpoints
router.register("countries", views.CountrysViewSet, basename="countries")
router.register("universities", views.UniversitysViewSet, basename="universities")
router.register("customers", views.CustomerViewSet, basename="customers")
router.register("ifens", views.IfenViewSet, basename="ifens")
router.register("buildings", views.BiuldingTypeViewSet, basename="buildings")
router.register("cemiterios", views.CemiteriosViewSet, basename="cemiterios")
router.register("streets", views.StreetsViewSet, basename="streets")
router.register("changes", views.ChangesViewSet, basename="changes")
router.register("towns", views.TownViewSet, basename="towns")
router.register("countys", views.CountysViewSet, basename="countys")
router.register("titles", views.CertificateTitleViewSet, basename="title")
router.register("certificates", views.CertificateViewSet, basename="certificates")
router.register("certificatescomment", views.CertificateCommentViewSet, basename="certificatescomment")
router.register("persons", views.PersonViewSet, basename="persons")
router.register("birthadddress", views.PersonBirthAddressViewSet, basename="birthadddress")
router.register("house", views.HouseViewSet, basename="house")
router.register("covals", views.CovalsViewSet, basename="covals")
router.register("covalsetup", views.CovalSetUpViewSet, basename="covalsetup")
router.register("parents", views.ParentViewSet, basename="parents")
router.register("idtypes", views.IdTypeViewSet, basename="idtypes")
router.register("intituitions", views.InstituitionsViewSet, basename="intituitions")
router.register("metadata", views.MetadataViewSet, basename="metadata")

# Initialize nested router for title-related resources
titles_router = routers.NestedSimpleRouter(router, r"titles", lookup="title", trailing_slash=False)

# Register nested endpoints under titles resource
titles_router.register(r"model", views.CertificateModelViewSet, basename="title-models")
titles_router.register(r"person", views.CertificatePersonsViewSet, basename="title-persons")
titles_router.register(r"singleperson", views.CertificateSinglePersonsViewSet, basename="title-singlepersons")
titles_router.register(r"parent", views.CertificateSimpleParentsViewSet, basename="title-parents")
titles_router.register(r"date", views.CertificateDatesViewSet, basename="title-dates")

# Combine base and nested router URLs
urlpatterns = router.urls + titles_router.urls
