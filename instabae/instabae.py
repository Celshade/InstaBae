"""Auto like your [wo]man's pictures on instagram.

Classes:
    BaeFinder(object): Handle communication with Instagram.
Functions:
    # TODO
Attributes:
    # TODO
"""
from time import sleep

from selenium import webdriver

# Drivers
GECKO = "../drivers/geckodriver.exe"


class BaeFinder(object):
    """Search Instagram for BAE and like their un-liked pictures.

    Attributes:
        # TODO
        TARGET: The username of your target.
    Public Methods:
        log_in(): Log into Instagram.
        scroll_and_grab(): Scroll through the page and gather post info.
        log_out(): Log out of Instagram and close the browser session.
    """

    def __init__(self) -> None:
        self.BAE = input("Enter the username of bae: ")
        self.USER = input("Enter your username: ")
        self._PASSWORD = input("Enter your password: ")
        self.DRIVER = webdriver.Firefox(executable_path=GECKO)
        # TODO Add additional driver support for IE and Chrome.
        # TODO Add function to select driver [browser] of choice
        # TODO Add 'modes' ('S' for Spectator mode | 'N' for Ninja mode)

    def __repr__(self) -> str:
        """Return basic information carried by BaeFinder."""
        pass

    def log_in(self, speed: float=3.00) -> None:
        """Open browser, log into Instagram, and navigate to target.

        Args:
            speed: Seconds to sleep (refresh) between pages.
        """
        GRAM = "https://www.instagram.com/accounts/login/?source=auth_switcher"
        TARGET = f"https://www.instagram.com/{self.BAE}/"

        # Open browser -> Instagram
        self.DRIVER.get(GRAM)
        sleep(3)

        # Log in
        username = self.DRIVER.find_element_by_name("username")
        password = self.DRIVER.find_element_by_name("password")
        username.send_keys(self.USER)
        password.send_keys(self._PASSWORD)
        del self._PASSWORD
        password.submit()
        sleep(3)
        # TODO Handle incorrect user/password

        # Navigate to target page
        self.DRIVER.get(TARGET)
        sleep(3)
        # TODO Handle TARGET not being found (incorrect username)

    def scroll_and_grab(self, speed: float=2.00) -> set:
        """Scroll to page bottom and return a set of all picture hrefs.

        Args:
            speed: Seconds to sleep after each scroll (default=2.00).
        """
        links = set()  # Automatically filter duplicates

        while True:
            # Add all currently 'visible' posts to the list
            path = "//div[@class='Nnq7C weEfm']//descendant::a"
            for x in self.DRIVER.find_elements_by_xpath(path):
                links.add(x.get_attribute('href'))

            # Get current page height and scroll to the bottom of the page
            js_height = "return document.body.scrollHeight"
            js_scroll = "window.scrollTo(0, document.body.scrollHeight);"
            height = self.DRIVER.execute_script(js_height)
            self.DRIVER.execute_script(js_scroll)
            sleep(speed)  # Allow refreshing

            # Compare height values
            current = self.DRIVER.execute_script(js_height)
            if current == height:
                break
            else:
                height = current
        sleep(1)
        return links

    def log_out(self, speed: float=3.00) -> None:
        """Loggout and close the browser.

        Args:
            speed: Seconds to sleep (refresh) between pages (default=3).
        """
        HOME = f"https://www.instagram.com/{self.USER}/"
        SETTINGS = "//button[@class='_0mzm- dCJp8']"
        LOG_OUT = "//button[text()='Log Out']"

        # Nav to USER's profile
        self.DRIVER.get(HOME)
        sleep(3)
        # Find settings
        self.DRIVER.find_element_by_xpath(SETTINGS).click()
        # Loggout and close browser.
        self.DRIVER.find_element_by_xpath(LOG_OUT).click()
        sleep(3)
        self.DRIVER.quit()

    def test(self) -> str:
        """Test"""
        # Find the total number of pictures
        POSTS = self.DRIVER.find_element_by_class_name("g47SY ")
        TOTAL = POSTS.get_attribute("textContent")
        print(f"\nTotal posts: {TOTAL}")

        # TODO Find the total number of 'liked' pictures
        try:
            # Scroll to bottom of page and build a list of picture hrefs
            pics = self.scroll_and_grab()
            print(f"Pictures found: {len(pics)}")
        except Exception:
            print("Something went wrong")
        finally:
            self.log_out()

        # TODO Like un-liked pictures
        # TODO Like each un-liked pictures


if __name__ == "__main__":
    main = BaeFinder()
    main.log_in()
    main.test()
    main.log_out
