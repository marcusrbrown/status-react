import pytest
import random

from tests import marks, common_password, get_current_time, unique_password
from tests.base_test_case import SingleDeviceTestCase
from views.sign_in_view import SignInView
from tests.users import basic_user


@marks.all
@marks.account
class TestCreateAccount(SingleDeviceTestCase):

    @marks.testrail_id(5300)
    @marks.critical
    @marks.battery_consumption
    @marks.skip
    # skipped because it is a part of other tests
    # obsolate
    def test_create_account(self):
        sign_in = SignInView(self.driver, skip_popups=False)
        sign_in.accept_agreements()
        if not sign_in.i_have_multiaccount_button.is_element_displayed():
            self.errors.append("'I have an account' button is not displayed")
        sign_in.create_multiaccount_button.click()
        sign_in.password_input.set_value(common_password)
        sign_in.next_button.click()
        sign_in.confirm_password_input.set_value(common_password)
        sign_in.next_button.click()

        sign_in.element_by_text_part('Display name').wait_for_element(30)
        sign_in.name_input.send_keys('user_%s' % get_current_time())

        sign_in.next_button.click()
        self.errors.verify_no_errors()

    @marks.testrail_id(5356)
    @marks.critical
    def test_switch_users_and_add_new_account(self):
        sign_in = SignInView(self.driver)
        sign_in.create_user()
        public_key = sign_in.get_public_key()
        profile = sign_in.get_profile_view()
        profile.logout()
        if sign_in.ok_button.is_element_displayed():
            sign_in.ok_button.click()
        sign_in.back_button.click()
        sign_in.generate_new_key_button.click()
        sign_in.generate_key_button.click()
        sign_in.next_button.click()
        sign_in.next_button.click()
        sign_in.create_password_input.set_value(common_password)
        sign_in.next_button.click()
        sign_in.confirm_your_password_input.set_value(common_password)
        sign_in.next_button.click()

        if sign_in.get_public_key() == public_key:
            self.driver.fail('New account was not created')

    @marks.testrail_id(5379)
    @marks.high
    def test_home_view(self):
        sign_in = SignInView(self.driver)
        sign_in.get_started_button.click()
        sign_in.generate_key_button.click()
        account_button = sign_in.get_account_by_position(random.randint(1, 4))
        username = account_button.username.text
        account_button.click()
        sign_in.next_button.click()
        sign_in.next_button.click()
        sign_in.create_password_input.set_value(common_password)
        sign_in.next_button.click()
        sign_in.confirm_your_password_input.set_value(common_password)
        sign_in.next_button.click()
        home_view = sign_in.get_home_view()
        text = 'There are no recent chats here yet. \nUse the (+) button to discover people \nto chat with'
        if not home_view.element_by_text(text).is_element_displayed():
            self.errors.append("'%s' text is not shown" % text)
        profile_view = home_view.profile_button.click()
        shown_username = profile_view.default_username_text.text
        if shown_username != username:
            self.errors.append("Default username '%s' doesn't match '%s'" % (shown_username, username))
        self.errors.verify_no_errors()

    @marks.testrail_id(5460)
    @marks.medium
    def test_create_account_short_and_mismatch_password(self):
        sign_in = SignInView(self.driver)
        sign_in.get_started_button.click()
        sign_in.generate_key_button.click()
        sign_in.next_button.click()
        sign_in.next_button.click()
        sign_in.create_password_input.set_value('12345')

        mismatch_error = "Passwords don't match"

        sign_in.next_button.click()
        if sign_in.confirm_your_password_input.is_element_displayed():
            self.errors.append('Next button is clickable when password is less then 6 symbols')

        sign_in.create_password_input.set_value('123456')
        sign_in.next_button.click()
        sign_in.confirm_your_password_input.set_value('1234567')
        sign_in.next_button.click()

        if not sign_in.find_text_part(mismatch_error):
            self.errors.append("'%s' is not shown")
        self.errors.verify_no_errors()

    @marks.testrail_id(5414)
    @marks.critical
    @marks.logcat
    def test_password_in_logcat_creating_account(self):
        sign_in = SignInView(self.driver)
        sign_in.create_user(password=unique_password)
        values_in_logcat = sign_in.find_values_in_logcat(password=unique_password)
        if values_in_logcat:
            self.driver.fail(values_in_logcat)

    @marks.testrail_id(5718)
    @marks.medium
    def test_special_characters_in_password_when_creating_new_account(self):
        sign_in = SignInView(self.driver)
        sign_in.create_user(password=basic_user['special_chars_password'])
        sign_in.relogin(password=basic_user['special_chars_password'])
