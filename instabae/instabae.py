"""Auto like your [wo]man's pictures on instagram."""
from time import sleep

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Set user/password/target values prior to opening browser
USER = input("Enter username: ")
PASSWORD = input("Enter password: ")
BAE = input("Enter bae's username: ")

# Designate firefox as browser and open window
GECKO = "../drivers/geckodriver.exe"
driver = webdriver.Firefox(executable_path=GECKO)
# TODO add additional drivers for IE and Chrome

# Log into insta and find bae
GRAM = "https://www.instagram.com/accounts/login/?source=auth_switcher"
driver.get(GRAM)
sleep(3)

username = driver.find_element_by_name('username')
password = driver.find_element_by_name('password')
username.send_keys(USER)
password.send_keys(PASSWORD)
password.submit()
sleep(3)
# TODO Raise an exception if user/password is incorrect

TARGET = f"https://www.instagram.com/{BAE}/"
driver.get(TARGET)
sleep(2)
# TODO Raise an exception if target user is not found

# TODO
# Find the total amount of pictures
# Find the total amount of pictures liked
# Like the link of un-liked pictures
# Like each un-liked pictures

# Logging out and closing the browser
ME = f"https://www.instagram.com/{USER}/"
driver.get(ME)
sleep(3)

settings = "/html/body/span/section/main/div/header/section/div[1]/div/button"
driver.find_element_by_xpath(settings).click()

loggout = "/html/body/div[3]/div/div/div/div/button[6]"
driver.find_element_by_xpath(loggout).click()
sleep(3)
driver.quit()
