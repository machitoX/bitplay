import time
from playwright.sync_api import sync_playwright, Page, expect

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    page = browser.new_page()

    try:
        # Navigate to the app
        page.goto("http://localhost:3347")

        # Open settings
        settings_button = page.get_by_role("button", name="Settings")
        expect(settings_button).to_be_visible()
        settings_button.click()

        # Go to Real-Debrid tab
        rd_tab = page.get_by_role("button", name="Real-Debrid")
        expect(rd_tab).to_be_visible()
        rd_tab.click()

        # Verify Real-Debrid form is visible
        rd_form = page.locator("#realdebrid-settings-form")
        expect(rd_form).to_be_visible()

        # Take a screenshot of the settings modal
        page.screenshot(path="jules-scratch/verification/realdebrid_settings.png")
        print("Screenshot of Real-Debrid settings saved.")

        # Close settings
        close_button = page.locator("#settings-model #close-settings").first
        close_button.click()
        expect(rd_form).not_to_be_visible()

        # Click demo torrent to load player
        demo_button = page.get_by_role("button", name="Try Demo with Sintel (CC Movie)")
        expect(demo_button).to_be_visible()
        demo_button.click()

        # Wait for player to be ready and take screenshot
        player_element = page.locator("#video-player")
        expect(player_element).to_be_visible(timeout=30000) # Wait up to 30s for player

        # Wait for the custom subtitle button to be loaded in the control bar
        subtitle_upload_button = player_element.locator(".vjs-icon-subtitles")
        expect(subtitle_upload_button).to_be_visible()

        time.sleep(2) # Wait for player to be fully rendered

        page.screenshot(path="jules-scratch/verification/player_with_subtitle_button.png")
        print("Screenshot of player with subtitle button saved.")

    except Exception as e:
        print(f"An error occurred: {e}")
        page.screenshot(path="jules-scratch/verification/error.png")
    finally:
        browser.close()

with sync_playwright() as playwright:
    run(playwright)
