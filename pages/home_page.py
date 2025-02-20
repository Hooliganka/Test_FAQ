import allure
from pathlib import Path
from playwright.async_api import Page


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    async def navigate(self, url: str):
        with allure.step(f"Навигация к {url}"):
            await self.page.goto(url)


class HomePage(BasePage):
    SCREENSHOT_DIR = Path("screenshots")

    URL = "https://autofaq.ai/"

    # Селекторы
    CHAT_BUTTON = "#chat21-launcher-button"
    CHAT_IFRAME = ".chat21-window.chat21-sheet"
    CHAT_IFRAME_CLOSE = ".chat21-sheet-header-close-button"
    CHAT_REGISTER_FORM_IFRAME = ".form_panel"
    NAME_INPUT = "input[name='senderFullName']"
    EMAIL_INPUT = "input[name='senderEmail']"
    SUBMIT_BUTTON = ".form_panel_action.form_panel_action-submit"
    SUCCESS_MESSAGE = ".chat21-header-modal-select"
    FORM_ERROR_MESSAGE = ".form_panel>.form_panel_field--error>.form_panel_field-hint"
    FORM_CLOSE = ".form_panel>.form_panel_close"
    CHAT_INPUT = "textarea.f21textarea"
    CHAT_INPUT_BUTTON = "#chat21-button-send"
    CHAT_MY_MESSAGE = "#chat21-contentScroll .messages .msg_content"

    # Проверочные данные
    TEXT_MESSAGE = "Напишите свой вопрос и я постараюсь вам помочь"

    async def navigate_to_home_page(self):
        with allure.step("Открытие главной страницы"):
            await self.navigate(self.URL)

    async def wait_chat_button_visible(self):
        with allure.step("Проверка видимости кнопки чата"):
            await self.page.wait_for_selector(self.CHAT_BUTTON, timeout=3000)

    async def is_chat_visible(self) -> bool:
        with allure.step("Проверка видимости чата"):
            chat = await self.page.is_visible(self.CHAT_IFRAME)
            return chat

    async def wait_chat_register_form_visible(self):
        with allure.step("Проверка видимости формы чата"):
            await self.page.wait_for_selector(self.CHAT_REGISTER_FORM_IFRAME, timeout=3000)

    async def click_chat_button(self):
        with allure.step("Клик по кнопке чата"):
            await self.page.click(self.CHAT_BUTTON)

    async def click_send_message(self):
        with allure.step("Отправка сообщения в чат"):
            await self.page.click(self.CHAT_INPUT_BUTTON)

    async def click_chat_close(self):
        with allure.step("Закрываем чат на крестик слева сверху"):
            await self.page.click(self.CHAT_IFRAME_CLOSE)

    async def click_form_close(self):
        with allure.step("Закрываем форму на крестик"):
            await self.page.click(self.FORM_CLOSE)

    async def take_screenshot(self, path: str):
        self.SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
        full_path = self.SCREENSHOT_DIR / path

        with allure.step(f"Создание скриншота: {path}"):
            await self.page.screenshot(path=str(full_path))
            allure.attach.file(str(full_path), name="Screenshot", attachment_type=allure.attachment_type.PNG)

    async def fill_contact_form(self, name: str, email: str):
        with allure.step(f"Заполнение формы данными: {name}, {email}"):
            await self.page.fill(self.NAME_INPUT, name)
            await self.page.fill(self.EMAIL_INPUT, email)

    async def submit_form(self):
        with allure.step("Отправка формы"):
            await self.page.click(self.SUBMIT_BUTTON)
