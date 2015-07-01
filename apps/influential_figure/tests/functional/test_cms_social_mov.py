from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from django.test import LiveServerTestCase

def login_as_admin(liveServer, username, password):
    liveServer.browser.get(liveServer.live_server_url + '/admin/')
    username_field = liveServer.browser.find_element_by_name('username')
    username_field.send_keys('nina')
    password_field = liveServer.browser.find_element_by_name('password')
    password_field.send_keys('nina')
    password_field.send_keys(Keys.RETURN)

def create_social_movement(liveServer, socialMovementName):
    add_sm_button = liveServer.browser.find_element_by_xpath('//*[@id="content-main"]/div[2]/table/tbody/tr/td[1]/a')
    add_sm_button.click()
    sm_name_field = liveServer.browser.find_element_by_name('name')
    sm_name_field.send_keys(socialMovementName)
    sm_save_button = liveServer.browser.find_element_by_name('_save')
    sm_save_button.click()

    body = liveServer.browser.find_element_by_tag_name('body')
    liveServer.assertIn('The social movement "' + socialMovementName + '" was added successfully.', body.text)

def update_social_movement(liveServer, oldSocialMovementName, newSocialMovementName):
    select_sm = liveServer.browser.find_element_by_link_text(oldSocialMovementName)
    select_sm.click()
    sm_name_field = liveServer.browser.find_element_by_name('name')
    sm_name_field.clear()
    sm_name_field.send_keys(newSocialMovementName)
    sm_save_button = liveServer.browser.find_element_by_name('_save')
    sm_save_button.click()

    body = liveServer.browser.find_element_by_tag_name('body')
    liveServer.assertIn('The social movement "' + newSocialMovementName + '" was changed successfully.', body.text)

def delete_social_movement(liveServer, socialMovement):
    select_sm = liveServer.browser.find_element_by_link_text(socialMovement)
    select_sm.click()
    delete_button = liveServer.browser.find_element_by_link_text('Delete')
    delete_button.click()
    confirm_button = liveServer.browser.find_element_by_xpath('//*[@id="content"]/form/div/input[2]')
    confirm_button.click()

    body = liveServer.browser.find_element_by_tag_name('body')
    liveServer.assertIn('The social movement "' + socialMovement + '" was deleted successfully.', body.text)

class SocialMovementTest(LiveServerTestCase):

    fixtures = ['admin.json']

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_create_sm(self):
        login_as_admin(self, 'nina', 'nina')
        expected_social_movement = 'SocialMovimentNameTest'

        create_social_movement(self, expected_social_movement)

        expected_social_movement_changed = 'SocialMovimentNameTestChanged'
        update_social_movement(self, expected_social_movement, expected_social_movement_changed)

        delete_social_movement(self, expected_social_movement_changed)