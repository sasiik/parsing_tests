from webbrowser import Chrome
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def open_webpage(url, driver):
    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.CLASS_NAME, "card-info-block"))
        )

        elements = driver.find_elements(By.CLASS_NAME, "card-info-block")
        result = []

        for element in elements:
            data = element.text.splitlines()
            if len(data) == 5:
                output = {
                    "name": data[0].strip(),
                    "rating": data[1].strip(),
                    "reviews": data[2].strip(),
                    "current_price": data[3].strip(),
                    "old_price": data[4].strip(),
                }
                result.append(output)
        print(result)
        return result
    except Exception as e:
        print("An error occurred:", e)


def main():
    driver = webdriver.Chrome()
    all_data = []
    base_url = 'https://kazanexpress.ru/category/bytovaya-tekhnika-10004'
    for i in range(1, 5):
        url = base_url + f"?currentPage={i}"
        current_page_data = open_webpage(url, driver)
        print(current_page_data, url)
        if current_page_data:
            all_data += current_page_data
    driver.quit()
    df = pd.DataFrame(all_data)
    df.to_excel('kazanexpress/output/output.xlsx',
                engine='openpyxl', index=False)
    print("Data saved to output.xlsx.")


main()
