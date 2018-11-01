"""Auto like your [wo]man's pictures on instagram."""
from time import sleep

from selenium import webdriver

# Set user/password/target values prior to opening browser
USER = input("Enter username: ")
PASSWORD = input("Enter password: ")
BAE = input("Enter bae's username: ")
# TODO Add 'modes' ('S' for Spectator mode | 'N' for Ninja mode)

# Useful constants.
GECKO = ".//drivers/geckodriver.exe"
GRAM = "https://www.instagram.com/accounts/login/?source=auth_switcher"
TARGET = f"https://www.instagram.com/{BAE}/"
ME = f"https://www.instagram.com/{USER}/"

# TODO Add additional driver support for IE and Chrome.
# TODO def driver(browser: str="FireFox") # select necessary driver
driver = webdriver.Firefox(executable_path=GECKO)

# ### Open browser, log in, navigate to target. ### #
driver.get(GRAM)
sleep(3)

username = driver.find_element_by_name("username")
password = driver.find_element_by_name("password")
username.send_keys(USER)
password.send_keys(PASSWORD)
password.submit()
sleep(3)
# TODO Handle incorrect user/password

driver.get(TARGET)
sleep(3)
# TODO Handle TARGET not being found (incorrect username)

try:
    # Find the total amount of pictures
    total = driver.find_element_by_class_name("g47SY ")
    total = total.get_attribute("textContent")
    # TODO Find the total amount of pictures liked
    # TODO Like un-liked pictures
    # TODO Like each un-liked pictures

except Exception:
    print("Something went wrong")
finally:
    # ### Logging out and closing the browser ### #
    driver.get(ME)
    sleep(3)

    settings = "/html/body/span/section/main/div/header/section/div[1]/div/button"
    driver.find_element_by_xpath(settings).click()

    loggout = "/html/body/div[3]/div/div/div/div/button[6]"
    driver.find_element_by_xpath(loggout).click()
    sleep(3)
    driver.quit()
