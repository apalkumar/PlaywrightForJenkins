from playwright.sync_api import Page
import time   
from pages.base_page import BasePage

class Loginpage(BasePage):

    # ---------- Initial Email ----------
    def enter_initial_email(self, email):
        self.page.locator("#email").fill(email)
        self.page.locator("#enterimg").click()