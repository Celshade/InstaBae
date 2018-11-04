"""Auto like your [wo]man's pictures on instagram."""
from time import sleep

from selenium import webdriver

# Set user/password/target values prior to opening browser
USER = input("Enter username: ")
PASSWORD = input("Enter password: ")
BAE = input("Enter bae's username: ")
# TODO Add 'modes' ('S' for Spectator mode | 'N' for Ninja mode)

# Useful constants.
GECKO = "../drivers/geckodriver.exe"
GRAM = "https://www.instagram.com/accounts/login/?source=auth_switcher"
TARGET = f"https://www.instagram.com/{BAE}/"
ME = f"https://www.instagram.com/{USER}/"

# TODO def driver(browser: str="FireFox") # select necessary driver
driver = webdriver.Firefox(executable_path=GECKO)
# TODO Add additional driver support for IE and Chrome.

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

# Find the total number of pictures
_ = driver.find_element_by_class_name("g47SY ")
total = _.get_attribute("textContent")

try:
    # TODO Find the total number of 'liked' pictures
    # Get current page height

    # Scroll to bottom of page
    while True:
        height = driver.execute_script("return document.body.scrollHeight")
        print(f"0riginal: {height}")
        # Scroll to current bottom
        scroll = "window.scrollTo(0, document.body.scrollHeight);"
        driver.execute_script(scroll)
        sleep(1)

        # Compare height values
        current = driver.execute_script("return document.body.scrollHeight")
        print(f"0riginal: {current}\n------------")
        if current == height:
            break
        else:
            height = current
    sleep(1)

    # TODO Like un-liked pictures
    # TODO Like each un-liked pictures
except Exception:
    print("Something went wrong")
finally:
    # ### Logging out and closing the browser ### #
    # Nav to USER's profile
    driver.get(ME)
    sleep(3)
    # Find settings
    settings = "//button[@class='_0mzm- dCJp8']"
    driver.find_element_by_xpath(settings).click()
    # Loggout and close browser.
    loggout = "//button[text()='Log Out']"
    driver.find_element_by_xpath(loggout).click()
    sleep(3)
    driver.quit()
