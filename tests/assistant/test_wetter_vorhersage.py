"""Tests for wetter_vorhersage.py."""

from assistant.wetter_vorhersage import weather_output_hnadler


def test_wetter_heute() -> None:
    """Test weatehr forcast for today."""
    assert 'heute' in weather_output_hnadler('wie ist das wetter')


def test_wetter_morgen() -> None:
    """Test weatehr forcast for tomorrow."""
    assert 'morgen' in weather_output_hnadler('wie ist das wetter  morgen')


def test_wetter_ubermorgen() -> None:
    """Test weatehr forcast for after tomorrow."""
    assert 'übermorgen' in weather_output_hnadler('wie ist das wetter übermorgen')


def test_wetter_city() -> None:
    """Test weatehr forcast for after tomorrow."""
    assert 'Berlin' in weather_output_hnadler('wie ist das wetter in Berlin übermorgen')
