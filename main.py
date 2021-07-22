from selenium import webdriver
import pathlib
import os
import antiCaptcha
import time
import configparser
import logging



def main():
    logging.basicConfig(filename='log.txt', level=logging.INFO)

    config = configparser.ConfigParser()
    config.read("config.ini")

    driver_path = config.get("ChromeDriver", "path")
    driver = webdriver.Chrome(driver_path)
    logging.info('Chrome Driver loaded at %s', driver_path)

    driver.get('https://www.1point3acres.com/bbs/member.php?mod=logging&action=login')

    # 1. Sign-in

    username_box = driver.find_element_by_name('username')
    username_box.send_keys(config.get("Account", "user"))

    password_box = driver.find_element_by_name('password')
    password_box.send_keys(config.get("Account", "password"))

    logging_button = driver.find_element_by_name('loginsubmit')
    logging_button.click()

    time.sleep(2)

    # 2. Get Daily Credit

    driver.get('https://www.1point3acres.com/bbs/dsu_paulsign-sign.html')

    emoji_selection =  driver.find_element_by_xpath("//li[@id='kx']")
    emoji_selection.click()

    mode_selection = driver.find_element_by_xpath("//input[@name = 'qdmode' and @type='radio' and @value='2']")
    mode_selection.click()

    refresh_captcha = driver.find_element_by_xpath("//a[@class='xi2']")
    refresh_captcha.click()

    # This wait time make sure the captcha is showing correctly
    time.sleep(3)

    captcha = driver.find_element_by_xpath("//span[@id='seccode_S00']/img[@class='vm']")
    captcha.screenshot("captcha.png")

    filePath = os.path.join(pathlib.Path().resolve(), 'captcha.png')
    result = antiCaptcha.parse_captcha(filePath, config.get("anti-captcha", "token"))

    logging.info("captcha: %s", result)

    captcha_box = driver.find_element_by_name('seccodeverify')
    captcha_box.send_keys(result)

    submit_button = driver.find_element_by_xpath("//input[@type='submit']")
    submit_button.click()

    time.sleep(3) # Let the user actually see something!
    logging.info("Sucess")
    driver.quit()
  

if __name__ == '__main__':
    main()