import random


class at_least_n_elements_found(object):
    def __init__(self, locator, n):
        self.locator = locator
        self.n = n

    def __call__(self, driver):
        elements = driver.find_elements(*self.locator)
        if len(elements) >= self.n:
            return elements
        else:
            width = random.randint(200, 800)
            height = random.randint(400, 1200)
            driver.set_window_size(width, height)
            return False
