from playwright.sync_api import sync_playwright

from gameweek.gameweek import (
    get_current_round,
    get_current_season
)


def download_grades():

    round_number = get_current_round()
    season = get_current_season()

    url = (
        "https://www.fantacalcio.it/"
        f"voti-fantacalcio-serie-a/{season}/{round_number}"
    )

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-dev-shm-usage"
            ]
        )

        page = browser.new_page()

        page.goto(url)

        page.goto(url, wait_until="networkidle")

        page.wait_for_timeout(1000)

        html = page.content()

        with open(
            "page_playwright.html",
            "w",
            encoding="utf-8"
        ) as f:

            f.write(html)

        browser.close()