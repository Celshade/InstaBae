"""Auto like your [wo]man's pictures on instagram.

Classes:
    BaeFinder(object): Communicate with Instagram.
Functions:
    config(): Specify the configuration for BaeFinder().
    main(): Summon BaeFinder().
"""
from time import sleep

from selenium import webdriver as WEB


class BaeFinder(object):
    """Search Instagram for Bae and like their posts.

    Objects defined in the 'settings' parameter are unpacked into each
    of BeaFinder's attributes.

    Attributes:
        DRIVER (webdriver): The driver to utilize.
        MODE (str): The mode in which to run.
        bae (str): The username of the target.
        depth (int): The amount of posts to like.
        user (str): The username of the user.
        passw (str): The password of the user.
    Public Methods:
        log_in(): Log into Instagram.
        get_total(): Gather the total number of posts.
        scroll_and_grab(): Scroll through the feed and gather post information.
        like_posts(): Like the gathered posts.
        log_out(): Log out of Instagram and close the browser session.
    """

    def __init__(self, settings: tuple) -> None:
        self.bae, self.user, self.passw, self.MODE, self.DRIVER = settings[1:]
        self.depth = settings[0]
        self._links = []

        if self.MODE == 'N':
            # TODO Add 'N' MODE
            raise NotImplementedError

    def __repr__(self) -> str:
        """Return session information."""
        return f"""\n
        [Session info]
        User: {self.user}
        Bae: {self.bae}
        Mode: Spectator (current default)
        Browser: FireFox (Geckodriver)\n"""

    def log_in(self, wait: float=2.00) -> None:
        """Open browser, log into Instagram, and navigate to target.

        Args:
            wait: Seconds to sleep between pages (default=2.00).
        """
        GRAM = "https://www.instagram.com/accounts/login/?source=auth_switcher"
        TARGET = f"https://www.instagram.com/{self.bae}/"

        # Open browser -> Instagram
        self.DRIVER.get(GRAM)
        sleep(wait)
        # Log in
        print("Logging in...")
        username = self.DRIVER.find_element_by_name("username")
        password = self.DRIVER.find_element_by_name("password")
        username.send_keys(self.user)
        password.send_keys(self.passw)
        password.submit()
        sleep(wait)
        # TODO Handle incorrect user/password

        # Navigate to target page
        print(f"Locating {self.bae}...")
        self.DRIVER.get(TARGET)
        sleep(wait)
        # TODO Handle TARGET not being found (incorrect username)
        print("Profile located.")

    def get_total(self) -> None:
        """Find and set the total number of posts."""
        POSTS = self.DRIVER.find_element_by_class_name("g47SY ")
        TOTAL = int(POSTS.get_attribute("textContent").replace(',', ""))
        print(f"Total posts: {TOTAL}\n")
        self.total = TOTAL

    def scroll_and_grab(self) -> list:
        """Scroll to page bottom and collect a list of all post links."""
        gather = True
        print("Gathering post information...")

        while gather is True:
            # TODO Like un-liked pictures
            href_path = "//div[@class='v1Nh3 kIKUG  _bz0w']/child::a"
            href_bundle = self.DRIVER.find_elements_by_xpath(href_path)

            # Scroll to and grab posts
            for post in href_bundle:
                href = post.get_attribute("href")  # The full href
                if href not in self._links:
                    # Scroll to element and add href to links
                    JS_SCROLL_TO = "arguments[0].scrollIntoView();"
                    self.DRIVER.execute_script(JS_SCROLL_TO, post)
                    self._links.append(href)

            if len(self._links) == self.total:
                gather = False
        print(f"Gathered posts: {len(self._links)}")

    def like_posts(self) -> None:
        """Inspect each post and attempt to 'like' it."""
        if self.depth == 'a':
            self.depth = self.total

        posts_liked = 0
        for link in self._links[:self.depth]:
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

    def log_out(self, wait: float=2.00) -> None:
        """Log out and close the browser.

        Args:
            wait: Seconds to sleep between pages (default=2.00).
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
    session information, run-mode, and driver.
    """
    message = f"Welcome to InstaBae!"
    wrap = '=' * len(message)
    title = f"\n{wrap}\n{message}\n{wrap}\n"
    print(title)

    # Configuration prompts
    MODE_TEXT = "('S' for Spectator mode | 'N' for Ninja mode):"
    DRIVER = WEB.Firefox(executable_path="../drivers/geckodriver.exe")
    MODE = input("\nEnter your desired MODE {MODE_TEXT}")
    BAE = input("\nEnter the username of your bae: ")
    DEPTH = input("Enter the number of posts to like ('A' for ALL -> SLOW!): ")
    USER = input("Enter your username: ")
    PASSWORD = input("Enter your password: ")

    depth = 'a' if depth.lower() == 'a' else int(depth)
    return (DRIVER, MODE, BAE, DEPTH, USER, PASSWORD)


def main() -> None:
    """Summon BaeFinder."""
    session = BaeFinder(config())

    try:
        print(session)
        session.log_in()
        session.get_total()
        session.scroll_and_grab()
        session.like_posts()
    finally:
        session.log_out()


if __name__ == "__main__":
    main()
