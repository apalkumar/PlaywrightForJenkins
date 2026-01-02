import pytest
from utilities.excel_register import get_excel_data
from pages.register_pages import RegisterPage

test_data = get_excel_data("test_data.xlsx", "Sheet1")

@pytest.mark.parametrize("data", test_data)
def test_register_after_login(logged_in_page, data):
    registerpage = RegisterPage(logged_in_page)

    registerpage.fill_personal_details(data)
    registerpage.select_gender_hobbies()
    registerpage.select_languages(["Bulgarian", "English"])
    registerpage.select_skill(data["Skill"])
    registerpage.select_country(data["Country"])
    registerpage.select_dob(year=data["Year"], month=data["Month"], day= data["Day"])
    registerpage.set_password(data["Password"])
    registerpage.submit()