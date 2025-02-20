import pytest
import allure
from utils import BaseChat

TEST_DATA = [
    pytest.param(
        {"name": "Test User", "email": "", "test_id": 2, "error_message": "Требуется указать почту."},
        id="invalid_data_2"
    ),
    pytest.param(
        {"name": "Test User", "email": "test", "test_id": 3, "error_message": "Почта имеет неверный формат."},
        id="invalid_data_3"
    ),
    pytest.param(
        {"name": "", "email": "test@example.com", "test_id": 1, "error_message": "???"},
        id="invalid_data_1"
    ),
]


@allure.feature("Тестирование формы регистрации")
class TestChatRegistrationForm(BaseChat):

    @allure.title("Тестирование формы")
    @allure.description("Заполнение формы регистрации с валидными данными")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.asyncio
    async def test_chat_registration_form(self):
        test_data = {"name": "Test User", "email": "test@example.com"}

        try:
            await self.home_page.navigate_to_home_page()

            await self.home_page.wait_chat_button_visible()

            # Нажимаем на кнопку
            await self.home_page.click_chat_button()
            with allure.step("Ожидаем появления чата"):
                await self.page.wait_for_selector(self.home_page.CHAT_IFRAME, timeout=3000)

            # Проверяем видимость чата
            assert await self.home_page.is_chat_visible()

            await self.home_page.take_screenshot("is_visible_chat.png")

            # Проверяем видимость формы чата
            await self.home_page.wait_chat_register_form_visible()

            await self.home_page.fill_contact_form(
                name=test_data.get('name'),
                email=test_data.get('email'),
            )

            await self.home_page.take_screenshot("fill_contact_form.png")

            # Отправляем форму
            await self.home_page.submit_form()

            with allure.step("Ожидаем появления сообщения в чате"):
                message_object = await self.page.wait_for_selector(self.home_page.SUCCESS_MESSAGE, timeout=3000)

                assert await message_object.text_content() == self.home_page.TEXT_MESSAGE

                await self.home_page.take_screenshot("form_submitted.png")

            # Закрываем чат
            await self.home_page.click_chat_close()

            with allure.step("Проверяем что чат закрыт"):
                count = await self.page.locator(self.home_page.CHAT_IFRAME).count()
                assert count == 0


        except Exception as e:
            await self.home_page.take_screenshot(f"Exception.png")
            allure.attach(str(e), name="Exception", attachment_type=allure.attachment_type.TEXT)
            raise e

    @allure.title("Тестирование формы")
    @allure.description("Заполнение формы регистрации с не валидными данными")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.asyncio
    @pytest.mark.parametrize("test_data", TEST_DATA)
    async def test_negative_chat_registration_form(self, test_data: dict):
        try:
            await self.home_page.navigate_to_home_page()

            await self.home_page.wait_chat_button_visible()

            # Нажимаем на кнопку
            await self.home_page.click_chat_button()
            with allure.step("Ожидаем появления чата"):
                await self.page.wait_for_selector(self.home_page.CHAT_IFRAME, timeout=3000)

            # Проверяем видимость чата
            assert await self.home_page.is_chat_visible()

            # Проверяем видимость формы чата
            await self.home_page.wait_chat_register_form_visible()

            await self.home_page.fill_contact_form(
                name=test_data.get('name'),
                email=test_data.get('email'),
            )

            # Отправляем форму
            await self.home_page.submit_form()

            with allure.step("Проверяем что форма не закрылась"):
                await self.home_page.wait_chat_register_form_visible()

                message_object = await self.page.wait_for_selector(self.home_page.FORM_ERROR_MESSAGE, timeout=1000)

                assert await message_object.text_content() == test_data.get('error_message')

                await self.home_page.take_screenshot(f"error_message_form_{test_data.get('test_id')}.png")


        except Exception as e:
            await self.home_page.take_screenshot(f"Exception_{test_data.get('test_id')}.png")
            allure.attach(str(e), name="Exception", attachment_type=allure.attachment_type.TEXT)
            raise e


    @allure.title("Тестирование формы")
    @allure.description("Проверка закрытия формы регистрации")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.asyncio
    async def test_close_chat_registration_form(self):
        try:
            await self.home_page.navigate_to_home_page()

            await self.home_page.wait_chat_button_visible()

            # Нажимаем на кнопку
            await self.home_page.click_chat_button()
            with allure.step("Ожидаем появления чата"):
                await self.page.wait_for_selector(self.home_page.CHAT_IFRAME, timeout=3000)

            # Проверяем видимость чата
            assert await self.home_page.is_chat_visible()

            # Проверяем видимость формы чата
            await self.home_page.wait_chat_register_form_visible()

            # Закрываем чат
            await self.home_page.click_form_close()

            with allure.step("Ожидаем появления сообщения в чате"):
                message_object = await self.page.wait_for_selector(self.home_page.SUCCESS_MESSAGE, timeout=3000)

                assert await message_object.text_content() == self.home_page.TEXT_MESSAGE

        except Exception as e:
            await self.home_page.take_screenshot(f"Exception.png")
            allure.attach(str(e), name="Exception", attachment_type=allure.attachment_type.TEXT)
            raise e
