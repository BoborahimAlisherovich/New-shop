from .views import HomeView,ShopDetailView,ContactView,ShopView,page_turt_view

from django.urls import path

urlpatterns = [
    path('', HomeView.as_view(), name="home-page"),
    path('shop/<slug:slug>/', ShopDetailView.as_view(),name="detail-page"),
    path('shop/',ShopView.as_view(), name="shop-page"),
    path("contact/",ContactView.as_view(),name="contact-page"),
    path("^<path:path>/",page_turt_view,name="404-page")
]