import json
from playwright.sync_api import sync_playwright


def run(playwright):
    browser = playwright.chromium.launch()
    context = browser.new_context()
    # Откройте новую страницу
    page = context.new_page()
    # Перейдите на страницу входа
    page.goto("http://quotes.toscrape.com/login")
    # Заполните форму входа
    page.fill('input[name="username"]', 'admin')
    page.fill('input[name="password"]', 'admin')
    # Отправьте форму
    page.click('input[type="submit"]')
    # Проверьте, что вход выполнен успешно
    if "Logout" in page.content():
        print("Login successful")
        # Перейдите на главную страницу
        page.goto("http://quotes.toscrape.com/")
        # Создайте список для хранения данных
        data = []
        # Пока есть ссылка на следующую страницу, продолжайте скрапинг
        while True:
            # Получите данные
            quotes = page.query_selector_all('.quote')
            for quote in quotes:
                text = quote.query_selector('.text').inner_text()
                author = quote.query_selector('.author').inner_text()
                tags = [tag.inner_text() for tag in quote.query_selector_all('.tags a.tag')]
                data.append({'text': text, 'author': author, 'tags': tags})
            # Попробуйте найти ссылку на следующую страницу
            next_link = page.query_selector('.next a')
            if next_link:
                # Если ссылка найдена, перейдите на следующую страницу
                next_link.click()
                # Дождитесь загрузки страницы
                page.wait_for_load_state('load')
            else:
                # Если ссылки нет, вы вышли из цикла
                break
        # Запишите собранные данные в файл JSON
        with open('new_quotes.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    else:
        print("Login failed")
    # Закройте страницу
    page.close()
    # Закройте браузер
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
