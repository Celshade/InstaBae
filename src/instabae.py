"""Automatically like Bae's posts on instagram.

Classes:
    BaeFinder(object): Communicate with Instagram.
Functions:
    config(): Specify the configuration for BaeFinder().
    main(): Summon BaeFinder().
"""
import os
import time
from getpass import getpass
from textwrap import dedent

from selenium import webdriver as WEB


class BaeFinder(object):
    """Search Instagram for Bae and like their posts.

    BaeFinder takes two parameters, 'settings' and 'driver'. Objects defined in
    the 'settings' parameter are unpacked into each of BaeFinder's attributes.
    The 'driver' parameter contains the file path to the default driver.

    Attributes:
        MODE (str): The mode in which to run.
        BAE (str): The username of the target.
        POSTS (int/str): The number of posts to like or 'A' for ALL posts.
        USER (str): The username of the user.
        PWD (str): The password of the user.
        DRIVER (webdriver): The driver to utilize.
    Public Methods:
        log_in(): Log into Instagram.
        locate(): Navigate to the target page.
        get_totals(): Gather the total number of posts.
        scroll_and_grab(): Scroll through the feed and gather posts.
        like_posts(): Like the gathered posts.
        log_out(): Log out of Instagram and close the browser session.
    """

    def __init__(self, settings: tuple, driver: str) -> None:
        self.MODE, self.BAE, self.POSTS, self.USER, self.PWD = settings
        self.DRIVER = WEB.Firefox(executable_path=driver)
        self._total, self._depth = None, None
        self._links = []

        if self.MODE == 'N':
            # TODO Add 'N' MODE
            raise NotImplementedError

    def __repr__(self) -> str:
        """Return session information."""
        return dedent(f"""\n
        ===================================
        <<Session Info>>
        User: {self.USER}
        Bae: {self.BAE}
        Search Depth: {"All" if self.POSTS == 'A' else self.POSTS}
        Mode: Spectator (current default)
        Browser: FireFox (geckodriver)\n
        ===================================
        """)

    def log_in(self, wait: float=2.25) -> None:
        """Open browser and log into Instagram.

        Args:
            wait: Seconds to sleep before page refresh (default=2.0).
        """
        # Open browser -> Instagram
        GRAM = "https://www.instagram.com/accounts/login/?source=auth_switcher"
        self.DRIVER.get(GRAM)
        time.sleep(wait)

        # Log in
        print("Logging in...")
        username = self.DRIVER.find_element_by_name("username")
        password = self.DRIVER.find_element_by_name("password")
        username.send_keys(self.USER)
        password.send_keys(self.PWD)
        password.submit()
        time.sleep(wait)
        # TODO Handle incorrect user/password

    def locate(self, wait: float=2.0) -> None:
        """Navigate to the target page.

        Args:
            wait: Seconds to sleep before page refresh (default=2.0)
        """
        print(f"Locating {self.BAE}...")
        TARGET = f"https://www.instagram.com/{self.BAE}/"

        self.DRIVER.get(TARGET)
        time.sleep(wait)
        print("Profile located.")
        # TODO Handle TARGET not being found (incorrect username for BAE)

    def get_totals(self) -> None:
        """Set the total number of posts and search depth."""
        POSTS = self.DRIVER.find_element_by_class_name("g47SY ")
        self._total = int(POSTS.get_attribute("textContent").replace(',', ''))
        self._depth = self._total if self.POSTS == 'A' else self.POSTS
        print(f"Total posts: {self._total}\n")

    def scroll_and_grab(self) -> None:
        """Scroll through the feed and build a list of posts."""
        print("Gathering post information...")
        gather = True

        while gather is True:
            href_path = "//div[@class='v1Nh3 kIKUG  _bz0w']/child::a"
            href_bundle = self.DRIVER.find_elements_by_xpath(href_path)

            # Scroll to and grab posts
            for post in href_bundle:
                href = post.get_attribute("href")
                if href not in self._links:
                    # Scroll to element and add href to links
                    JS_SCROLL_TO = "arguments[0].scrollIntoView();"
                    self.DRIVER.execute_script(JS_SCROLL_TO, post)
                    self._links.append(href)

            if len(self._links) >= self._depth:
                gather = False

    def like_posts(self) -> None:
        """Inspect and 'like' each post."""
        print(f"Checking the [{self._depth}] most recent posts...")
        posts_liked = 0

        for link in self._links[:self._depth]:
            self.DRIVER.get(link)
            HEART_PATH = "//div[@class='QBdPU ']"
            heart = self.DRIVER.find_element_by_xpath(HEART_PATH)
            if heart.get_attribute("aria-label") == "Like":
                heart.click()
                posts_liked += 1

        if posts_liked > 0:
            print(f"Posts liked: {posts_liked}")
        else:
            print("No new posts found!")

    def log_out(self, wait: float=2.0) -> None:
        """Log out and close the browser.

        Args:
            wait: Seconds to sleep before page refresh (default=2.0)
        """
        print("\nLogging out...")
        HOME = f"https://www.instagram.com/{self.USER}/"
        OPTIONS = "//div[@class='AFWDX']"
        LOG_OUT = "//button[text()='Log Out']"

        # Nav to USER's profile
        self.DRIVER.get(HOME)
        time.sleep(wait)

        # Loggout and close browser.
        self.DRIVER.find_element_by_xpath(OPTIONS).click()
        time.sleep(1)
        self.DRIVER.find_element_by_xpath(LOG_OUT).click()
        time.sleep(wait)
        self.DRIVER.quit()
        print("Session closed successfully!", end='\n')


def config() -> tuple:
    """Configure and return session information for BaeFinder()."""
    print(dedent("""
    ----------------------------CONFIGURATION---------------------------------
    MODE  << **Not yet implemented**
             Enter 'S' for SPECTATOR mode or 'N' for NINJA mode.
             SPECTATOR shows the process of Instabae. NINJA runs silently.
    BAE   << Enter the username of your target.
    POSTS << Enter a whole number (no punctuation) or 'A' for ALL.
             (Instabae looks at the most recent posts first.)

             **WARNING** Selecting 'A' searches ALL of the target's posts.
             Depending on the total number of posts, this may take a while.
    USER  << Enter your username.
    PWD   << Enter your password.
    --------------------------------------------------------------------------

    <<Please configure your session>>
    """), end='\n')

    MODE = 'S'  # TODO Remove default
    print(f"Enter your MODE: {MODE}")  # TODO Convert to input()
    BAE = input("Enter the username of your BAE: ")
    POSTS = input("Enter the number of POSTS to like: ")
    USER = input("Enter your USERNAME: ")
    PASSWORD = getpass("Enter your PASSWORD: ")

    # Optimize POSTS
    optimized = False
    while optimized is False:
        try:
            POSTS = 'A' if POSTS.upper() == 'A' else int(POSTS)
            optimized = True
        except ValueError:
            print("Please enter a valid number or 'A' to search ALL posts.")
            POSTS = input("Enter the number of POSTS to like: ")

    # Attempt to clear the terminal window
    try:
        os.system("cls||clear")
    finally:
        return (MODE, BAE, POSTS, USER, PASSWORD)


def main() -> None:
    """Summon BaeFinder()."""
    message = f"Welcome to InstaBae!"
    wrap = '=' * len(message)
    WELCOME = f"\n{wrap}\n{message}\n{wrap}\n"
    print(WELCOME)
    session = BaeFinder(config(), "../drivers/geckodriver.exe")

    # Run session.
    try:
        print(session)
        session.log_in()
        session.locate()
        session.get_totals()
        session.scroll_and_grab()
        session.like_posts()
    finally:
        session.log_out()


if __name__ == "__main__":
    main()
