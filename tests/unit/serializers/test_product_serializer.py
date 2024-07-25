import json
import unittest
from unittest.mock import Mock

from models.product import Product
from serializers.product import ProductSerializer


class TestProductSerializer(unittest.TestCase):
    def setUp(self):
        self.product = Product(
            name="Product 1",
            description="Product 1 description",
            price=10
        )
        fx_rate = 1.2
        self.converted_price = self.product.price * fx_rate
        mock_current = Mock(return_value=fx_rate)
        fx_rate_service = Mock(current=mock_current)
        self.serializer = ProductSerializer(fx_rate_service=fx_rate_service)

    def test_serialize_to_json(self):
        data = self.serializer.to_json(self.product, to_currency="EUR")
        expected = json.dumps({
            "data": {
                "name": self.product.name,
                "description": self.product.description,
                "price": self.converted_price,
            }
        })

        assert data == expected

    def test_serialize_to_xml(self):
        data = self.serializer.to_xml(self.product, to_currency="GBP")
        expected = (
            "<data>"
            f"<name>{self.product.name}</name>"
            f"<description>{self.product.description}</description>"
            f"<price>{self.converted_price}</price>"
            "</data>"
        )

        assert data == expected


if __name__ == '__main__':
    unittest.main()
