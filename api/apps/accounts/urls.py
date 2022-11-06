from rest_framework.routers import SimpleRouter

from apps.accounts import views

router = SimpleRouter()
router.register(r'', views.AuthView, basename="auth")

urlpatterns = router.urls
