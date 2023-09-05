import pytest
from unittest.mock import MagicMock, patch

from ..common import BaseYealinkPgAssociator, BaseYealinkPlugin


@pytest.fixture
def v82_entry(module_initializer):
    def execfile_(_, common_globals):
        common_globals['BaseYealinkPlugin'] = BaseYealinkPlugin
        common_globals['BaseYealinkPgAssociator'] = BaseYealinkPgAssociator

    return module_initializer('entry', {'execfile_': execfile_})


@pytest.fixture
def v82_plugin(v82_entry):
    with patch('v82.common.FetchfwPluginHelper'), patch(
        'v82.common.TemplatePluginHelper'
    ):
        yield v82_entry.YealinkPlugin(MagicMock(), 'test_dir', MagicMock(), MagicMock())
