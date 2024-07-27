import os
import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common import WebDriverException
from selenium.webdriver.common.by import By

MAX_WAIT = 5


def wait(fn):
    def modified_fn(*args, **kwargs):
        start_time = time.time()

        while True:
            try:
                return fn(*args, **kwargs)
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.1)

    return modified_fn


class FunctionalTest(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        test_server = os.environ.get("TEST_SERVER")
        if test_server:
            self.live_server_url = "http://" + test_server

    def tearDown(self):
        self.browser.quit()

    @wait
    def wait_for(self, fn):
        return fn()

    def row_in_list_table(self, row_text):
        table = self.browser.find_element(By.ID, "id_list_table")
        rows = table.find_elements(By.TAG_NAME, "tr")
        self.assertIn(row_text, [row.text for row in rows])

    def wait_for_row_in_list_table(self, row_text):
        return self.wait_for(lambda: self.row_in_list_table(row_text))

    def get_item_input_box(self):
        return self.browser.find_element(By.ID, "id_text")

    def wait_to_be_logged_in(self, email):
        self.wait_for(lambda: self.browser.find_element(By.ID, "Log_out"))
        navbar = self.browser.find_element(By.CSS_SELECTOR, ".navbar")
        self.assertIn(email, navbar.text)

    def wait_to_be_logged_out(self, email):
        self.wait_for(lambda: self.browser.find_element(By.NAME, "email"))
        navbar = self.browser.find_element(By.CSS_SELECTOR, ".navbar")
        self.assertNotIn(email, navbar.text)
