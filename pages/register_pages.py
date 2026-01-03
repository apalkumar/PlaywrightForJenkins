from playwright.sync_api import expect, Page
import time
from pages.base_page import BasePage


class RegisterPage(BasePage):

        # ---------- Personal Details ----------
    def fill_personal_details(self, data):
        self.page.get_by_placeholder("First Name").fill(data["FirstName"])
        self.page.get_by_placeholder("Last Name").fill(data["LastName"])
        self.page.locator("textarea[rows='3']").fill(data["Address"])
        self.page.locator("input[type='email']").fill(data["Email"])
        self.page.locator("input[type='tel']").fill(str(data["Phone_no"]))

        # ---------- Gender & Hobbies ----------
    def select_gender_hobbies(self):
        self.page.locator("input[value='Male']").click()
        self.page.locator("#checkbox2").click()


     # ---------- Languages (UL / LI dropdown) ----------
    def select_languages(self, languages):
        time.sleep(1)
        self.page.locator("#msdd").hover()
        self.page.locator("#msdd").click()
       
        
        for lang in languages:
            self.page.get_by_text(lang).click()
        time.sleep(1)

        selected_text = self.page.locator("#msdd").inner_text()
        assert all(lang in selected_text for lang in languages)
        self.page.locator("#imagetrgt").click()

        # ---------- Skills ----------
    def select_skill(self,skill):
        self.page.locator("#Skills").select_option(label=skill)
        expect(self.page.locator("#Skills")).to_have_value(skill)

        # ---------- Country ----------
    def select_country(self, country):
        self.page.locator(".selection").click()
        self.page.locator("#select2-country-results").get_by_text(country).click()

        # ---------- DOB ----------
    def select_dob(self, year, month, day):
        self.page.locator("#yearbox").select_option(label=str(year)) 
        self.page.get_by_placeholder("Month").select_option(label=str(month))
        self.page.locator("#daybox").select_option(label=str(day))
        
        assert self.page.locator("#yearbox").input_value()== str(year)
        assert self.page.get_by_placeholder("Month").input_value() == str(month)
        assert self.page.locator("#daybox").input_value() == str(day)

        # ---------- Password ----------
    def set_password(self, password):
        # print("Password is --",password)
        self.page.locator("#firstpassword").fill(password)
        self.page.locator("#secondpassword").fill(password)

    # ---------- Submit ----------
    def submit(self):
        self.page.locator("#Button1").click()

    # open the other url
    def openAnotherUrl(self):
        self.page.goto("https://demo.automationtesting.in/Charts.html")