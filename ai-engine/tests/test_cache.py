from unittest.mock import MagicMock

from serving.cache import CachedModel, ModelCache


def test_cache_creation():
    cache = ModelCache()

    assert cache.size() == 0
    assert cache.hits == 0
    assert cache.misses == 0


def test_put_model():
    cache = ModelCache()

    model = MagicMock()

    cached = cache.put(
        model_name="failure_prediction",
        model=model,
        version="1",
        stage="Production",
    )

    assert isinstance(cached, CachedModel)
    assert cache.size() == 1


def test_get_model():
    cache = ModelCache()

    model = MagicMock()

    cache.put(
        "failure_prediction",
        model,
        "1",
        "Production",
    )

    result = cache.get(
        "failure_prediction"
    )

    assert result is not None
    assert result.model == model


def test_get_missing_model():
    cache = ModelCache()

    result = cache.get("missing")

    assert result is None
    assert cache.misses == 1


def test_contains():
    cache = ModelCache()

    cache.put(
        "failure_prediction",
        MagicMock(),
        "1",
        "Production",
    )

    assert cache.contains(
        "failure_prediction"
    )

    assert not cache.contains(
        "abc"
    )


def test_remove():
    cache = ModelCache()

    cache.put(
        "failure_prediction",
        MagicMock(),
        "1",
        "Production",
    )

    cache.remove(
        "failure_prediction"
    )

    assert cache.size() == 0


def test_clear():
    cache = ModelCache()

    cache.put(
        "a",
        MagicMock(),
        "1",
        "Production",
    )

    cache.put(
        "b",
        MagicMock(),
        "1",
        "Production",
    )

    cache.clear()

    assert cache.size() == 0


def test_list_models():
    cache = ModelCache()

    cache.put(
        "b",
        MagicMock(),
        "1",
        "Production",
    )

    cache.put(
        "a",
        MagicMock(),
        "1",
        "Production",
    )

    assert cache.list_models() == [
        "a",
        "b",
    ]


def test_hit_rate():
    cache = ModelCache()

    cache.put(
        "model",
        MagicMock(),
        "1",
        "Production",
    )

    cache.get("model")
    cache.get("missing")

    assert cache.hit_rate == 0.5


def test_stats():
    cache = ModelCache()

    cache.put(
        "failure_prediction",
        MagicMock(),
        "1",
        "Production",
    )

    stats = cache.stats()

    assert "size" in stats
    assert "hits" in stats
    assert "misses" in stats
    assert "models" in stats


def test_items():
    cache = ModelCache()

    cache.put(
        "failure_prediction",
        MagicMock(),
        "1",
        "Production",
    )

    items = cache.items()

    assert len(items) == 1
    assert isinstance(items[0], CachedModel)