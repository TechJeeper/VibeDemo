from playwright.sync_api import sync_playwright, expect
import os

def verify_layout():
    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Load the local index.html file
        file_path = os.path.abspath("index.html")
        page.goto(f"file://{file_path}")

        print("Verifying page title...")
        expect(page).to_have_title("Generic Designs Inc.")

        print("Verifying profile picture...")
        expect(page.locator(".profile-pic")).to_be_visible()

        print("Verifying main heading...")
        expect(page.locator("h1")).to_contain_text("Generic Designs Inc.")

        print("Verifying links...")
        links = [
            "Twitch", "X", "Website", "MakerWorld", "TikTok", "Contact Email"
        ]

        for link_text in links:
            print(f"Checking link: {link_text}")
            link = page.locator(f"a.link-card:has-text('{link_text}')")
            expect(link).to_be_visible()
            # Verify hover effect (basic check that CSS is likely applied)
            box = link.bounding_box()
            assert box['width'] > 0
            assert box['height'] > 0

        print("Verifying background canvas...")
        canvas = page.locator("#bg-canvas")
        expect(canvas).to_be_attached()
        canvas_box = canvas.bounding_box()
        assert canvas_box['width'] > 0
        assert canvas_box['height'] > 0

        print("Verifying social feed container...")
        feed_container = page.locator(".social-feed")
        expect(feed_container).to_be_visible()

        print("Verifying Twitter timeline integration...")
        page.wait_for_timeout(2000)

        # Count how many elements match .twitter-timeline (could be anchor or div)
        # We just need at least one to prove the code is there.
        count = page.locator(".twitter-timeline").count()

        if count > 0:
            print(f"Twitter timeline elements found: {count}")
        else:
            # Fallback: check for iframe if the class was removed
            iframe_count = page.locator("iframe[id^='twitter-widget']").count()
            if iframe_count > 0:
                print(f"Twitter widget iframe found: {iframe_count}")
            else:
                raise AssertionError("No Twitter timeline elements found.")

        print(" taking screenshot...")
        page.screenshot(path="verification_screenshot.png", full_page=True)

        browser.close()
        print("Verification successful!")

if __name__ == "__main__":
    verify_layout()
