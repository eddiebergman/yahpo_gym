import pytest
from yahpo_gym.get_suite import get_suite

def test_get_tasks_single():

    df = get_suite('single', version=0.1)
    assert list(df.columns.values) == ['scenario', 'instance', 'target']
    assert len(df) == 21

    with pytest.raises(Exception) as info:
        get_suite('single', version=3)
        assert info == "version must coincide with version in `local_config.data_path`"
    
def test_get_tasks_multi():

    df = get_suite('multi', version=0.1)
    assert list(df.columns.values) == ['scenario', 'instance', 'target']
    assert len(df) == 21

    with pytest.raises(Exception) as info:
        get_suite('single', version=3)
        assert info == "version must coincide with version in `local_config.data_path`"