"""Auto like your [wo]man's pictures on instagram.

Classes:
    BaeFinder(object): Handle communication with Instagram.
Functions:
    config(): Specify the configuration for BaeFinder().
    main(): Summon BaeFinder().
"""
from time import sleep

from selenium import webdriver as WEB
# from selenium.webdriver import common as COM


class BaeFinder(object):
    """Search Instagram for Bae and like their un-liked pictures.

    Parameters defined in the config (tuple) parameter are unpacked into each
    of BeaFinder's attributes.

    Attributes:
        bae (str): The username of the target bae.
        user (str): The username of the user.
        __password (str): The password of the user.
        MODE (str): The mode in which to run BaeFinder() (default='N').
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
        """Return basic information carried by BaeFinder."""
        return f"""
        ::Session info::
        User: {self.user}
        Bae: {self.bae}
        Mode: Spectator (current default)
        Browser: FireFox (Geckodriver)
        """

    def log_in(self, refresh: float=3.00) -> None:
        """Open browser, log into Instagram, and navigate to target.

        Args:
            refresh: Seconds to sleep between pages (default=3.00).
        """
        GRAM = "https://www.instagram.com/accounts/login/?source=auth_switcher"
        TARGET = f"https://www.instagram.com/{self.bae}/"
        # Welcome message
        message = f"Welcome to InstaBae {self.user}!"
        wrap = '=' * len(message)
        title = f"\n{wrap}\n{message}\n{wrap}"

        # Open browser -> Instagram
        print(title)
        self.DRIVER.get(GRAM)
        sleep(refresh)

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
        sleep(refresh)
        # TODO Handle TARGET not being found (incorrect username)
        print("Profile located.")

    def scroll_and_grab(self) -> None:
        """Scroll to page bottom and return a set of all picture hrefs."""
        POSTS = self.DRIVER.find_element_by_class_name("g47SY ")
        TOTAL = int(POSTS.get_attribute("textContent"))
        links = []

        print(f"Total posts: {TOTAL}\n")
        print("Gathering post information...")
        while True:
            # Add all currently 'visible' posts to the list
            path = "//div[@class='Nnq7C weEfm']//descendant::a"

            for post in self.DRIVER.find_elements_by_xpath(path):
                href = post.get_attribute("href")

                if href not in links:
                    # Scroll to element
                    self.DRIVER.execute_script("arguments[0].scrollIntoView();", post)
                    links.append(href)
            if len(links) == TOTAL:
                break
        print(f"Gathered posts: {len(links)}")

    def log_out(self, refresh: float=3.00) -> None:
        """Log out and close the browser.

        Args:
            refresh: Seconds to sleep between pages (default=3.00).
        """
        print("Logging out...")
        HOME = f"https://www.instagram.com/{self.user}/"
        SETTINGS = "//button[@class='dCJp8 afkep _0mzm-']"
        LOG_OUT = "//button[text()='Log Out']"

        # Nav to USER's profile
        self.DRIVER.get(HOME)
        sleep(3)
        # Find settings
        self.DRIVER.find_element_by_xpath(SETTINGS).click()
        # Loggout and close browser.
        self.DRIVER.find_element_by_xpath(LOG_OUT).click()
        sleep(refresh)
        self.DRIVER.quit()
        print("Session closed successfully!")


def config() -> tuple:
    """Prompt for user input and return the configuration.

    To be used in conjunction with BaeFinder(), by providing the necessary
    target/user information, run-mode, and driver.

    Returns:
        A tuple containing the configuration for Baefinder().
    """
    # Configuration prompts
    bae = input("\nEnter the username of your bae: ")
    user = input("Enter your username: ")
    password = input("Enter your password: ")
    mode = None  # TODO To be added later.
    driver = WEB.Firefox(executable_path="../drivers/geckodriver.exe")

    return (bae, user, password, mode, driver)


def main() -> None:
    """Summon BaeFinder."""
    session = BaeFinder(config())

    print(session)
    session.log_in()
    # TODO Find the total number of 'liked' pictures
    try:
        session.scroll_and_grab()
    except Exception:
        print("Something went wrong")
    finally:
        session.log_out()
    # TODO Like un-liked pictures
    # TODO Like each un-liked pictures

if __name__ == "__main__":
    main()
