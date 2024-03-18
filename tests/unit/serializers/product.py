import unittest
from unittest.mock import MagicMock

from models.product import Product
from serializers.product import ProductSerializer


class TestProductSerializer(unittest.TestCase):
    def test_serialize_to_json(self):
        product = Product(name="Product 1", description="A very detailed description", price=10)
        fx_rate = 1.2
        converted_price = product.price * fx_rate
        mock_current = MagicMock(return_value=fx_rate)
        fx_rate_service = MagicMock(current=mock_current)
        serializer = ProductSerializer(fx_rate_service=fx_rate_service)

        data = serializer.to_json(product, to_currency="EUR")
        expected = (
                '{"data": {"name": "'
                + product.name
                + '", "description": "'
                + product.description
                + '", "price": '
                + str(converted_price)
                + '}}'
        )

        assert data == expected

    def test_serialize_to_xml(self):
        product = Product(name="Product 1", description="A very detailed description", price=10)
        fx_rate = 1.2
        converted_price = product.price * fx_rate
        mock_current = MagicMock(return_value=fx_rate)
        fx_rate_service = MagicMock(current=mock_current)
        serializer = ProductSerializer(fx_rate_service=fx_rate_service)

        data = serializer.to_xml(product, to_currency="EUR")

        expected = (
            "<data>"
            f"<name>{product.name}</name>"
            f"<description>{product.description}</description>"
            f"<price>{converted_price}</price>"
            "</data>"
        )
        assert data == expected
