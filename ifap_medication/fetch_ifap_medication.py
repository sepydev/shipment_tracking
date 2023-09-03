from dataclasses import dataclass

import requests
import xmltodict

from shipment_tracking import settings


@dataclass
class MedicineData:
    pic: int
    name: str
    description: str
    manufacturer_name: str


def _convert_dict_keys_to_snake_case(value: dict) -> dict:
    return {k.replace('-', '_'): v for k, v in value.items()}


def _parse_xml_to_dict(xml_str: str, target_key: str, convert_to_snake_case: bool) -> dict:
    result = xmltodict.parse(xml_str, )[target_key]
    if convert_to_snake_case:
        result = _convert_dict_keys_to_snake_case(result)
    return result


def _map_to_medicine(json_data: dict) -> MedicineData:
    return MedicineData(
        pic=int(json_data['pic']),
        name=json_data['name'],
        description=json_data['description'],
        manufacturer_name=json_data['manufacturer_name'],
    )


async def _make_ifap_request(uri: str, params: dict) -> str:
    return _execute_http_post(
        url=f"{settings.IFAP_MEDICATION_SERVICE_BASE_URL}/{uri}",
        params=params
    )


def _execute_http_post(url: str, params: dict) -> str:
    response = requests.post(url=url, data=params)
    return response.text
