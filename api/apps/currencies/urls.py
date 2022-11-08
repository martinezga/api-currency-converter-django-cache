from rest_framework.routers import SimpleRouter

from apps.currencies import views

router = SimpleRouter()
router.register(r'currencies', views.CurrencyView, basename="currency")

urlpatterns = router.urls
