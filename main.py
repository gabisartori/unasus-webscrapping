from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

with open('config.txt') as f:
    url = f.readline().strip().split()[-1]
    login = f.readline().strip().split()[-1]
    password = f.readline().strip().split()[-1]
    numero_grupos = int(f.readline().strip().split()[-1].strip())
    try:
        download_path = f.readline().strip().split()[-1]
    except IndexError:
        download_path = '.'

options = webdriver.FirefoxOptions()
options.set_preference("browser.download.folderList", 2)
options.set_preference("browser.download.manager.showWhenStarting", False)
options.set_preference("browser.download.dir", download_path)
options.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/csv")

def visit_and_login(driver: webdriver.Firefox, url: str, login: str, password: str):
    driver.get(url)
    username_field = driver.find_element(By.ID, 'username')
    password_field = driver.find_element(By.ID, 'password')
    submit_button = driver.find_element(By.NAME, 'submit')
    username_field.send_keys(login)
    password_field.send_keys(password)
    submit_button.click()

def open_history(driver: webdriver.Firefox):
    WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))
    driver.switch_to.window(driver.window_handles[1])
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "Ver histórico")]')))
    driver.find_element(By.XPATH, '//*[contains(text(), "Ver histórico")]').click()

def select_group(driver: webdriver.Firefox, group: str):
    select_element = driver.find_element(By.ID, 'group_id')
    driver.execute_script("arguments[0].scrollIntoView();", select_element)
    select = Select(select_element)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(select_element))
    time.sleep(1)
    select.select_by_visible_text(group)

def get_meetings_actions():
    for element in driver.find_elements(By.CLASS_NAME, 'icon-options-dots'):
        if element.is_displayed():
            yield element

def open_meeting_report(driver: webdriver.Firefox, meeting_dots):
    driver.execute_script("arguments[0].scrollIntoView();", meeting_dots)
    meeting_dots.click()

    time.sleep(0.25)

    # This is a workaround because the xpath '//*[contains(text(), "Relatório de engajamento")]'
    # doesn't work
    # ¯\_(ツ)_/¯
    all_buttons = driver.find_elements(By.XPATH, '//button')
    report_link = [x for x in all_buttons if x.text == "Relatório de engajamento"][0]
    report_link.click()

if __name__ == '__main__':
    driver = webdriver.Firefox(options=options)
    visit_and_login(driver, url, login, password)
    open_history(driver)

    # Go through each group
    for i in range(1, numero_grupos+1):
        select_group(driver, f"Grupo {i:0>3}")
        # Go through each meeting of the group
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'icon-options-dots')))
        for meeting_dots in get_meetings_actions():
            open_meeting_report(driver, meeting_dots)
            
            WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(3))
            driver.switch_to.window(driver.window_handles[2])
            
            # Replace this sleep with the wait for another component
            # Because the download button renders before the page is fully loaded
            time.sleep(1)
            download_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[text()='Download Session Data']")))
            download_button.click()

            driver.close()
            driver.switch_to.window(driver.window_handles[1])
            time.sleep(1)