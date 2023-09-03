import pytest
import responses

from ifap_medication.fetch_ifap_medication import MedicineData, _parse_xml_to_dict, _map_to_medicine, \
    _make_ifap_request, _execute_http_post
from rest_framework import status


@pytest.fixture
def settings():
    class Settings:
        IFAP_MEDICATION_SERVICE_BASE_URL = 'http://localhost:8001'

    return Settings()


@responses.activate
def test_execute_http_post_success(settings):
    ifap_url = f"{settings.IFAP_MEDICATION_SERVICE_BASE_URL}/test"
    responses.add(
        responses.POST,
        ifap_url,
        body='SUCCESS',
        status=200
    )
    response = _execute_http_post(url=ifap_url, params={'id': 1})
    assert response == 'SUCCESS'


async def fetch_ifap_medication_by_pic(pic: int) -> MedicineData:
    assert type(pic) == int
    xml_str = await _make_ifap_request(
        uri="ifapGetMedicineByPICV2",
        params={
            "Search": pic,
        }
    )
    json_data = _parse_xml_to_dict(xml_str, target_key='medicine_v2', convert_to_snake_case=True)
    return _map_to_medicine(json_data)


@pytest.mark.asyncio
@responses.activate
async def test_fetch_ifap_medication_by_pic_success(settings):
    ifap_url = f"{settings.IFAP_MEDICATION_SERVICE_BASE_URL}/ifapGetMedicineByPICV2"
    responses.add(
        responses.POST,
        ifap_url,
        body="""
        <medicine_v2>
                <pic>123456</pic>
                <name>Test</name>
                <description>Test</description>
                <manufacturer>Test</manufacturer>
        </medicine_v2>
        """,
        status=status.HTTP_200_OK
    )
    medicine_data = await fetch_ifap_medication_by_pic(pic=123456)
    assert type(medicine_data) == MedicineData
    assert medicine_data.pic == '123456'
    assert medicine_data.name == 'Test'
    assert medicine_data.description == 'Test'
    assert medicine_data.manufacturer == 'Test'