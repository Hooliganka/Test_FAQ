import pytest
import allure
from utils import BaseChat


@allure.feature("Отображение чата")
class TestChat(BaseChat):

    @allure.title("Тестирование чата")
    @allure.description("Открытие/закрытие чата")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.asyncio
    async def test_chat_button_visibility(self):
        try:
            await self.home_page.navigate_to_home_page()

            await self.home_page.wait_chat_button_visible()

            # Нажимаем на кнопку
            await self.home_page.click_chat_button()
            with allure.step("Ожидаем появления чата"):
                await self.page.wait_for_selector(self.home_page.CHAT_IFRAME, timeout=3000)

            # Проверяем видимость чата
            assert await self.home_page.is_chat_visible()

            # Закрываем чат
            await self.home_page.click_chat_close()

            with allure.step("Проверяем что чат закрыт"):
                count = await self.page.locator(self.home_page.CHAT_IFRAME).count()
                assert count == 0


        except Exception as e:
            await self.home_page.take_screenshot(f"Exception.png")
            allure.attach(str(e), name="Exception", attachment_type=allure.attachment_type.TEXT)
            raise e