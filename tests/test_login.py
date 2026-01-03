# import pytest
# from utilities.excel_register import get_excel_data
# from pages.login_page import Loginpage

# test_data = get_excel_data("test_data.xlsx", "Sheet1")

# @pytest.fixture(scope='function')
# def test_login(page):    
    # data = test_data[0]
    # login = Loginpage(page)
    # login.open(data["Url"])
    # login.enter_initial_email(data["Email"])
    # return page