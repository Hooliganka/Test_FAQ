import pytest

from conftest import Browser
from pages.home_page import HomePage


class BaseChat:
    @pytest.fixture(autouse=True)
    async def setup_teardown(self):
        self.browser = Browser()
        self.page = await self.browser.start()
        self.home_page = HomePage(self.page)
        yield
        await self.browser.close()