import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


def test_api_login_success():
    """Проверка успешной авторизации"""
    response = requests.post(
        "https://reqres.in/api/login",
        json={"email": "eve.holt@reqres.in", "password": "cityslicka"}
    )
    assert response.status_code == 200
    assert "token" in response.json()


def test_api_user_not_found():
    """Проверка ошибки при неверных данных"""
    response = requests.post(
        "https://reqres.in/api/login",
        json={"email": "wrong@example.com", "password": "123"}
    )
    assert response.status_code == 400
    assert response.json().get("error") == "user not found"


def setup_driver():
    options = Options()
    options.add_argument("--headless")
    return webdriver.Chrome(options=options)


def test_ui_search():
    """Проверка поиска на сайте"""
    driver = setup_driver()
    driver.get("https://www.wikipedia.org/")

    search = driver.find_element(By.ID, "searchInput")
    search.send_keys("Python")
    search.submit()

    heading = driver.find_element(By.ID, "firstHeading")
    assert "Python" in heading.text

    driver.quit()


def test_ui_language_switch():
    """Проверка переключения языка"""
    driver = setup_driver()
    driver.get("https://www.wikipedia.org/")

    russian = driver.find_element(By.CSS_SELECTOR, "#js-link-box-ru")
    russian.click()

    assert "ru.wikipedia.org" in driver.current_url

    driver.quit()


def test_api_request_from_ui():
    """
    Проверка, что API отвечает корректно.
    Эмулируем DevTools: делаем запрос напрямую.
    """
    response = requests.get("https://reqres.in/api/users?page=2")
    assert response.status_code == 200
    assert len(response.json().get("data", [])) > 0



def test_ui_form_validation():
    """Проверка валидации формы"""
    driver = setup_driver()
    driver.get("https://www.selenium.dev/selenium/web/web-form.html")

    submit = driver.find_element(By.CSS_SELECTOR, "button")
    submit.click()

    text = driver.find_element(By.ID, "my-text-id")
    assert text.get_attribute("value") == ""

    driver.quit()



def test_redirect_after_action():
    """Проверка редиректа после действия"""
    response = requests.get("https://httpbin.org/redirect/1", allow_redirects=True)
    assert response.url == "https://httpbin.org/get"
    assert response.status_code == 200
