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
        print("Settings modal opened.")

        # Verify the modal is visible
        settings_modal = page.locator("#settings-model")
        expect(settings_modal).to_be_visible()

        # Click the Real-Debrid tab
        rd_tab = page.get_by_role("button", name="Real-Debrid")
        expect(rd_tab).to_be_visible()
        rd_tab.click()
        print("Clicked Real-Debrid tab.")

        # Verify Real-Debrid form is visible
        rd_form = page.locator("#realdebrid-settings-form")
        expect(rd_form).to_be_visible()
        print("Real-Debrid form is visible.")

        # Take a screenshot of the settings modal
        page.screenshot(path="jules-scratch/verification/settings_verification.png")
        print("Screenshot of Real-Debrid settings saved.")

    except Exception as e:
        print(f"An error occurred: {e}")
        page.screenshot(path="jules-scratch/verification/error.png")
    finally:
        browser.close()

with sync_playwright() as playwright:
    run(playwright)
