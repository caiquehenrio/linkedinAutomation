#imported libraries

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from openpyxl import Workbook
from time import sleep

#get credentials

def read_credentials(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()

        credentials = {}
        for line in lines:
            key, value = line.strip().split(":")
            credentials[key] = value
        return credentials
    
file_path_credentials = "credentials.txt"
credentials = read_credentials(file_path_credentials)

#job openings information

print("Let's start looking for your job openings")
search = input("Enter your search: ")
location = input("Enter your location:")

#additional options

def select_announcement_date():
    while True:
        print("Select announcement date (or press Enter to skip):")
        print("1 - A qualquer momento")
        print("2 - Último mês")
        print("3 - Última semana")
        print("4 - Últimas 24 horas")

        option = input("Enter the number corresponding to your choice: ")

        if option == '':
            return None
        elif option == '1':
            return "A qualquer momento"
        elif option == '2':
            return "Último mês"
        elif option == '3':
            return "Última semana"
        elif option == '4':
            return "Últimas 24 horas"
        else:
            print("Invalid option. Please try again.\n")

selected_announcement_date = select_announcement_date()

if selected_announcement_date:
    print(f"You selected: {selected_announcement_date}")
else:
    print("No announcement date filter was selected.")

#enter the login screen

browser = webdriver.Chrome()
browser.maximize_window()
browser.get("https://www.linkedin.com/login")
sleep(3)
email = WebDriverWait(browser, 10).until(
    EC.presence_of_element_located((By.ID, "username"))
)
password = WebDriverWait(browser, 10).until(
    EC.presence_of_element_located((By.ID, "password"))
)
btn_enter = browser.find_element(By.XPATH, "//button[normalize-space(text())='Entrar']")
sleep(3)
email.send_keys(credentials['user'])
sleep(3)
password.send_keys(credentials['password'])
sleep(3)
btn_enter.click()
sleep(5)

#search for job openings

browser.get("https://www.linkedin.com/jobs/")
sleep(3)
input_jobs_search = browser.find_element(By.XPATH, "//input[contains(@class, 'jobs-search-box__text-input')]")
sleep(3)
input_jobs_search.send_keys(search)
sleep(3)
if location:
    input_jobs_search = browser.find_element(By.XPATH, "//input[contains(@id, 'jobs-search-box-location-id')]")
    sleep(3)
    input_jobs_search.clear()
    sleep(3)
    input_jobs_search.send_keys(location)
    sleep(3)
input_jobs_search.send_keys(Keys.ENTER)
sleep(3)

#apply additional options

if selected_announcement_date:
    btn_menu = browser.find_element(By.XPATH, "//button[contains(@aria-label, 'Filtro Data do anúncio. Clicar neste botão exibe todas as opções de filtro de Data do anúncio.')]")
    btn_menu.click() 
    sleep(2) 
    
    if selected_announcement_date == "A qualquer momento":
        option = browser.find_element(By.XPATH, "//label[@for='timePostedRange-']")
    elif selected_announcement_date == "Último mês":
        option = browser.find_element(By.XPATH, "//label[@for='timePostedRange-r2592000']")
    elif selected_announcement_date == "Última semana":
        option = browser.find_element(By.XPATH, "//label[@for='timePostedRange-r604800']")
    elif selected_announcement_date == "Últimas 24 horas":
        option = browser.find_element(By.XPATH, "//label[@for='timePostedRange-r86400']")
    
    option.click()  
sleep(3)
btn_enter = browser.find_element(By.XPATH, "//button[contains(@class, 'artdeco-button artdeco-button--2 artdeco-button--primary ember-view ml2')]")
sleep(3)
btn_enter.click()
sleep(3)
ul_element = browser.find_element(By.CSS_SELECTOR, "main div.jobs-search-results-list")
sleep(3)

#get job openings

def scroll_list(pixels):
    browser.execute_script(f"arguments[0].scrollTop += {pixels};", ul_element)
    sleep(2)


links = []
for _ in range(25):
    scroll_list(200)
    links = browser.find_elements(By.XPATH, "//main//div/div//ul//li//a[@data-control-id]")
    print(len(links))
    if len(links) >= 25:
        print(f'we reached the expected number of {len(links)}')
        break

#save in excel

spreadsheet = Workbook()

sheet = spreadsheet.active

sheet['A1'] = "JOB NAME"
sheet['B1'] = "JOB LINK"
next_line = sheet.max_row + 1

for link in links:
    text = link.text
    url_link = link.get_attribute("href")

    sheet[f'A{next_line}'] = text
    sheet[f'B{next_line}'] = url_link

    next_line += 1

spreadsheet.save("jobs-links-"+search+".xlsx")
print("Spreadsheet created successfully")

#finalize application

print("Ending search")
sleep(5)
browser.quit()
