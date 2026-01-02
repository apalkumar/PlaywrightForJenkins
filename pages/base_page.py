from playwright.sync_api import Page

class BasePage:
    def __init__(self, page: Page):
        self.page = page

        # ---------- Navigation ----------
    def open(self, url):
        self.page.goto(url)

