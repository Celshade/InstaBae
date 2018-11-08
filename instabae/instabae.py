"""Auto like your [wo]man's pictures on instagram."""
from time import sleep

from selenium import webdriver

# Useful constants.
USER = input("Enter username: ")
PASSWORD = input("Enter password: ")
BAE = input("Enter bae's username: ")
GECKO = "../drivers/geckodriver.exe"
GRAM = "https://www.instagram.com/accounts/login/?source=auth_switcher"
TARGET = f"https://www.instagram.com/{BAE}/"
HOME = f"https://www.instagram.com/{USER}/"
DRIVER = webdriver.Firefox(executable_path=GECKO)
# TODO Add additional driver support for IE and Chrome.
# TODO Add function to select driver [browser] of choice
# TODO Add 'modes' ('S' for Spectator mode | 'N' for Ninja mode)


def scroll_and_grab(speed: float=2.00) -> set:
    """Scroll to the bottom of a page and return a set of all picture hrefs.

    Args:
        speed: Seconds to sleep after each scroll (default=1.00).
    """
    links = set()  # Automatically filter duplicates

    while True:
        # Add all currently 'visible' posts to the list
        path = "//div[@class='Nnq7C weEfm']//descendant::a"
        for x in DRIVER.find_elements_by_xpath(path):
            links.add(x.get_attribute('href'))

        # Get current page height and scroll to the bottom of the page
        height = DRIVER.execute_script("return document.body.scrollHeight")
        j_scroll = "window.scrollTo(0, document.body.scrollHeight);"
        DRIVER.execute_script(j_scroll)
        sleep(speed)  # Allow refreshing

        # Compare height values
        current = DRIVER.execute_script("return document.body.scrollHeight")
        if current == height:
            break
        else:
            height = current
    sleep(1)
    return links


def loggout(speed: float=3.00) -> None:
    """Loggout and close the browser.

    Args:
        speed: Seconds to sleep prior to accessing page 'settings' (default=3).
    """
    # Nav to USER's profile
    DRIVER.get(HOME)
    sleep(3)
    # Find settings
    settings = "//button[@class='_0mzm- dCJp8']"
    DRIVER.find_element_by_xpath(settings).click()
    # Loggout and close browser.
    loggout = "//button[text()='Log Out']"
    DRIVER.find_element_by_xpath(loggout).click()
    sleep(3)
    DRIVER.quit()


# ### Open browser, log in, navigate to target. ### #
DRIVER.get(GRAM)
sleep(3)

username = DRIVER.find_element_by_name("username")
password = DRIVER.find_element_by_name("password")
username.send_keys(USER)
password.send_keys(PASSWORD)
password.submit()
sleep(3)
# TODO Handle incorrect user/password

DRIVER.get(TARGET)
sleep(3)
# TODO Handle TARGET not being found (incorrect username)

# Find the total number of pictures
_ = DRIVER.find_element_by_class_name("g47SY ")
total = _.get_attribute("textContent")
print(f"\nTotal posts: {total}")

# TODO Find the total number of 'liked' pictures
try:
    # Scroll to bottom of page and build a list of picture hrefs
    pics = scroll_and_grab()
    print(f"Pictures found: {len(pics)}")
except Exception:
    print("Something went wrong")
finally:
    loggout()

# TODO Like un-liked pictures
# TODO Like each un-liked pictures
