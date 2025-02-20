import pytest
import allure
from utils import BaseChat


@allure.feature("Тестирование отправки сообщения в чат")
class TestSendMessage(BaseChat):

    @allure.title("Тестирование чата")
    @allure.description("Отправка простого текстового сообщения")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.asyncio
    async def test_send_simple_message(self):
        test_data = {"name": "Test User", "email": "test@example.com"}

        try:
            await self.home_page.navigate_to_home_page()

            await self.home_page.wait_chat_button_visible()

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

            with allure.step("Ожидаем появления сообщения в чате"):
                message_object = await self.page.wait_for_selector(self.home_page.SUCCESS_MESSAGE, timeout=3000)

                assert await message_object.text_content() == self.home_page.TEXT_MESSAGE

            m = "Привет мир"
            with allure.step("Отправляем сообщение в чат"):
                await self.page.fill(self.home_page.CHAT_INPUT, m)

                await self.home_page.click_send_message()

            with allure.step("Ожидаем появления нашего сообщения в чате"):
                message = await self.page.wait_for_selector(self.home_page.CHAT_MY_MESSAGE, timeout=3000)
                assert await message.text_content() == m

        except Exception as e:
            await self.home_page.take_screenshot(f"Exception.png")
            allure.attach(str(e), name="Exception", attachment_type=allure.attachment_type.TEXT)
            raise e
