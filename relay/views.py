from rest_framework import viewsets, permissions
from rest_framework.generics import CreateAPIView
from .models import RelayPoint
from .serializers import RelayPointSerializer, RelayOperatorRegisterSerializer
from orders.models import Order
from orders.serializers import OrderSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

# Create your views here.

class RelayPointViewSet(viewsets.ModelViewSet):
    queryset = RelayPoint.objects.all()
    serializer_class = RelayPointSerializer
    permission_classes = [permissions.IsAdminUser]
    
    #te3 admin hadiiii

class RelayOperatorRegisterView(CreateAPIView):
    serializer_class = RelayOperatorRegisterSerializer

class RelayParcelViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        try:
            relay_point = RelayPoint.objects.get(operator=self.request.user)
            return Order.objects.filter(relay_point=relay_point)
        except RelayPoint.DoesNotExist:
            return Order.objects.none()

class RelayProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        try:
            relay_point = RelayPoint.objects.get(operator=user)
            return Response({
                'address': relay_point.address,
                'wilaya': relay_point.wilaya.name,
                'opening_hours': relay_point.opening_hours,
                'contact_phone': relay_point.contact_phone,
                'status': relay_point.status,
            })
        except RelayPoint.DoesNotExist:
            return Response({'error': 'Relay point not found'}, status=404)

class RelayEarningsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        try:
            relay_point = RelayPoint.objects.get(operator=user)
            return Response({'earnings': relay_point.earnings})
        except RelayPoint.DoesNotExist:
            return Response({'error': 'Relay point not found'}, status=404)
