from dataclasses import dataclass

import requests
import xmltodict

from shipment_tracking import settings


@dataclass
class MedicineData:
    pic: str
    name: str
    description: str
    manufacturer: str


def _parse_xml_to_dict(xml_str, target_key, convert_to_snake_case):
    return xmltodict.parse(xml_str, )[target_key]


def _map_to_medicine(json_data: dict) -> MedicineData:
    return MedicineData(
        pic=json_data['pic'],
        name=json_data['name'],
        description=json_data['description'],
        manufacturer=json_data['manufacturer'],
    )


async def _make_ifap_request(uri, params):
    return _execute_http_post(
        url=f"{settings.IFAP_MEDICATION_SERVICE_BASE_URL}/{uri}",
        params=params
    )


def _execute_http_post(url: str, params: dict) -> str:
    response = requests.post(url=url, data=params)
    return response.text
