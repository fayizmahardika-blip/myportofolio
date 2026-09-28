import os
import sys

import django
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


load_dotenv()

USER_PASSWORD = os.getenv("E2E_USER_PASSWORD")
ADMIN_PASSWORD = os.getenv("E2E_ADMIN_PASSWORD")

if not USER_PASSWORD or not ADMIN_PASSWORD:
    sys.exit(
        "E2E_USER_PASSWORD dan E2E_ADMIN_PASSWORD "
        "belum diisi di file .env."
    )


os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "portofolio.settings",
)

django.setup()


from django.contrib.auth.models import User
from django.urls import reverse


def setup_users():
    user, _ = User.objects.get_or_create(
        username="fayiz_test_user"
    )
    user.set_password(USER_PASSWORD)
    user.is_superuser = False
    user.is_staff = False
    user.save()

    admin, _ = User.objects.get_or_create(
        username="fayiz_test_admin"
    )
    admin.set_password(ADMIN_PASSWORD)
    admin.is_superuser = True
    admin.is_staff = True
    admin.save()


def main():
    setup_users()

    options = webdriver.ChromeOptions()

    if "--headless" in sys.argv:
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")
    else:
        options.add_argument("--start-maximized")

    options.add_experimental_option(
        "excludeSwitches",
        ["enable-logging"],
    )

    driver = webdriver.Chrome(options=options)

    wait = WebDriverWait(driver, 10)

    base_url = "http://127.0.0.1:8000"

    login_url = base_url + reverse("main:login")
    logout_url = base_url + reverse("main:logout")
    main_url = base_url + reverse("main:show_main")
    create_experience_url = (
        base_url
        + reverse("main:create_experience")
    )

    try:
        # 1. Cek CSRF di form login
        try:
            driver.get(login_url)

        except Exception:
            print(
                "Server belum berjalan. "
                "Jalankan python manage.py runserver."
            )
            return

        csrf = wait.until(
            EC.presence_of_element_located(
                (
                    By.NAME,
                    "csrfmiddlewaretoken",
                )
            )
        )

        assert csrf.get_attribute("value")
        assert driver.get_cookie("csrftoken")

        print(
            "[PASS] CSRF token dan cookie "
            "terverifikasi"
        )

        # 2. Login user biasa
        driver.find_element(
            By.NAME,
            "username",
        ).send_keys(
            "fayiz_test_user"
        )

        driver.find_element(
            By.NAME,
            "password",
        ).send_keys(
            USER_PASSWORD
        )

        driver.find_element(
            By.XPATH,
            "//button[@type='submit']",
        ).click()

        wait.until(
            EC.url_to_be(main_url)
        )

        wait.until(
            EC.visibility_of_element_located(
                (
                    By.CLASS_NAME,
                    "nav-user",
                )
            )
        )

        assert driver.get_cookie("sessionid")
        assert driver.get_cookie("last_login")

        assert (
            "Sesi Terakhir Login"
            in driver.page_source
        )

        print(
            "[PASS] Login user biasa "
            "dan cookie sesi berhasil"
        )

        # 3. User biasa tidak boleh Create Experience
        driver.get(create_experience_url)

        assert (
            "403" in driver.title
            or "Forbidden" in driver.page_source
        )

        print(
            "[PASS] User biasa dibatasi "
            "dari Create Experience (403)"
        )

        # 4. Logout user biasa
        driver.get(logout_url)

        wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//a[contains(@href, '/login/')]",
                )
            )
        )

        # 5. Login sebagai superuser
        driver.get(login_url)

        wait.until(
            EC.presence_of_element_located(
                (
                    By.NAME,
                    "username",
                )
            )
        ).send_keys(
            "fayiz_test_admin"
        )

        driver.find_element(
            By.NAME,
            "password",
        ).send_keys(
            ADMIN_PASSWORD
        )

        driver.find_element(
            By.XPATH,
            "//button[@type='submit']",
        ).click()

        wait.until(
            EC.url_to_be(main_url)
        )

        wait.until(
            EC.text_to_be_present_in_element(
                (
                    By.CLASS_NAME,
                    "nav-user",
                ),
                "fayiz_test_admin",
            )
        )

        # 6. Superuser boleh membuka form
        driver.get(create_experience_url)

        wait.until(
            EC.presence_of_element_located(
                (
                    By.CLASS_NAME,
                    "education-form",
                )
            )
        )

        print(
            "[PASS] Superuser dapat membuka "
            "form Create Experience"
        )

        # 7. Logout + cek cookie hilang
        driver.get(logout_url)

        wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//a[contains(@href, '/login/')]",
                )
            )
        )

        cookie_last_login = driver.get_cookie(
            "last_login"
        )

        assert (
            cookie_last_login is None
            or cookie_last_login["value"] == ""
        )

        print(
            "[PASS] Logout dan penghapusan "
            "cookie berhasil"
        )

        print(
            "\nSemua pengujian E2E berhasil!"
        )

    finally:
        driver.quit()


if __name__ == "__main__":
    main()