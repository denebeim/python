from django.contrib.auth import BACKEND_SESSION_KEY, SESSION_KEY, get_user_model
from django.contrib.sessions.backends.db import SessionStore
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from superlists import settings

from .base import FunctionalTest, wait

User = get_user_model()


class MyListsTest(FunctionalTest):
    @wait
    def create_pre_authenticated_session(self, email):
        user = User.objects.create(email=email)
        session = SessionStore()
        session[SESSION_KEY] = user.pk
        session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
        session.save()
        ## to set a cookie we need to first visit the domain,
        ## 404 pages load the quickest!
        self.browser.get(self.live_server_url + "/404_no_such_url/")
        self.browser.add_cookie(
            dict(
                name=settings.SESSION_COOKIE_NAME,
                value=session.session_key,
                path="/",
            )
        )

    def wait_for_my_lists_to_go_away(self):
        try:
            self.browser.find_element(By.LINK_TEXT, "My lists")
        except NoSuchElementException:
            pass

    def test_logged_in_users_lists_are_saved_as_my_lists(self):
        # Edith is a logged in user
        self.create_pre_authenticated_session("edith@example.com")

        # She goes to the home page and starts a list
        self.browser.get(self.live_server_url)
        self.add_list_item("Reticulate splines")
        self.add_list_item("Immanentize eschaton")
        first_list_url = self.browser.current_url

        # She notices a "My lists" link, for the first time
        self.browser.find_element(By.LINK_TEXT, "My lists").click()

        # She sees that her list is in there, named according to its first line item
        self.wait_for(
            lambda: self.browser.find_element(By.LINK_TEXT, "Reticulate splines")
        )
        self.browser.find_element(By.LINK_TEXT, "Reticulate splines").click()
        self.wait_for(
            lambda: self.assertEqual(self.browser.current_url, first_list_url)
        )

        # She decides to start another list, just to see
        self.browser.get(self.live_server_url)
        self.add_list_item("Click cows")
        second_list_url = self.browser.current_url

        # Under "my Lists", her new list appears
        self.browser.find_element(By.LINK_TEXT, "My lists").click()
        self.browser.find_element(By.LINK_TEXT, "Click cows").click()
        self.wait_for(
            lambda: self.assertEqual(self.browser.current_url, second_list_url)
        )

        # She logs out. The "My lists" option disappears
        self.browser.find_element(By.ID, "Log_out").click()
        self.wait_for(lambda: self.wait_for_my_lists_to_go_away())
