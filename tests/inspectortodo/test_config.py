from inspectortodo.config import get_config_value, set_config_value


def test_get_config_returns_none_without_config():
    config_value = get_config_value('test_category', 'test_key')
    assert config_value is None


def test_get_config_returns_value_when_overwritten():
    set_config_value('test_category', 'test_key', 'test_value')
    config_value = get_config_value('test_category', 'test_key')
    assert config_value == 'test_value'
