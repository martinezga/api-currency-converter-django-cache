from rest_framework.routers import SimpleRouter

from apps.home import views

router = SimpleRouter()
router.register(r'', views.HomeView, basename="home")

urlpatterns = router.urls
