from django.urls import path
from .views import (ProductsApi,
                    ProductDetailApi,
                    CartItemApi,
                    CartApi,
                    DeleteItemApi,
                    UpdateCartItemApi)


app_name = "magazine"
urlpatterns = [
    path("api/products/", ProductsApi.as_view(), name="products"),
    path("api/products/<int:pk>/", ProductDetailApi.as_view(), name="product"),
    path("api/cart/<int:pk>/", CartItemApi.as_view(), name="cart-item"),
    path("api/cart/", CartApi.as_view(), name='my-cart'),
    path("api/cart/delete/<int:pk>/", DeleteItemApi.as_view(),name="delete-item"),
    path("api/cart/update/<int:pk>/", UpdateCartItemApi.as_view(), name="update-item")
]
