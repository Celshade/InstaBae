"""Auto like your [wo]man's pictures on instagram.

Classes:
    BaeFinder(object): Handle communication with Instagram.
Functions:
    config(): Specify the configuration for BaeFinder().
    main(): Summon BaeFinder().
"""
from time import sleep

from selenium import webdriver


class BaeFinder(object):
    """Search Instagram for Bae and like their un-liked pictures.

    Attributes:
        config: A tuple containing the configuration for BaeFinder().
        bae: The username of the target bae.
        user: The username of the user.
        __password: The password of the user.
        DRIVER: The specified driver to utilize.
    Public Methods:
        log_in(): Log into Instagram.
        scroll_and_grab(): Scroll through the page and gather posts.
        log_out(): Log out of Instagram and close the browser session.
        test(): Temporary handler of BaeFinder() methods.
    """

    def __init__(self, config: tuple) -> None:
        self.bae = config[0]
        self.user = config[1]
        self.__password = config[2]
        self.DRIVER = config[3]
        self.MODE = None  # Will be added later.
        # TODO Add 'modes' ('S' for Spectator mode | 'N' for Ninja mode)

    def __repr__(self) -> str:
        """Return basic information carried by BaeFinder."""
        return f"""
        \nSession info:
        User: {self.user}
        Bae: {self.bae}
        Driver: {type(self.DRIVER)}
        Mode: TBA
        """

    def log_in(self, speed: float=3.00) -> None:
        """Open browser, log into Instagram, and navigate to target.

        Args:
            speed: Seconds to sleep (refresh) between pages.
        """
        GRAM = "https://www.instagram.com/accounts/login/?source=auth_switcher"
        TARGET = f"https://www.instagram.com/{self.bae}/"

        # Open browser -> Instagram
        self.DRIVER.get(GRAM)
        sleep(3)

        # Log in
        username = self.DRIVER.find_element_by_name("username")
        password = self.DRIVER.find_element_by_name("password")
        username.send_keys(self.user)
        password.send_keys(self.__password)
        password.submit()
        sleep(3)
        # TODO Handle incorrect user/password

        # Navigate to target page
        print(f"\nLocating {self.bae}...")
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
        """Log out and close the browser.

        Args:
            speed: Seconds to sleep (refresh) between pages (default=3.00).
        """
        print("Logging out...")
        HOME = f"https://www.instagram.com/{self.user}/"
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
        print("Session closed successfully!")

    # Placeholder method. Will be re-named and re-located upon completion.
    def test(self) -> None:
        """Test"""
        # Find the total number of pictures
        POSTS = self.DRIVER.find_element_by_class_name("g47SY ")
        TOTAL = POSTS.get_attribute("textContent")
        print(f"Total posts: {TOTAL}")

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


def config() -> tuple:
    """Prompt for user input and return the configuration.

    To be used in conjunction with BaeFinder(), by providing the necessary
    user information (str) and driver (webdriver()) needed to run the program.

    Returns:
        A tuple containing bae's username, your username, password, and driver.
    """
    # Title display
    message = "Welcome to InstaBae!"
    wrap = '=' * len(message)
    print(f"\n{wrap}\n{message}\n{wrap}")

    # Configuration prompts
    bae = input("\nEnter the username of your bae: ")
    user = input("Enter your username: ")
    password = input("Enter your password: ")
    driver = None
    mode = None  # TODO To be added later.

    while driver is None:
        _ = input("Enter [F] for FireFox or [C] for Chrome: ")
        if _.lower() == "f":
            GECKO = "../drivers/geckodriver.exe"
            driver = webdriver.Firefox(executable_path=GECKO)
            break
        elif _.lower() == "c":
            CHROME = "../drivers/chromedriver.exe"
            driver = webdriver.Chrome(exectable_path=CHROME)
            break
        else:
            print("\nNot a compatible browser.\n")
    return (bae, user, password, driver)


def main() -> None:
    """Summon BaeFinder."""
    session = BaeFinder(config())
    print(session)
    session.log_in()
    session.test()


if __name__ == "__main__":
    main()
