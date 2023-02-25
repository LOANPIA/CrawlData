from selenium import webdriver # chỉ sử dụng webdriver -- selenium 4.8
from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options
import datetime # lâý time để lưu file
import os, time # time.sleep() và os để nối đường dẫn

# <iframe scrolling="no" frameborder="0" width="100%" height="100" style="height: 1039px;"></iframe> iframe 2: index 1
# class city
# class total
# class daynow
# class die
# xpath = /html/body/div[1]/div[2]/div[3]/div/iframe
if __name__ == "__main__":

    data_save_file_csv = [] #variable set for data save into file

    url_file_driver = os.path.join('etc', 'chromedriver.exe')
    driver = webdriver.Chrome(executable_path = url_file_driver)
    driver.get("https://covid19.gov.vn/")

    driver.switch_to.frame(1) #1 là index of iframe defined before
    target = driver.find_elements(By.XPATH, '/html/body/div[2]/div[1]/div') #--table-left (find_elements : return list, find_element : return string)
    for data in target:
        cities = data.find_elements(By.CLASS_NAME, 'city')
        totals = data.find_elements(By.CLASS_NAME, 'total')
        today = data.find_elements(By.CLASS_NAME, 'daynow')
        deaths = data.find_elements(By.CLASS_NAME, 'die')

    # for i in cities:
    #     print(i.text)
    list_cities = [city.text for city in cities]
    list_totals = [total.text for total in totals]
    list_today = [daynow.text for daynow in today]
    list_deaths = [die.text for die in deaths]

    for i in range(len(list_cities)):
        row = "{},{},{},{}\n".format(list_cities[i],list_totals[i],list_today[i],list_deaths[i]) #type format string: "{}".format()
        data_save_file_csv.append(row)

    today_ = (datetime.datetime.now()).strftime('%Y%m%d') #get current timestamp and format YYYYmmdd
    filename = f"{today_}.csv" #type format string: f"{}" embbed string ez
    with open(os.path.join('data', filename),'w+', encoding='utf-8') as f: #overwriting on old file - not continue to write
        f.writelines(data_save_file_csv)

    # time.sleep(3) #stop with 3s after start website page
    driver.close() #notice