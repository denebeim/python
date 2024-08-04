from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

from .base import FunctionalTest
from .list_page import ListPage


class LayoutAndStylingTest(FunctionalTest):
    def test_layout_and_styling(self):
        # Edith goes to the home page,
        self.browser.get(self.live_server_url)

        # her browser is set to a very specific size
        self.browser.set_window_size(1024, 768)

        # she notices the input box is nicely centered
        inputbox = ListPage(self).get_item_input_box()
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size["width"] / 2,
            512,
            delta=10,
        )

        # She starts a new list and sees the input is nicely
        # centered there too
        inputbox.send_keys("testing")
        inputbox.send_keys(Keys.ENTER)
        ListPage(self).wait_for_row_in_list_table("testing","1")
        inputbox = ListPage(self).get_item_input_box()
        self.assertAlmostEqual(
            inputbox.location["x"] + inputbox.size["width"] / 2,
            512,
            delta=10,
        )
