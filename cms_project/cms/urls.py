from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter(trailing_slash=False)

# Read-only routes
router.register("districts", views.DistrictViewSet, basename="districts")

# Full CRUD routes
router.register("associations", views.AssociationViewSet, basename="associations")
router.register("association-images", views.AssociationImageViewSet, basename="association-images")
router.register("videos", views.VideoViewSet, basename="videos")
router.register("budgets", views.BudgetViewSet, basename="budgets")
router.register("extra-docs", views.ExtraDocViewSet, basename="extra-docs")
router.register("extra-images", views.ExtraImageViewSet, basename="extra-images")
router.register("images-tour", views.ImagesTourViewSet, basename="images-tour")
router.register("informations", views.InformationViewSet, basename="informations")
router.register("messages", views.MessageViewSet, basename="messages")
router.register("partners", views.PartnerViewSet, basename="partners")
router.register("posts", views.PostViewSet, basename="posts")
router.register("post-documents", views.PostDocumentViewSet, basename="post-documents")
router.register("post-files", views.PostFileViewSet, basename="post-files")
router.register("post-images", views.PostImageViewSet, basename="post-images")
router.register("post-videos", views.PostVideoViewSet, basename="post-videos")
router.register("roles", views.RoleViewSet, basename="roles")
router.register("sections", views.SectionViewSet, basename="sections")
router.register("secretaries", views.SecretaryViewSet, basename="secretaries")
router.register("secretary-sections", views.SecreatarySectionViewSet, basename="secretary-sections")
router.register("teams", views.TeamViewSet, basename="teams")
router.register("tours", views.TourViewSet, basename="tours")
router.register("year-goals", views.YearGoalsViewSet, basename="year-goals")
router.register("laws", views.LawViewSet, basename="laws")
urlpatterns = router.urls
