import time
from playwright.sync_api import sync_playwright, Page, expect

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    page = browser.new_page()

    try:
        # Navigate to the app
        page.goto("http://localhost:3347")

        # Click demo torrent to load player
        demo_button = page.get_by_role("button", name="Try Demo with Sintel (CC Movie)")
        expect(demo_button).to_be_visible()
        demo_button.click()
        print("Demo button clicked.")

        # Wait for player to be ready and take screenshot
        player_element = page.locator("#video-player")
        expect(player_element).to_be_visible(timeout=30000) # Wait up to 30s for player
        print("Player is visible.")

        time.sleep(2) # Wait for player to be fully rendered

        page.screenshot(path="jules-scratch/verification/original_flow.png")
        print("Screenshot of original flow player saved.")

    except Exception as e:
        print(f"An error occurred: {e}")
        page.screenshot(path="jules-scratch/verification/error.png")
    finally:
        browser.close()

with sync_playwright() as playwright:
    run(playwright)
