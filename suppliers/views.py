from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from .models import Supplier
from .permissions import IsActiveEmployee
from .serializers import SupplierSerializer


class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [IsActiveEmployee]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["contacts__country"]
    search_fields = ["contacts__city"]

    def get_serializer(self, *args, **kwargs):
        if self.action in ["update", "partial_update"]:
            data = self.request.data.copy()
            data.pop("debt", None)
        return super().get_serializer(*args, **kwargs)
