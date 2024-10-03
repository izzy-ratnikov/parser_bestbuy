import json
from playwright.sync_api import sync_playwright
from bestbuy_parser.utils.config import PROXY, URL
from bestbuy_parser.locators.locators import Locators


class BestBuyFullPageParser:

    def __get_phone_info(self, page):
        try:
            page.wait_for_selector('body', timeout=5000)

            seller_element = page.query_selector(Locators.MODEL)
            seller_name = seller_element.inner_text() if seller_element else "Элемент с названием модели не найден."

            screen_size_element = page.query_selector(Locators.SCREEN_SIZE)
            screen_size = screen_size_element.inner_text() if screen_size_element else "Не найдено"

            front_camera_element = page.query_selector(Locators.FRONT_CAMERA)
            front_camera = front_camera_element.inner_text() if front_camera_element else "Не найдено"

            rear_camera_element = page.query_selector(Locators.REAR_CAMERA)
            rear_camera = rear_camera_element.inner_text() if rear_camera_element else "Не найдено"

            ultrawide_camera_element = page.query_selector(Locators.ULTRAWIDE_CAMERA)
            ultrawide_camera = ultrawide_camera_element.inner_text() if ultrawide_camera_element else "Не найдено"

            series_element = page.query_selector(Locators.SERIES)
            series = series_element.inner_text() if series_element else "Не найдено"

            result = {
                "Модель": seller_name,
                "Screen Size": screen_size,
                "Front-Facing Camera": front_camera,
                "Rear-Facing Camera": rear_camera,
                "Ultrawide Camera": ultrawide_camera,
                "Series": series
            }

            print(json.dumps(result, ensure_ascii=False, indent=4))

        except Exception as e:
            print(f"Ошибка при получении данных: {e}")

    def __get_full_page_info(self, page):
        try:
            page.wait_for_selector('body', timeout=5000)

            headers = [h.inner_text() for h in page.query_selector_all('h1, h2, h3, h4, h5, h6')]
            paragraphs = [p.inner_text() for p in page.query_selector_all('p, div')]
            links = [a.get_attribute('href') for a in page.query_selector_all('a')]
            images = [img.get_attribute('src') for img in page.query_selector_all('img')]

            headers = list(set(headers))
            paragraphs = list(set(paragraphs))
            links = list(set(links))
            images = list(set(images))

            page_data = {
                "headers": headers,
                "paragraphs": paragraphs,
                "links": links,
                "images": images
            }

            print(json.dumps(page_data, ensure_ascii=False, indent=4))

        except Exception as e:
            print(f"Ошибка при получении данных со страницы: {e}")

    def parse(self):
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=False)
            self.context = browser.new_context(proxy=PROXY, record_har_path="network_log.har")
            self.page = self.context.new_page()
            try:
                self.page.goto(URL, timeout=300000)
            except TimeoutError:
                print("Не удалось загрузить страницу в течение отведенного времени.")

            self.__get_full_page_info(self.page)

            self.__get_phone_info(self.page)
