from rest_framework.routers import SimpleRouter

from api.apps.home import views

router = SimpleRouter()
router.register(r'', views.HomeView, basename="home")

urlpatterns = router.urls
