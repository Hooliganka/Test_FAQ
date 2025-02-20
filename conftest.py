import asyncio
import os
import pytest
import allure
from playwright.async_api import async_playwright


class Browser:
    def __init__(self):
        self.browser = None
        self.context = None
        self.page = None
        self.playwright = None

    async def start(self):
        with allure.step("Запуск браузера"):
            self.playwright = await async_playwright().start()
            self.browser = await self.playwright.chromium.launch()

            if not os.path.exists('video'):
                os.makedirs('video')

            self.context = await self.browser.new_context(
                record_video_dir="video",
                record_video_size={"width": 1280, "height": 720}
            )

            self.page = await self.context.new_page()
            return self.page

    async def close(self):
        with allure.step("Закрытие браузера"):
            try:
                if self.page:
                    video = self.page.video
                    await self.page.close()

                    if video:
                        video_path = await video.path()
                        await asyncio.sleep(1)

                        if os.path.exists(video_path):
                            allure.attach.file(
                                video_path,
                                name="test_video",
                                attachment_type=allure.attachment_type.WEBM
                            )

                if self.context:
                    await self.context.close()
                if self.browser:
                    await self.browser.close()
                if self.playwright:
                    await self.playwright.stop()

            except Exception as e:
                print(f"Error during browser closing: {e}")
                allure.attach(
                    str(e),
                    name="Browser closing error",
                    attachment_type=allure.attachment_type.TEXT
                )


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()