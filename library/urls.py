from django.urls import path
from .views import (
    BookManageView,
    BookDetailManageView,
    BookReportView,
    BookBrowseView,
    CartView,
    CheckoutView,
    WishlistView,
    WishlistDetailView
)

urlpatterns = [
    # Librarian endpoints
    path('librarian/books/', BookManageView.as_view(), name='librarian-book-list-create'),
    path('librarian/books/<int:pk>/', BookDetailManageView.as_view(), name='librarian-book-detail'),
    path('librarian/report/', BookReportView.as_view(), name='librarian-book-report'),

    # Customer endpoints
    path('books/', BookBrowseView.as_view(), name='customer-book-browse'),
    path('cart/', CartView.as_view(), name='customer-cart-view'),
    path('checkout/', CheckoutView.as_view(), name='customer-checkout'),
    path('wishlist/', WishlistView.as_view(), name='customer-wishlist-list-create'),
    path('wishlist/<int:pk>/', WishlistDetailView.as_view(), name='customer-wishlist-detail'),
]