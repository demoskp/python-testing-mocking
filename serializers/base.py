import json
from xml.etree import ElementTree


class BaseSerializer:
    def to_json(self, model, **kwargs):
        self.check_get_data_implemented()
        data = self.get_data(model, **kwargs)
        return json.dumps({"data": data})

    def to_xml(self, model, **kwargs):
        self.check_get_data_implemented()
        data = self.get_data(model, **kwargs)
        data_element = ElementTree.Element("data")
        for key, value in data.items():
            element = ElementTree.SubElement(data_element, key)
            element.text = str(value)

        return ElementTree.tostring(data_element, encoding="unicode")

    def check_get_data_implemented(self):
        if not hasattr(self, "get_data"):
            raise NotImplemented("Method get_data needs to be implemented")
