import time

import emoji
import pytest
import random
import string
from datetime import datetime
from selenium.common.exceptions import TimeoutException

from tests import marks, get_current_time
from tests.base_test_case import MultipleDeviceTestCase, SingleDeviceTestCase
from tests.users import transaction_senders, transaction_recipients, basic_user, ens_user
from views.sign_in_view import SignInView


@marks.chat
class TestMessagesOneToOneChatMultiple(MultipleDeviceTestCase):

    @marks.testrail_id(5305)
    @marks.critical
    def test_text_message_1_1_chat(self):
        self.create_drivers(2)
        device_1, device_2 = SignInView(self.drivers[0]), SignInView(self.drivers[1])
        device_1_home, device_2_home = device_1.create_user(), device_2.create_user()
        profile_1 = device_1_home.profile_button.click()
        default_username_1 = profile_1.default_username_text.text
        device_1_home = profile_1.get_back_to_home_view()
        device_2_public_key = device_2_home.get_public_key()
        device_2_home.home_button.click()

        device_1_chat = device_1_home.add_contact(device_2_public_key)

        message = 'hello'
        device_1_chat.chat_message_input.send_keys(message)
        device_1_chat.send_message_button.click()

        device_2_chat = device_2_home.get_chat_with_user(default_username_1).click()
        device_2_chat.chat_element_by_text(message).wait_for_visibility_of_element()

    @marks.testrail_id(5310)
    @marks.critical
    def test_offline_messaging_1_1_chat(self):
        self.create_drivers(2)
        sign_in_1, sign_in_2 = SignInView(self.drivers[0]), SignInView(self.drivers[1])
        home_1, home_2 = sign_in_1.create_user(), sign_in_2.create_user()
        public_key_1 = home_1.get_public_key()
        home_1.home_button.click()

        home_1.toggle_airplane_mode()  # airplane mode on primary device

        profile_2 = home_2.profile_button.click()
        username_2 = profile_2.default_username_text.text
        profile_2.get_back_to_home_view()
        chat_2 = home_2.add_contact(public_key_1)
        message_1 = 'test message'
        chat_2.chat_message_input.send_keys(message_1)
        chat_2.send_message_button.click()
        chat_2.toggle_airplane_mode()  # airplane mode on secondary device

        home_1.toggle_airplane_mode()  # turning on WiFi connection on primary device

        home_1.connection_status.wait_for_invisibility_of_element(30)
        chat_element = home_1.get_chat_with_user(username_2)
        chat_element.wait_for_visibility_of_element(30)
        chat_1 = chat_element.click()
        chat_1.chat_element_by_text(message_1).wait_for_visibility_of_element(2)

        chat_2.toggle_airplane_mode()  # turning on WiFi connection on secondary device
        home_1.toggle_airplane_mode()  # airplane mode on primary device

        chat_2.element_by_text('Connecting to peers...').wait_for_invisibility_of_element(60)
        chat_2.connection_status.wait_for_invisibility_of_element(60)
        message_2 = 'one more message'
        chat_2.chat_message_input.send_keys(message_2)
        chat_2.send_message_button.click_until_absense_of_element(chat_2.send_message_button)

        home_1.toggle_airplane_mode()  # turning on WiFi connection on primary device

        chat_1 = chat_element.click()
        chat_1.chat_element_by_text(message_2).wait_for_visibility_of_element(180)

    @marks.testrail_id(5338)
    @marks.critical
    def test_messaging_in_different_networks(self):
        self.create_drivers(2)
        sign_in_1, sign_in_2 = SignInView(self.drivers[0]), SignInView(self.drivers[1])
        home_1, home_2 = sign_in_1.create_user(), sign_in_2.create_user()
        profile_1 = home_1.profile_button.click()
        default_username_1 = profile_1.default_username_text.text
        home_1 = profile_1.get_back_to_home_view()
        public_key_2 = home_2.get_public_key()
        profile_2 = home_2.get_profile_view()
        profile_2.switch_network('Mainnet with upstream RPC')

        chat_1 = home_1.add_contact(public_key_2)
        message = 'test message'
        chat_1.chat_message_input.send_keys(message)
        chat_1.send_message_button.click()

        chat_2 = home_2.get_chat_with_user(default_username_1).click()
        chat_2.chat_element_by_text(message).wait_for_visibility_of_element()

        public_chat_name = home_1.get_public_chat_name()
        chat_1.get_back_to_home_view()
        home_1.join_public_chat(public_chat_name)
        chat_2.get_back_to_home_view()
        home_2.join_public_chat(public_chat_name)

        chat_1.chat_message_input.send_keys(message)
        chat_1.send_message_button.click()
        chat_2.chat_element_by_text(message).wait_for_visibility_of_element()

    @marks.testrail_id(5315)
    @marks.high
    def test_send_message_to_newly_added_contact(self):
        self.create_drivers(2)
        device_1, device_2 = SignInView(self.drivers[0]), SignInView(self.drivers[1])

        device_1_home, device_2_home = device_1.create_user(), device_2.create_user()
        profile_1 = device_1_home.profile_button.click()
        default_username_1 = profile_1.default_username_text.text
        device_1_home = profile_1.get_back_to_home_view()

        profile_1 = device_1_home.profile_button.click()
        profile_1.edit_profile_picture('sauce_logo.png')
        profile_1.home_button.click()

        device_2_public_key = device_2_home.get_public_key()
        device_2_home.home_button.click()

        device_1_chat = device_1_home.add_contact(device_2_public_key)
        message = 'hello'
        device_1_chat.chat_message_input.send_keys(message)
        device_1_chat.send_message_button.click()

        chat_element = device_2_home.get_chat_with_user(default_username_1)
        chat_element.wait_for_visibility_of_element()
        device_2_chat = chat_element.click()
        if not device_2_chat.chat_element_by_text(message).is_element_displayed():
            self.errors.append("Message with test '%s' was not received" % message)
        if not device_2_chat.add_to_contacts.is_element_displayed():
            self.errors.append('Add to contacts button is not shown')
        if device_2_chat.user_name_text.text != default_username_1:
            self.errors.append("Default username '%s' is not shown in one-to-one chat" % default_username_1)
        device_2_chat.chat_options.click()
        device_2_chat.view_profile_button.click()
        if not device_2_chat.contact_profile_picture.is_element_image_equals_template('sauce_logo.png'):
            self.errors.append("Updated profile picture is not shown in one-to-one chat")
        self.errors.verify_no_errors()

    @marks.testrail_id(5316)
    @marks.critical
    def test_add_to_contacts(self):
        self.create_drivers(2)
        device_1, device_2 = SignInView(self.drivers[0]), SignInView(self.drivers[1])

        device_1_home, device_2_home = device_1.create_user(), device_2.create_user()
        profile_1 = device_1_home.profile_button.click()
        default_username_1 = profile_1.default_username_text.text
        device_1_home = profile_1.get_back_to_home_view()

        device_2_public_key = device_2_home.get_public_key()
        profile_2 = device_2_home.get_profile_view()
        file_name = 'sauce_logo.png'
        profile_2.edit_profile_picture(file_name)
        default_username_2 = profile_2.default_username_text.text
        profile_2.home_button.click()

        device_1_chat = device_1_home.add_contact(device_2_public_key)
        message = 'hello'
        device_1_chat.chat_message_input.send_keys(message)
        device_1_chat.send_message_button.click()

        chat_element = device_2_home.get_chat_with_user(default_username_1)
        chat_element.wait_for_visibility_of_element()
        device_2_chat = chat_element.click()
        if not device_2_chat.chat_element_by_text(message).is_element_displayed():
            self.errors.append("Message with text '%s' was not received" % message)
        device_2_chat.connection_status.wait_for_invisibility_of_element(60)
        device_2_chat.add_to_contacts.click()

        device_2_chat.get_back_to_home_view()
        device_2_home.plus_button.click()
        device_2_contacts = device_2_home.start_new_chat_button.click()
        if not device_2_contacts.element_by_text(default_username_1).is_element_displayed():
            self.errors.append('%s is not added to contacts' % default_username_1)

        if device_1_chat.user_name_text.text != default_username_2:
            self.errors.append("Default username '%s' is not shown in one-to-one chat" % default_username_2)
        device_1_chat.chat_options.click()
        device_1_chat.view_profile_button.click()
        if not device_1_chat.contact_profile_picture.is_element_image_equals_template(file_name):
            self.errors.append("Updated profile picture is not shown in one-to-one chat")
        self.errors.verify_no_errors()

    @marks.testrail_id(5373)
    @marks.high
    def test_send_and_open_links(self):
        self.create_drivers(2)
        device_1, device_2 = SignInView(self.drivers[0]), SignInView(self.drivers[1])

        home_1, home_2 = device_1.create_user(), device_2.create_user()
        profile_1 = home_1.profile_button.click()
        default_username_1 = profile_1.default_username_text.text
        home_1 = profile_1.get_back_to_home_view()
        public_key_2 = home_2.get_public_key()
        home_2.home_button.click()

        chat_1 = home_1.add_contact(public_key_2)
        url_message = 'status.im'
        chat_1.chat_message_input.send_keys(url_message)
        chat_1.send_message_button.click()
        chat_1.get_back_to_home_view()
        chat_2 = home_2.get_chat_with_user(default_username_1).click()
        chat_2.element_starts_with_text(url_message, 'button').click()
        web_view = chat_2.open_in_status_button.click()
        try:
            web_view.find_full_text('Private, Secure Communication')
        except TimeoutException:
            self.errors.append('Device 2: URL was not opened from 1-1 chat')
        web_view.back_to_home_button.click()
        chat_2.home_button.click()
        chat_2.back_button.click()

        chat_name = ''.join(random.choice(string.ascii_lowercase) for _ in range(7))
        home_1.join_public_chat(chat_name)
        home_2.join_public_chat(chat_name)
        chat_2.chat_message_input.send_keys(url_message)
        chat_2.send_message_button.click()
        chat_1.element_starts_with_text(url_message, 'button').click()
        web_view = chat_1.open_in_status_button.click()
        try:
            web_view.find_full_text('Private, Secure Communication')
        except TimeoutException:
            self.errors.append('Device 1: URL was not opened from 1-1 chat')
        self.errors.verify_no_errors()

    @marks.testrail_id(5326)
    @marks.critical
    def test_offline_status(self):
        self.create_drivers(1)
        sign_in = SignInView(self.drivers[0])
        home_view = sign_in.create_user()

        home_view.airplane_mode_button.click()

        chat = home_view.add_contact(transaction_senders['C']['public_key'])
        chat.element_by_text('Offline').wait_for_visibility_of_element(15)
        if chat.connection_status.text != 'Offline':
            self.errors.append('Offline status is not shown in 1-1 chat')
        chat.get_back_to_home_view()

        if home_view.connection_status.text != 'Offline':
            self.errors.append('Offline status is not shown in home screen')

        public_chat = home_view.join_public_chat(home_view.get_public_chat_name())
        if public_chat.connection_status.text != 'Offline':
            self.errors.append('Offline status is not shown in a public chat')
        self.errors.verify_no_errors()

    @marks.testrail_id(5374)
    @marks.high
    def test_message_marked_as_sent_in_1_1_chat(self):
        self.create_drivers(1)
        sign_in_view = SignInView(self.drivers[0])
        home_view = sign_in_view.create_user()
        chat_view = home_view.add_contact(basic_user['public_key'])
        message = 'test message'
        chat_view.chat_message_input.send_keys(message)
        chat_view.send_message_button.click()
        if chat_view.chat_element_by_text(message).status.text != 'Sent':
            self.errors.append("'Sent' status is not shown under the sent text message")
        self.errors.verify_no_errors()

    @marks.testrail_id(5362)
    @marks.critical
    def test_unread_messages_counter_1_1_chat(self):
        self.create_drivers(2)
        device_1, device_2 = SignInView(self.drivers[0]), SignInView(self.drivers[1])
        device_1_home, device_2_home = device_1.create_user(), device_2.create_user()
        profile_2 = device_2_home.profile_button.click()
        default_username_2 = profile_2.default_username_text.text
        device_2_home = profile_2.get_back_to_home_view()
        device_1_public_key = device_1_home.get_public_key()
        device_1_home.home_button.click()

        device_2_chat = device_2_home.add_contact(device_1_public_key)

        message = 'test message'
        device_2_chat.chat_message_input.send_keys(message)
        device_2_chat.send_message_button.click()

        if device_1_home.home_button.counter.text != '1':
            self.errors.append('New messages counter is not shown on Home button')

        chat_element = device_1_home.get_chat_with_user(default_username_2)
        if chat_element.new_messages_counter.text != '1':
            self.errors.append('New messages counter is not shown on chat element')

        chat_element.click()
        device_1_home.get_back_to_home_view()

        if device_1_home.home_button.counter.is_element_displayed():
            self.errors.append('New messages counter is shown on Home button for already seen message')

        if chat_element.new_messages_counter.is_element_displayed():
            self.errors.append('New messages counter is shown on chat element for already seen message')
        self.errors.verify_no_errors()

    @marks.testrail_id(5425)
    @marks.medium
    @marks.skip
    # TODO: e2e blocker: 8995 (should be enabled after fix)
    def test_bold_and_italic_text_in_messages(self):
        self.create_drivers(2)
        sign_in_1, sign_in_2 = SignInView(self.drivers[0]), SignInView(self.drivers[1])
        device_1_home, device_2_home = sign_in_1.create_user(), sign_in_2.create_user()
        profile_2 = device_2_home.profile_button.click()
        default_username_2 = profile_2.default_username_text.text
        device_2_home = profile_2.get_back_to_home_view()
        device_1_public_key = device_1_home.get_public_key()
        device_1_home.home_button.click()

        device_2_chat = device_2_home.add_contact(device_1_public_key)

        bold_text = 'bold text'
        bold_text_expected = u'\u200b' + bold_text + u'\u200b'  # Zero width whitespaces
        device_2_chat.chat_message_input.send_keys('*%s*' % bold_text)
        device_2_chat.send_message_button.click()
        if not device_2_chat.chat_element_by_text(bold_text_expected).is_element_displayed():
            self.errors.append('Bold text is not displayed in 1-1 chat for the sender \n')

        device_1_chat = device_1_home.get_chat_with_user(default_username_2).click()
        if not device_1_chat.chat_element_by_text(bold_text_expected).is_element_displayed():
            self.errors.append('Bold text is not displayed in 1-1 chat for the recipient \n')

        italic_text = 'italic text'
        italic_text_expected = u'\u200b' + italic_text + u'\u200b'
        device_2_chat.chat_message_input.send_keys('_%s_' % italic_text)
        device_2_chat.send_message_button.click()
        if not device_2_chat.chat_element_by_text(italic_text_expected).is_element_displayed():
            self.errors.append('Italic text is not displayed in 1-1 chat for the sender \n')

        if not device_1_chat.chat_element_by_text(italic_text_expected).is_element_displayed():
            self.errors.append('Italic text is not displayed in 1-1 chat for the recipient \n')

        device_1_chat.get_back_to_home_view()
        device_2_chat.get_back_to_home_view()
        chat_name = device_1_home.get_public_chat_name()
        device_1_home.join_public_chat(chat_name)
        device_2_home.join_public_chat(chat_name)

        device_2_chat.chat_message_input.send_keys('*%s*' % bold_text)
        device_2_chat.send_message_button.click()
        if not device_2_chat.chat_element_by_text(bold_text_expected).is_element_displayed():
            self.errors.append('Bold text is not displayed in public chat for the sender')

        if not device_1_chat.chat_element_by_text(bold_text_expected).is_element_displayed():
            self.errors.append('Bold text is not displayed in public chat for the recipient')

        device_2_chat.chat_message_input.send_keys('_%s_' % italic_text)
        device_2_chat.send_message_button.click()
        if not device_2_chat.chat_element_by_text(italic_text_expected).is_element_displayed():
            self.errors.append('Italic text is not displayed in public chat for the sender')

        if not device_1_chat.chat_element_by_text(italic_text_expected).is_element_displayed():
            self.errors.append('Italic text is not displayed in 1-1 chat for the recipient')

        self.errors.verify_no_errors()

    @marks.skip
    @marks.testrail_id(5385)
    @marks.high
    # TODO: update with correct time - doesn't work for now
    def test_timestamp_in_chats(self):
        self.create_drivers(2)
        sign_in_1, sign_in_2 = SignInView(self.drivers[0]), SignInView(self.drivers[1])
        username_1 = 'user_%s' % get_current_time()
        device_1_home, device_2_home = sign_in_1.create_user(), sign_in_2.create_user()
        device_2_public_key = device_2_home.get_public_key()
        device_2_home.home_button.click()

        device_1_chat = device_1_home.add_contact(device_2_public_key)

        message = 'test text'
        device_1_chat.chat_message_input.send_keys(message)
        device_1_chat.send_message_button.click()
        sent_time = datetime.strptime(device_1_chat.driver.device_time, '%a %b %d %H:%M:%S GMT %Y').strftime("%I:%M %p")
        if not device_1_chat.chat_element_by_text(message).contains_text(sent_time):
            self.errors.append('Timestamp is not displayed in 1-1 chat for the sender')
        if device_1_chat.chat_element_by_text(message).member_photo.is_element_displayed():
            self.errors.append('Member photo is displayed in 1-1 chat for the sender')

        device_2_chat = device_2_home.get_chat_with_user(username_1).click()
        if not device_2_chat.chat_element_by_text(message).contains_text(sent_time):
            self.errors.append('Timestamp is not displayed in 1-1 chat for the recipient')
        if not device_2_chat.chat_element_by_text(message).member_photo.is_element_displayed():
            self.errors.append('Member photo is not displayed in 1-1 chat for the recipient')

        device_1_chat.get_back_to_home_view()
        device_2_chat.get_back_to_home_view()
        chat_name = device_1_home.get_public_chat_name()
        device_1_home.join_public_chat(chat_name)
        device_2_home.join_public_chat(chat_name)

        device_2_chat.chat_message_input.send_keys(message)
        device_2_chat.send_message_button.click()
        sent_time = datetime.strptime(device_2_chat.driver.device_time, '%a %b %d %H:%M:%S GMT %Y').strftime("%I:%M %p")
        if not device_2_chat.chat_element_by_text(message).contains_text(sent_time):
            self.errors.append('Timestamp is not displayed in public chat for the sender')
        if device_2_chat.chat_element_by_text(message).member_photo.is_element_displayed():
            self.errors.append('Member photo is displayed in public chat for the sender')

        if not device_1_chat.chat_element_by_text(message).contains_text(sent_time):
            self.errors.append('Timestamp is not displayed in public chat for the recipient')
        if not device_1_chat.chat_element_by_text(message).member_photo.is_element_displayed():
            self.errors.append('Member photo is not displayed in 1-1 chat for the recipient')

        self.errors.verify_no_errors()

    @marks.testrail_id(5405)
    @marks.high
    @marks.skip
    # TODO: temporary skipped due to 8601
    def test_fiat_value_is_correctly_calculated_on_recipient_side(self):
        sender = transaction_senders['Y']
        recipient = transaction_recipients['I']

        self.create_drivers(2)
        signin_view1, signin_view2 = SignInView(self.drivers[0]), SignInView(self.drivers[1])
        home_view1, home_view2 = signin_view1.recover_access(sender['passphrase']), signin_view2.recover_access(
            recipient['passphrase'])

        devices = [
            {'home_view': home_view1, 'currency': 'AUD'},
            {'home_view': home_view2, 'currency': 'EUR'},
        ]

        # changing currency for both devices
        for device in devices:
            wallet_view = device['home_view'].wallet_button.click()
            wallet_view.set_up_wallet()
            wallet_view.set_currency(device['currency'])
            wallet_view.get_back_to_home_view()

        device1 = devices[0]
        device2 = devices[1]

        # setting up device1 wallet
        # wallet1 = device1['home_view'].wallet_button.click()
        # wallet1.get_back_to_home_view()

        # sending ETH to device2 in 1*1 chat
        device1_chat = device1['home_view'].add_contact(recipient['public_key'])
        send_amount = device1_chat.get_unique_amount()
        device1_chat.send_transaction_in_1_1_chat('ETHro', send_amount)

        sent_message = device1_chat.chat_element_by_text(send_amount)
        if not sent_message.is_element_displayed() and not sent_message.contains_text(device1['currency']):
            self.errors.append('Wrong currency fiat value while sending ETH in 1*1 chat.')

        device2_chat = device2['home_view'].get_chat_with_user(sender['username']).click()
        received_message = device2_chat.chat_element_by_text(send_amount)
        if not received_message.is_element_displayed() and not received_message.contains_text(device2['currency']):
            self.errors.append('Wrong currency fiat value while receiving ETH in 1*1 chat.')

        # Currently disabled because sending / requesting funds from wallet is not shown in chat
        # device1_chat.get_back_to_home_view()
        # wallet1 = device1['home_view'].wallet_button.click()
        # send_amount = device1_chat.get_unique_amount()

        # Send and request some ETH from wallet and check whether the fiat currency value of
        # the new messages is equal to user-selected
        # wallet1.send_transaction(asset_name='ETHro', recipient=recipient['username'], amount=send_amount)
        # wallet1.get_back_to_home_view()
        # device1_chat = device1['home_view'].get_chat_with_user(recipient['username']).click()
        #
        # sent_message = device1_chat.chat_element_by_text(send_amount)
        # received_message = device2_chat.chat_element_by_text(send_amount)
        #
        # if not sent_message.is_element_displayed() and not sent_message.contains_text(device1['currency']):
        #     self.errors.append('Wrong currency fiat value while sending ETH from wallet.')
        #
        # if not received_message.is_element_displayed() and not sent_message.contains_text(device2['currency']):
        #     self.errors.append('Wrong currency fiat value while receiving ETH sent via wallet.')

        self.errors.verify_no_errors()


@marks.all
@marks.chat
class TestMessagesOneToOneChatSingle(SingleDeviceTestCase):

    @marks.testrail_id(5317)
    @marks.critical
    def test_copy_and_paste_messages(self):
        sign_in = SignInView(self.driver)
        home = sign_in.create_user()

        home.join_public_chat(''.join(random.choice(string.ascii_lowercase) for _ in range(7)))
        chat = sign_in.get_chat_view()
        message_text = 'test'
        message_input = chat.chat_message_input
        message_input.send_keys(message_text)
        chat.send_message_button.click()

        chat.chat_element_by_text(message_text).long_press_element()
        chat.element_by_text('Copy').click()

        message_input.paste_text_from_clipboard()
        if message_input.text != message_text:
            self.errors.append('Message text was not copied in a public chat')

        chat.get_back_to_home_view()
        home.add_contact(transaction_senders['M']['public_key'])
        message_input.send_keys(message_text)
        chat.send_message_button.click()

        chat.chat_element_by_text(message_text).long_press_element()
        chat.element_by_text('Copy').click()

        message_input.paste_text_from_clipboard()
        if message_input.text != message_text:
            self.errors.append('Message text was not copied in 1-1 chat')
        self.errors.verify_no_errors()

    @marks.testrail_id(5322)
    @marks.medium
    def test_delete_cut_and_paste_messages(self):
        sign_in = SignInView(self.driver)
        home = sign_in.create_user()
        chat = home.add_contact(transaction_senders['N']['public_key'])

        message_text = 'test'
        message_input = chat.chat_message_input
        message_input.send_keys(message_text)

        message_input.delete_last_symbols(2)
        current_text = message_input.text
        if current_text != message_text[:-2]:
            self.driver.fail("Message input text '%s' doesn't match expected '%s'" % (current_text, message_text[:-2]))

        message_input.cut_text()

        message_input.paste_text_from_clipboard()
        chat.send_message_button.click()

        chat.chat_element_by_text(message_text[:-2] + ' ').wait_for_visibility_of_element(2)

    @marks.testrail_id(5328)
    @marks.critical
    @marks.battery_consumption
    def test_send_emoji(self):
        sign_in = SignInView(self.driver)
        home = sign_in.create_user()

        home.join_public_chat(home.get_public_chat_name())
        chat = sign_in.get_chat_view()
        emoji_name = random.choice(list(emoji.EMOJI_UNICODE))
        emoji_unicode = emoji.EMOJI_UNICODE[emoji_name]
        chat.chat_message_input.send_keys(emoji.emojize(emoji_name))
        chat.send_message_button.click()

        if not chat.chat_element_by_text(emoji_unicode).is_element_displayed():
            self.errors.append('Message with emoji was not sent in public chat')

        chat.get_back_to_home_view()
        home.add_contact(transaction_senders['O']['public_key'])
        chat.chat_message_input.send_keys(emoji.emojize(emoji_name))
        chat.send_message_button.click()

        if not chat.chat_element_by_text(emoji_unicode).is_element_displayed():
            self.errors.append('Message with emoji was not sent in 1-1 chat')
        self.errors.verify_no_errors()

    @marks.testrail_id(5393)
    @marks.high
    @marks.skip
    # TODO: temporary skipped due to 8601
    def test_that_fiat_value_is_correct_for_token_transactions(self):
        sender_passphrase = transaction_senders['X']['passphrase']
        recipient_public_key = transaction_recipients['H']['public_key']
        recipient_user_name = transaction_recipients['H']['username']
        default_currency = 'USD'
        user_currency = 'EUR'
        sigin_view = SignInView(self.driver)
        home_view = sigin_view.recover_access(sender_passphrase)
        wallet = home_view.wallet_button.click()
        wallet.set_up_wallet()

        wallet.get_back_to_home_view()

        chat = home_view.add_contact(recipient_public_key)
        send_amount, request_amount = [chat.get_unique_amount() for _ in range(2)]
        # Send and request some tokens in 1x1 chat and check whether the fiat currency value of the messages is equal
        # to default
        chat.send_transaction_in_1_1_chat('STT', send_amount)
        chat.request_transaction_in_1_1_chat('STT', request_amount)

        send_message = chat.chat_element_by_text(send_amount)
        if not send_message.is_element_displayed() and not send_message.contains_text(default_currency):
            self.errors.append('Wrong fiat value while sending assets in 1-1 chat with default currency.')

        request_message = chat.chat_element_by_text(request_amount)
        if not request_message.is_element_displayed() and not request_message.contains_text(default_currency):
            self.errors.append('Wrong fiat value while requesting assets in 1-1 chat with default currency.')

        chat.get_back_to_home_view()

        # Switch default currency to user-selected
        wallet_view = sigin_view.wallet_button.click()
        wallet_view.set_currency(user_currency)
        wallet_view.get_back_to_home_view()

        chat = home_view.get_chat_with_user(recipient_user_name).click()

        # Check whether the fiat currency value of the messages sent is not changed to user-selected
        send_message = chat.chat_element_by_text(send_amount)
        if not send_message.is_element_displayed() and not send_message.contains_text(default_currency):
            self.errors.append('Wrong fiat value while sending assets in 1-1 chat with default currency.')

        request_message = chat.chat_element_by_text(request_amount)
        if not request_message.is_element_displayed() and not request_message.contains_text(default_currency):
            self.errors.append('Wrong fiat value while requesting assets in 1-1 chat with default currency.')

        # Send and request some tokens in 1x1 chat and check whether the fiat currency value of
        # the new messages is equal to user-selected
        send_amount, request_amount = [chat.get_unique_amount() for _ in range(2)]
        chat.send_transaction_in_1_1_chat('STT', send_amount)
        chat.request_transaction_in_1_1_chat('STT', request_amount)

        send_message = chat.chat_element_by_text(send_amount)
        if not send_message.is_element_displayed() and not send_message.contains_text(user_currency):
            self.errors.append('Wrong fiat value while sending assets in 1-1 chat with user selected currency.')

        request_message = chat.chat_element_by_text(request_amount)
        if not request_message.is_element_displayed() and not request_message.contains_text(user_currency):
            self.errors.append('Wrong fiat value while requesting assets in 1-1 chat with user selected currency.')

        # disabled since after merge https://github.com/status-im/status-react/pull/8425 no messages are shown
        # in 1-1 chat after sending from wallet

        # chat.get_back_to_home_view()
        #
        # wallet = home_view.wallet_button.click()
        # send_amount, request_amount = [chat.get_unique_amount() for _ in range(2)]

        # Send and request some tokens from wallet and check whether the fiat currency value of
        # the new messages is equal to user-selected
        #
        # wallet.send_transaction(asset_name='STT', recipient=recipient_user_name, amount=send_amount)
        # wallet.receive_transaction(asset_name='STT', recipient=recipient_user_name, amount=request_amount)
        #
        # wallet.get_back_to_home_view()
        # chat = home_view.get_chat_with_user(recipient_user_name).click()
        #
        # send_message = chat.chat_element_by_text(send_amount)
        # if not send_message.is_element_displayed() and not send_message.contains_text(user_currency):
        #     self.errors.append('Wrong fiat value while sending assets from wallet with user selected currency.')
        #
        # request_message = chat.chat_element_by_text(request_amount)
        # if not request_message.is_element_displayed() and not request_message.contains_text(user_currency):
        #     self.errors.append('Wrong fiat value while requesting assets from wallet with user selected currency.')

        self.errors.verify_no_errors()

    @marks.testrail_id(5782)
    @marks.critical
    def test_install_pack_and_send_sticker(self):
        sign_in = SignInView(self.driver)
        home = sign_in.create_user()

        sign_in.just_fyi('join public chat and check that stickers are not available on Ropsten')
        chat_name = home.get_public_chat_name()
        home.join_public_chat(chat_name)
        chat = sign_in.get_chat_view()
        if chat.show_stickers_button.is_element_displayed():
            self.errors.append('Sticker button is shown while on Ropsten')

        sign_in.just_fyi('switch to mainnet')
        chat.get_back_to_home_view()
        profile = home.profile_button.click()
        profile.switch_network('Mainnet with upstream RPC')
        home.get_chat_with_user('#' + chat_name).click()

        sign_in.just_fyi('install free sticker pack and use it in public chat')
        chat.show_stickers_button.click()
        chat.get_stickers.click()
        chat.install_sticker_pack_by_name('Status Cat')
        chat.back_button.click()
        time.sleep(2)
        chat.swipe_left()
        chat.sticker_icon.click()
        if not chat.chat_item.is_element_displayed():
            self.errors.append('Sticker was not sent')
        chat.swipe_right()
        if not chat.sticker_icon.is_element_displayed():
            self.errors.append('Sticker is not shown in recently used list')
        self.errors.verify_no_errors()

    @marks.testrail_id(5783)
    @marks.critical
    def test_can_use_purchased_stickers_on_recovered_account(self):
        sign_in_view = SignInView(self.driver)
        home_view = sign_in_view.recover_access(ens_user['passphrase'])

        sign_in_view.just_fyi('switch to Mainnet')
        profile_view = home_view.profile_button.click()
        profile_view.switch_network('Mainnet with upstream RPC')

        sign_in_view.just_fyi('join to public chat, buy and install stickers')
        chat = home_view.join_public_chat(home_view.get_public_chat_name())
        chat.show_stickers_button.click()
        chat.get_stickers.click()
        chat.install_sticker_pack_by_name('Tozemoon')
        chat.back_button.click()

        sign_in_view.just_fyi('check that can use installed pack')
        time.sleep(2)
        chat.swipe_left()
        chat.sticker_icon.click()
        if not chat.chat_item.is_element_displayed():
            self.driver.fail('Sticker was not sent')

    @marks.testrail_id(5403)
    @marks.critical
    def test_start_chat_with_ens(self):
        sign_in = SignInView(self.driver)
        home = sign_in.create_user()
        profile = home.profile_button.click()
        profile.switch_network('Mainnet with upstream RPC')
        chat = home.add_contact(ens_user['ens'])
        if not chat.element_by_text(ens_user['username']).is_element_displayed():
            self.driver.fail('Wrong user is resolved from username when starting 1-1 chat.')
