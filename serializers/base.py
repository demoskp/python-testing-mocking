import json
from xml.etree import ElementTree


class BaseSerializer:
    def to_json(self, model, **kwargs):
        data = self.get_data(model, **kwargs)
        return json.dumps({"data": data})

    def to_xml(self, model, **kwargs):
        data = self.get_data(model, **kwargs)
        data_element = ElementTree.Element("data")
        for key, value in data.items():
            element = ElementTree.SubElement(data_element, key)
            element.text = str(value)

        return ElementTree.tostring(data_element, encoding="unicode")

    def get_data(self, *args, **kwargs):
        raise NotImplemented("This method should be overridden")
