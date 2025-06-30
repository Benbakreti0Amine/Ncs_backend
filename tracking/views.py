from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from orders.models import Order
from relay.models import RelayPoint
from core.models import Wilaya

# Create your views here.

class TrackOrderView(APIView):
    def get(self, request, tracking_id):
        try:
            order = Order.objects.get(tracking_id=tracking_id)
            relay = order.relay_point
            return Response({
                'status': order.status,
                'relay_point': {
                    'address': relay.address,
                    'wilaya': relay.wilaya.name,
                    'opening_hours': relay.opening_hours,
                    'contact_phone': relay.contact_phone,
                },
                'instructions': 'Show this QR or PIN at the relay point to collect your parcel.'
            })
        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=404)
