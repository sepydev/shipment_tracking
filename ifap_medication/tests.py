import pytest
import responses
from rest_framework import status

from ifap_medication.fetch_ifap_medication import (
    MedicineData, _parse_xml_to_dict, _map_to_medicine, _make_ifap_request, _execute_http_post
)


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


@pytest.fixture
def settings():
    class Settings:
        IFAP_MEDICATION_SERVICE_BASE_URL = 'http://localhost:8001'

    return Settings()


@pytest.fixture
def expected_medication_data():
    return MedicineData(
        pic=123456,
        name='Test',
        description='Test',
        manufacturer_name='manufacturer_name'
    )


@pytest.fixture
def snake_case_body(expected_medication_data):
    return f"""
        <medicine_v2>
                <pic>{expected_medication_data.pic}</pic>
                <name>{expected_medication_data.name}</name>
                <description>{expected_medication_data.description}</description>
                <manufacturer_name>{expected_medication_data.manufacturer_name}</manufacturer_name>
        </medicine_v2>
        """


@pytest.fixture
def kebab_case_body(expected_medication_data):
    return f"""
        <medicine_v2>
                <pic>{expected_medication_data.pic}</pic>
                <name>{expected_medication_data.name}</name>
                <description>{expected_medication_data.description}</description>
                <manufacturer-name>{expected_medication_data.manufacturer_name}</manufacturer-name>
        </medicine_v2>
        """


@pytest.fixture
def ifap_url(settings):
    return f"{settings.IFAP_MEDICATION_SERVICE_BASE_URL}/ifapGetMedicineByPICV2"


@pytest.mark.asyncio
@responses.activate
async def test_execute_http_post_success(settings):
    ifap_url = f"{settings.IFAP_MEDICATION_SERVICE_BASE_URL}/test"
    responses.add(
        responses.POST,
        ifap_url,
        body='SUCCESS',
        status=200
    )
    response = _execute_http_post(url=ifap_url, params={'id': 1})
    assert response == 'SUCCESS'


@pytest.fixture
def ifab_fixtures(settings, ifap_url, expected_medication_data, snake_case_body, kebab_case_body):

    class IfapFixtures:
        SETTINGS = settings
        IFAP_URL = ifap_url
        EXPECTED_MEDICATION_DATA = expected_medication_data
        SNAKE_CASE_BODY = snake_case_body
        KEBAB_CASE_BODY = kebab_case_body

    return IfapFixtures()


@pytest.mark.asyncio
@responses.activate
async def test_fetch_ifap_medication_by_pic_snake_case_success(ifab_fixtures):
    body = ifab_fixtures.SNAKE_CASE_BODY
    await _test_fetech_ifap_medication_by_pic(body, ifab_fixtures)


@pytest.mark.asyncio
@responses.activate
async def test_fetch_ifap_medication_by_pic_kebab_case_success(ifab_fixtures):
    body = ifab_fixtures.KEBAB_CASE_BODY
    await _test_fetech_ifap_medication_by_pic(body, ifab_fixtures)


async def _test_fetech_ifap_medication_by_pic(body, ifab_fixtures):
    responses.add(
        responses.POST,
        ifab_fixtures.IFAP_URL,
        body=body,
        status=status.HTTP_200_OK
    )
    medicine_data = await fetch_ifap_medication_by_pic(pic=ifab_fixtures.EXPECTED_MEDICATION_DATA.pic)
    assert type(medicine_data) == MedicineData
    assert medicine_data == ifab_fixtures.EXPECTED_MEDICATION_DATA


@pytest.mark.asyncio
@responses.activate
async def test_fetch_ifap_medication_by_pic_failure(ifab_fixtures):
    responses.add(
        responses.POST,
        ifab_fixtures.IFAP_URL,
        body='ERROR',
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
    )
    with pytest.raises(Exception):
        await fetch_ifap_medication_by_pic(pic=123456)
        assert False


@pytest.mark.asyncio
@responses.activate
async def test_fetch_ifap_medication_by_pic_unauthorized(ifab_fixtures):
    responses.add(
        responses.POST,
        ifab_fixtures.IFAP_URL,
        body='ERROR',
        status=status.HTTP_401_UNAUTHORIZED
    )
    with pytest.raises(Exception):
        await fetch_ifap_medication_by_pic(pic=123456)
        assert False


@pytest.mark.asyncio
async def test_fetch_ifap_medication_by_pic_invalid_pic(ifab_fixtures):
    with pytest.raises(Exception):
        await fetch_ifap_medication_by_pic(pic='123456')
        assert False
