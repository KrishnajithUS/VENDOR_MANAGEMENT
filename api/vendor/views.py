from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from common.models import Vendor, PurchaseOrder, HistoricalPerformance
from .serializers import (
    VendorSerializer,
    PurchaseOrderSerializer,
    HistoricalPerformanceSerializer,
    VendorAcknowledgmentSerializer,
    VendorPerformanceMatrixSerializer,
)
from datetime import datetime


class VendorCrudView(viewsets.ModelViewSet):
    """
    A viewset for vendor crud operations
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = VendorSerializer
    queryset = Vendor.objects.all()

    @action(detail=True, methods=["get"])
    def performance(self, request, pk):
        try:
            po = Vendor.objects.get(pk=pk)
            serializer = VendorPerformanceMatrixSerializer(po)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Vendor.DoesNotExist:
            return Response(
                {"error": f"Vendor with vendor code {pk} does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class PurchaseOrderCrudView(viewsets.ModelViewSet):
    """
    A viewset for vendor crud operations
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PurchaseOrderSerializer
    queryset = PurchaseOrder.objects.all()

    def get_queryset(self):
        queryset = self.queryset
        vendor_id = self.request.query_params.get("vendor_id")
        if vendor_id:
            queryset = queryset.filter(vendor=vendor_id)
        return queryset

    @action(detail=True, methods=["post"])
    def acknowledge(self, request, pk):
        try:
            instance = PurchaseOrder.objects.get(pk=pk)
            serializer = VendorAcknowledgmentSerializer(
                data=request.data, instance=instance
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except PurchaseOrder.DoesNotExist:
            return Response(
                {
                    "error": f"Purchase order with  parchase order number {pk} does not exist"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
