from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

from lists.forms import EMPTY_ITEM_ERROR
from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_list_items(self):
        # Edith goes to the home page and accidentally tries to submit
        # an empty list item. She hits enter on the empty input box
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys(Keys.ENTER)

        # The browser intercepts the request, and does not load the list page
        self.wait_for(
            lambda: 
                self.browser.find_element(By.CSS_SELECTOR, "#id_text:invalid")
        )

        # She starts typing some text for the new item and the error disappears
        self.get_item_input_box().send_keys("Buy Milk")
        self.wait_for(
            lambda: self.browser.find_element(By.CSS_SELECTOR, "#id_text:valid")
        )

        # And she can submit it successfully
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Buy Milk")

        # Pervesly, she now decides to submit a second blank list item
        self.get_item_input_box().send_keys(Keys.ENTER)

        # The browser will not comply
        self.wait_for(
            lambda: self.browser.find_element(By.CSS_SELECTOR, "#id_text:invalid")
        )

        # And she can make it happy by filling some text in
        self.get_item_input_box().send_keys("Make Tea")
        self.wait_for(
            lambda: self.browser.find_element(By.CSS_SELECTOR, "#id_text:valid")
        )
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Buy Milk")
        self.wait_for_row_in_list_table("2: Make Tea")
