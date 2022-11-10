from rest_framework.routers import SimpleRouter

from apps.exchanges import views

router = SimpleRouter()
router.register(r'rates', views.ExchangeRateView, basename="exchange-rates")
router.register(r'convert', views.ConverterView, basename="convert")

urlpatterns = router.urls
