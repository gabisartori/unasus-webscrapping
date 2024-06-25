from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime

url = ""
login = ""
senha = ""
grupo_inicio = 1
grupo_fim = 259
data_inicio = ""
data_fim = ""
download_path = ""

with open('config.txt') as f:
    for line in f.readlines():
        if line.strip().startswith("#") or line.strip() == "": continue
        key, *value = line.split(": ")
        value = "".join(value).strip()
        exec(f'{key}="{value}"')

password = senha
group_start = int(grupo_inicio)
group_end = int(grupo_fim)
date_start = datetime.strptime(data_inicio, "%d/%m/%Y") if data_inicio else ""
date_end = datetime.strptime(data_fim, "%d/%m/%Y") if data_fim else ""


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

def get_meetings():
    for element in driver.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr'):
        yield element

def download_meeting_csv(meeting):
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'col-5')))

    date = meeting.find_element(By.CLASS_NAME, 'col-5')
    date = datetime.strptime(date.text.split("\n")[0], "%d/%m/%Y")

    print(date, date_start, date < date_start)
    if date_start and date < date_start:
        print("Reunião antiga, ignorando")
        return
    if date_end and date > date_end: return

    meeting_options = meeting.find_element(By.CLASS_NAME, 'icon-options-dots')
    open_and_download_meeting_report(driver, meeting_options)

def open_and_download_meeting_report(driver: webdriver.Firefox, meeting_dots):
    # Click the dots to show options and then click the report link
    driver.execute_script("arguments[0].scrollIntoView();", meeting_dots)
    meeting_dots.click()

    time.sleep(0.25)

    # This is a workaround because the xpath '//*[contains(text(), "Relatório de engajamento")]'
    # doesn't work
    # ¯\_(ツ)_/¯
    all_buttons = driver.find_elements(By.XPATH, '//button')
    report_link = [x for x in all_buttons if x.text == "Relatório de engajamento"]
    if not report_link:
        print("Relatório não encontrado")
        return
    report_link = report_link[0]
    report_link.click()

    # Wait for report page to load
    WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(3))
    driver.switch_to.window(driver.window_handles[2])

    # Wait for download button to load
    time.sleep(1)
    download_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[text()='Download Session Data']")))
    download_button.click()

    # Close report tab and go back to the history tab
    driver.close()
    driver.switch_to.window(driver.window_handles[1])

if __name__ == '__main__':
    driver = webdriver.Firefox(options=options)
    visit_and_login(driver, url, login, password)
    open_history(driver)

    for i in range(group_start, group_end+1):
        select_group(driver, f"Grupo {i:0>3}")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'icon-options-dots')))
        for meeting in get_meetings():
            download_meeting_csv(meeting)