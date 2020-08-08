import requests



activities_url = "https://www.strava.com/api/v3/athlete/activities"

header = {"Authorization": "Bearer ENTER ACCESS TOKEN"}
my_dataset = requests.get(activities_url, headers = header).json()

print(my_dataset)

433971a49862b25cbcf89b71f241ae2e7ccf34d0

from selenium import webdriver

driver.get("https://www.featuresneakerboutique.com")
driver = webdriver.Chrome(executable_path=r'C:\Users\mahre\Desktop\chromeDriver\chromedriver.exe')