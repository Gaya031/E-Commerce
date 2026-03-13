import asyncio

from app.services import delivery_service


class DummySeller:
    def __init__(self, latitude=None, longitude=None):
        self.latitude = latitude
        self.longitude = longitude


def test_coerce_float_and_extract_drop_coordinates():
    assert delivery_service._coerce_float("23.4") == 23.4
    assert delivery_service._coerce_float("x") is None

    lat, lng = delivery_service._extract_drop_coordinates(
        {"coordinates": {"lat": "23.25", "lng": "77.46"}}
    )
    assert lat == 23.25
    assert lng == 77.46


def test_estimate_distance_defaults_when_coordinates_missing():
    seller = DummySeller(latitude=None, longitude=None)
    distance = delivery_service._estimate_distance_km(seller, {"coordinates": {"lat": 23.2, "lng": 77.4}})
    assert distance == 5


def test_generate_delivery_route_fallback(monkeypatch):
    class BrokenAsyncClient:
        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            return False

        async def get(self, *_args, **_kwargs):
            raise RuntimeError("network down")

    monkeypatch.setattr(delivery_service.httpx, "AsyncClient", lambda *args, **kwargs: BrokenAsyncClient())

    route = asyncio.run(delivery_service.generate_delivery_route(23.25, 77.46, 23.26, 77.47))
    assert route["source"] == "fallback"
    assert isinstance(route["polyline"], list)
    assert route["eta_minutes"] >= 1
