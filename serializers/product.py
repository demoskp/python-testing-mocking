from models.product import Product
from serializers.base import BaseSerializer
from services.currency import FXRateService


class ProductSerializerException(Exception):
    pass


class ProductSerializer(BaseSerializer):
    def __init__(self, fx_rate_service: FXRateService):
        self._fx_rate_service = fx_rate_service

    def get_data(self, model: Product, **kwargs):
        return {
            "name": model.name,
            "description": model.description,
            "price": self._fx_rate_service.current("USD", kwargs.get("to_currency")) * model.price
        }

    def to_json(self, model, **kwargs):
        to_currency = kwargs.get("to_currency")

        if not to_currency:
            raise ProductSerializerException("to_currency is required for this serializer")

        return super().to_json(model, to_currency=to_currency)

    def to_xml(self, model, **kwargs):
        to_currency = kwargs.get("to_currency")

        if not to_currency:
            raise ProductSerializerException("to_currency is required for this serializer")

        return super().to_xml(model, to_currency=to_currency)
