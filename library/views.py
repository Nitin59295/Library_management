from rest_framework import generics, status, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db import transaction
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from .models import Book, Cart, CartItem, Order, OrderItem, Wishlist
from .serializers import BookSerializer, CartSerializer, OrderSerializer, WishlistSerializer
from .permissions import IsLibrarian



class BookManageView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated, IsLibrarian]

class BookDetailManageView(generics.DestroyAPIView):

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated, IsLibrarian]

class BookReportView(generics.ListAPIView):

    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated, IsLibrarian]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['author']
    ordering_fields = ['issue_count', 'author', 'title'] # 'most issued' and 'least issued'

    def get_queryset(self):
        return Book.objects.annotate(issue_count=Count('orderitem')).order_by('-issue_count')


class BookBrowseView(generics.ListAPIView):

    serializer_class = BookSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['author']
    ordering_fields = ['issue_count', 'author', 'title']

    def get_queryset(self):
        return Book.objects.annotate(issue_count=Count('orderitem')).order_by('-issue_count')

class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    def post(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        book_id = request.data.get('book_id')
        quantity = int(request.data.get('quantity', 1))
        
        try:
            book = Book.objects.get(id=book_id)
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart, book=book, defaults={'quantity': quantity}
            )
            if not created:
                cart_item.quantity += quantity
                cart_item.save()
            return Response(CartSerializer(cart).data, status=status.HTTP_201_CREATED)
        except Book.DoesNotExist:
            return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)

class CheckoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        cart = Cart.objects.filter(user=request.user).first()
        if not cart or not cart.items.exists():
            return Response({"error": "Cart is empty."}, status=status.HTTP_400_BAD_REQUEST)

        total_price = sum(item.book.price * item.quantity for item in cart.items.all())

        with transaction.atomic():
            order = Order.objects.create(user=request.user, total_price=total_price)
            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order, book=item.book, quantity=item.quantity, price_at_purchase=item.book.price
                )
            cart.items.all().delete()

        serializer = OrderSerializer(order)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class WishlistView(generics.ListCreateAPIView):

    serializer_class = WishlistSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class WishlistDetailView(generics.DestroyAPIView):

    serializer_class = WishlistSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user)
