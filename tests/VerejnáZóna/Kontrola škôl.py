import pytest
from playwright.sync_api import Page, expect
from pages.verejna_zona_page import VerejnaZona

import pytest
from playwright.sync_api import Page
from pages.verejna_zona_page import VerejnaZona


@pytest.mark.regres1kolo
@pytest.mark.regres2kolo
def test_kontrola_SS(page: Page, visual_snapshot) -> None:
    page.set_viewport_size({"width": 1920, "height": 1080})

    zona = VerejnaZona(page)
    zona.vyhladaj_skolu("Stredná škola pre AT", "910021624", "Stredné školy")
    zona.rozklikni_SS()

    visual_snapshot(
        "najst-skolu-ss.png",
        threshold=0.05,
        full_page=True,
        max_diff_pixels=10000
    )

@pytest.mark.regres1kolo
@pytest.mark.regres2kolo
def test_kontrola_ZS(page: Page, visual_snapshot) -> None:
    page.set_viewport_size({"width": 1920, "height": 1080})

    zona = VerejnaZona(page)
    zona.vyhladaj_skolu("Základná škola pre AT", "910021625", "Základné školy")
    page.wait_for_timeout(5000)

    visual_snapshot(
        "najst-skolu-zs.png",
        threshold=0.05,
        full_page=True,
        max_diff_pixels=10000
    )

@pytest.mark.regres1kolo
@pytest.mark.regres2kolo
def test_kontrola_MS(page: Page, visual_snapshot) -> None:
    page.set_viewport_size({"width": 1920, "height": 1080})

    zona = VerejnaZona(page)
    zona.vyhladaj_skolu("Materská škola pre AT", "910021626", "Materské školy")
    page.wait_for_timeout(5000)

    visual_snapshot(
        "najst-skolu-ms.png",
        threshold=0.05,
        full_page=True,
        max_diff_pixels=10000
    )

