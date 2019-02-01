"""Auto like your [wo]man's pictures on instagram.

Classes:
    BaeFinder(object): Handle communication with Instagram.
Functions:
    config(): Specify the configuration for BaeFinder().
    main(): Summon BaeFinder().
"""
from time import sleep

from selenium import webdriver as WEB
from selenium.webdriver import common as COM


class BaeFinder(object):
    """Search Instagram for Bae and like their un-liked pictures.

    Parameters defined in the config parameter are unpacked into each
    of BeaFinder's attributes.

    Attributes:
        bae (str): The username of the target.
        user (str): The username of the user.
        __password (str): The password of the user.
        MODE (str): The mode in which to run.
        DRIVER (webdriver): The driver to utilize.
    Public Methods:
        log_in(): Log into Instagram.
        scroll_and_grab(): Scroll through the page and gather post information.
        log_out(): Log out of Instagram and close the browser session.
    """

    def __init__(self, config: tuple) -> None:
        self.bae, self.user, self.__password, self.MODE, self.DRIVER = config
        # TODO Add 'modes' ('S' for Spectator mode | 'N' for Ninja mode)

    def __repr__(self) -> str:
        """Return session information."""
        return f"""
        ::Session info::
        User: {self.user}
        Bae: {self.bae}
        Mode: Spectator (current default)
        Browser: FireFox (Geckodriver)
        """

    def log_in(self, wait: float=3.00) -> None:
        """Open browser, log into Instagram, and navigate to target.

        Args:
            wait: Seconds to sleep between pages (default=3.00).
        """
        GRAM = "https://www.instagram.com/accounts/login/?source=auth_switcher"
        TARGET = f"https://www.instagram.com/{self.bae}/"
        message = f"Welcome to InstaBae {self.user}!"
        wrap = '=' * len(message)
        title = f"\n{wrap}\n{message}\n{wrap}"

        # Open browser -> Instagram
        print(title)
        self.DRIVER.get(GRAM)
        sleep(wait)

        # Log in
        print("Logging in...")
        username = self.DRIVER.find_element_by_name("username")
        password = self.DRIVER.find_element_by_name("password")
        username.send_keys(self.user)
        password.send_keys(self.__password)
        password.submit()
        sleep(3)
        # TODO Handle incorrect user/password

        # Navigate to target page
        print(f"Locating {self.bae}...")
        self.DRIVER.get(TARGET)
        sleep(wait)
        # TODO Handle TARGET not being found (incorrect username)
        print("Profile located.")

    def scroll_and_grab(self) -> None:
        """Scroll to page bottom and collect a list of all picture hrefs."""
        POSTS = self.DRIVER.find_element_by_class_name("g47SY ")
        TOTAL = int(POSTS.get_attribute("textContent").replace(",", ""))
        links = []

        print(f"Total posts: {TOTAL}\n")
        print("Gathering post information...")
        while True:
            # TODO Like un-liked pictures
            # ACTIONS = WEB.ActionChains(self.DRIVER)
            # ESC = COM.keys.Keys.ESCAPE
            href_path = "//div[@class='v1Nh3 kIKUG  _bz0w']/child::a"
            # For zipping href nodes with clickable post nodes
            click_path = "//div[@class='eLAPa']"
            href_bundle = self.DRIVER.find_elements_by_xpath(href_path)
            click_bundle = self.DRIVER.find_elements_by_xpath(click_path)

            # Gather all currently 'visible' posts
            # for post in self.DRIVER.find_elements_by_xpath(href_path):
            for post, clicker in zip(href_bundle, click_bundle):
                href = post.get_attribute("href")  # The full href
                sub_index = href.index("/p")
                suffix = href[sub_index:]  # The href suffix

                if suffix not in links:
                    # Scroll to element and add suffix to links
                    JS_SCROLL_TO = "arguments[0].scrollIntoView();"
                    self.DRIVER.execute_script(JS_SCROLL_TO, post)
                    links.append(suffix)
                    print(suffix)

                    # TODO click and close elements
                    # self.DRIVER.find_element_by_tag_name("body")
                    # ACTIONS.send_keys(COM.keys.Keys.COMMAND + 't').perform()
                    # self.DRIVER.find_element_by_tag_name("body")
                    # ACTIONS.send_keys(COM.keys.Keys.COMMAND + 'w').perform()

                    # clicker.click()  # BUG This works, but SLOWLY!
                    # heart_class = 'dCJp8 afkep coreSpriteHeartOpen _0mzm-'
                    # heart_path = f"//button[@class={heart_class}]"
                    # heart = self.DRIVER.find_element_by_xpath(heart_path)

            if len(links) == TOTAL:
                break
        print(f"Gathered posts: {len(links)}")

    def log_out(self, wait: float=3.00) -> None:
        """Log out and close the browser.

        Args:
            wait: Seconds to sleep between pages (default=3.00).
        """
        print("Logging out...")
        HOME = f"https://www.instagram.com/{self.user}/"
        SETTINGS = "//button[@class='dCJp8 afkep _0mzm-']"
        LOG_OUT = "//button[text()='Log Out']"

        # Nav to USER's profile
        self.DRIVER.get(HOME)
        sleep(wait)
        # Find settings
        self.DRIVER.find_element_by_xpath(SETTINGS).click()
        # Loggout and close browser.
        self.DRIVER.find_element_by_xpath(LOG_OUT).click()
        sleep(wait)
        self.DRIVER.quit()
        print("Session closed successfully!")


def config() -> tuple:
    """Prompt for user input and return the configuration.

    To be used in conjunction with BaeFinder(), by providing the necessary
    target/user information, run-mode, and driver.
    """
    # Configuration prompts
    bae = input("\nEnter the username of your bae: ")
    user = input("Enter your username: ")
    password = input("Enter your password: ")
    mode = None  # TODO To be added later.
    driver = WEB.Firefox(executable_path="../drivers/geckodriver.exe")

    return (bae, user, password, mode, driver)


# Testing purposes only
def main() -> None:
    """Summon BaeFinder."""
    session = BaeFinder(config())

    print(session)
    session.log_in()
    try:
        session.scroll_and_grab()
    finally:
        session.log_out()


if __name__ == "__main__":
    main()
