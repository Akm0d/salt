"""
tests for host state
"""

from tests.support.case import ModuleCase
from tests.support.helpers import slowTest


class HandleErrorTest(ModuleCase):
    """
    Validate that ordering works correctly
    """

    @slowTest
    def test_function_do_not_return_dictionary_type(self):
        """
        Handling a case when function returns anything but a dictionary type
        """
        ret = self.run_function("state.sls", ["issue-9983-handleerror"])
        self.assertTrue(
            "Data must be a dictionary type" in ret[[a for a in ret][0]]["comment"]
        )
        self.assertTrue(not ret[[a for a in ret][0]]["result"])
        self.assertTrue(ret[[a for a in ret][0]]["changes"] == {})
