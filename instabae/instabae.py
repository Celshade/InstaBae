"""Automatically like Bae's posts on instagram.

Classes:
    BaeFinder(object): Communicate with Instagram.
Functions:
    config(): Specify the configuration for BaeFinder().
    main(): Summon BaeFinder().
"""
from time import sleep
from textwrap import dedent

from selenium import webdriver as WEB


class BaeFinder(object):
    """Search Instagram for Bae and like their posts.

    Objects defined in the 'setting' parameter are unpacked into each
    of BeaFinder's attributes.

    Attributes:
        BAE (str): The username of the target.
        USER (str): The username of the user.
        PASSWORD (str): The password of the user.
        POSTS (int): The amount of posts to like.
        MODE (str): The mode in which to run.
        DRIVER (webdriver): The driver to utilize.
    Public Methods:
        log_in(): Log into Instagram.
        locate(): Navigate to the target page.
        get_totals(): Gather the total number of posts.
        scroll_and_grab(): Scroll through the feed and gather post information.
        like_posts(): Like the gathered posts.
        log_out(): Log out of Instagram and close the browser session.
    """
    # TODO Add ability to store last known total posts and date used.

    def __init__(self, settings: tuple) -> None:
        self.BAE, self.USER, self.PASSWORD, self.POSTS, self.MODE = settings
        self.DRIVER = WEB.Firefox(executable_path="../drivers/geckodriver.exe")
        self._links = []
        self._total = None
        self._depth = None

        if self.MODE == 'N':
            # TODO Add 'N' MODE
            raise NotImplementedError

    def __repr__(self) -> str:
        """Return session information."""
        return dedent(f"""
        [Session info]
        User: {self.USER}
        Bae: {self.BAE}
        Search Depth: {self.POSTS}
        Mode: Spectator (current default)
        Browser: FireFox (Geckodriver)\n
        """)

    def log_in(self, wait: float=2.0) -> None:
        """Open browser and log into Instagram.

        Args:
            wait: Seconds to sleep before page refresh (default=2.0).
        """
        # Open browser -> Instagram
        GRAM = "https://www.instagram.com/accounts/login/?source=auth_switcher"
        self.DRIVER.get(GRAM)
        sleep(wait)

        # Log in
        print("Logging in...")
        username = self.DRIVER.find_element_by_name("username")
        password = self.DRIVER.find_element_by_name("password")
        username.send_keys(self.USER)
        password.send_keys(self.PASSWORD)
        password.submit()
        sleep(wait)
        # TODO Handle incorrect user/password

    def locate(self, wait: float=2.0) -> None:
        """Navigate to the target page.

        Args:
            wait: Seconds to sleep before page refresh (default=2.0)
        """
        TARGET = f"https://www.instagram.com/{self.BAE}/"
        print(f"Locating {self.BAE}...")
        self.DRIVER.get(TARGET)
        sleep(wait)
        # TODO Handle TARGET not being found (incorrect username)
        print("Profile located.")

    def get_totals(self) -> None:
        """Set the total number of posts and search depth."""
        POSTS = self.DRIVER.find_element_by_class_name("g47SY ")
        TOTAL = int(POSTS.get_attribute("textContent").replace(',', ""))
        print(f"Total posts: {TOTAL}\n")
        self._total = TOTAL
        self._depth = self._total if self.POSTS == 'A' else int(self.POSTS)

    def scroll_and_grab(self) -> list:
        """Scroll through the feed and gather a list of posts."""
        gather = True
        print("Gathering post information...")

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

            if len(self._links) > self._depth:
                gather = False
        print(f"Gathered posts: {len(self._links)}")

    def like_posts(self) -> None:
        """Inspect and 'like' each post."""
        posts_liked = 0
        for link in self._links[:self._depth]:
            self.DRIVER.get(link)
            heart_path = "//button[@class='dCJp8 afkep _0mzm-']/child::span"
            heart = self.DRIVER.find_element_by_xpath(heart_path)
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
        print("Logging out...")
        HOME = f"https://www.instagram.com/{self.USER}/"
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

    Used in conjunction with BaeFinder(), by providing the necessary
    session information.
    """
    # Introduction
    message = f"Welcome to InstaBae!"
    wrap = '=' * len(message)
    WELCOME = f"\n{wrap}\n{message}\n{wrap}\n"
    OPTIONS = dedent("""
    -----------------------------------------------------------------------
    MODE  << Enter 'S' for SPECTATOR mode or 'N' for NINJA mode.
             SPECTATOR shows the process of Instabae. NINJA runs silently.
    POSTS << Enter a whole number (no punctuation) or 'A' for ALL.
             (Instabae looks at the most recent posts first.)

             **WARNING** Selecting 'A' searches ALL of the target's posts.
             Depending on the total number of posts, this may take a while.
    -----------------------------------------------------------------------
    """)
    print(WELCOME, OPTIONS)

    # Configuration prompts
    MODE = 'S'  # Current default. TODO Add 'N' mode.
    print(f"\nEnter your MODE: {MODE}")  # TODO Remove once 'N' mode is added.
    BAE = input("Enter the username of your BAE: ")
    POSTS = input("Enter the number of POSTS to like: ")
    USER = input("Enter your USERNAME: ")
    PASSWORD = input("Enter your PASSWORD: ")

    return (BAE, USER, PASSWORD, POSTS, MODE)


def main() -> None:
    """Summon BaeFinder."""
    session = BaeFinder(config())

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
