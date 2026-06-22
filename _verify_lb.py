from playwright.sync_api import sync_playwright
import time, json

results = {}

with sync_playwright() as p:
    browser = p.chromium.launch(channel="msedge", headless=True)
    page = browser.new_page(viewport={"width":1280,"height":900})
    page.goto("http://127.0.0.1:8743/index.html", wait_until="load")

    # --- Test 1: Beth Harmon section has single bozza -> arrows should be hidden ---
    img1 = page.locator('img[src*="01-beth-harmon/bozza-1.jpg"]').first
    img1.scroll_into_view_if_needed()
    img1.click()
    page.wait_for_timeout(300)
    lb_open = page.locator("#lightbox.open").count() > 0
    prev_hidden = page.locator(".lb-prev").get_attribute("hidden")
    next_hidden = page.locator(".lb-next").get_attribute("hidden")
    results["single_image_section"] = {
        "lb_open": lb_open,
        "prev_hidden": prev_hidden is not None,
        "next_hidden": next_hidden is not None,
    }
    page.keyboard.press("Escape")
    page.wait_for_timeout(300)
    results["escape_closes"] = page.locator("#lightbox.open").count() == 0

    # --- Test 2: Fuga di Logan bz-strip with 8 images -> arrows visible, click-through ---
    img2 = page.locator('img[src*="05-fuga-di-logan/bozze/01.jpg"]').first
    img2.scroll_into_view_if_needed()
    img2.click()
    page.wait_for_timeout(300)
    prev_hidden2 = page.locator(".lb-prev").get_attribute("hidden")
    next_hidden2 = page.locator(".lb-next").get_attribute("hidden")
    src_initial = page.locator("#lightbox img").get_attribute("src")
    page.locator(".lb-next").click()
    page.wait_for_timeout(200)
    src_after_click = page.locator("#lightbox img").get_attribute("src")
    page.keyboard.press("ArrowRight")
    page.wait_for_timeout(200)
    src_after_arrowkey = page.locator("#lightbox img").get_attribute("src")
    page.keyboard.press("ArrowLeft")
    page.keyboard.press("ArrowLeft")
    page.wait_for_timeout(200)
    src_after_arrowleft = page.locator("#lightbox img").get_attribute("src")
    results["fuga_di_logan"] = {
        "prev_hidden": prev_hidden2 is not None,
        "next_hidden": next_hidden2 is not None,
        "src_initial": src_initial,
        "src_after_click": src_after_click,
        "src_after_arrowkey": src_after_arrowkey,
        "src_after_arrowleft_x2": src_after_arrowleft,
    }

    # wraparound test: click prev from first image should wrap to last
    # reset to first by clicking prev once more or reload
    page.keyboard.press("Escape")
    page.wait_for_timeout(200)
    img2.click()
    page.wait_for_timeout(200)
    page.locator(".lb-prev").click()
    page.wait_for_timeout(200)
    src_wrap = page.locator("#lightbox img").get_attribute("src")
    results["wraparound_prev_from_first"] = src_wrap
    page.keyboard.press("Escape")
    page.wait_for_timeout(200)

    # --- Test 3: grouped bambina d'ombra -- click image in "Cover" group (3 imgs), verify scope doesn't bleed to "Capurela" group ---
    cover_img = page.locator('img[src*="04-bambina-dombra/1-cover/bozza-1.JPG"]').first
    cover_img.scroll_into_view_if_needed()
    cover_img.click()
    page.wait_for_timeout(300)
    seq = [page.locator("#lightbox img").get_attribute("src")]
    for _ in range(4):
        page.locator(".lb-next").click()
        page.wait_for_timeout(150)
        seq.append(page.locator("#lightbox img").get_attribute("src"))
    results["bambina_cover_group_sequence"] = seq
    page.keyboard.press("Escape")
    page.wait_for_timeout(200)

    browser.close()

print(json.dumps(results, indent=2))
