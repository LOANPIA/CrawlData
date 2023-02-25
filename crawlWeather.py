from selenium import webdriver # chỉ sử dụng webdriver -- selenium 4.8
from selenium.webdriver.common.by import By
import pyodbc
import pandas as pd
# from selenium.webdriver.chrome.options import Options
import datetime # lâý time để lưu file
import os, time # time.sleep() và os để nối đường dẫn

if __name__ == "__main__":

    data_save_file_csv = [] #variable set for data save into file

    url_file_driver = os.path.join('etc', 'etc/chromedriver.exe')
    driver = webdriver.Chrome(executable_path = url_file_driver)
    driver.get("https://nchmf.gov.vn/Kttvsite/vi-VN/1/ha-noi-w28.html")

    # /html/body/form/div[3]/div/div[2]/section/div/div/article/div/div/div[2]/div/div --uk-grid : lưới thời tiết
    target = driver.find_elements(By.XPATH, '/html/body/form/div[3]/div/div[2]/section/div/div/article/div/div/div[2]/div/div') #--section (find_elements : return list, find_element : return string)
    for data in target:
        datewts = data.find_elements(By.CLASS_NAME, 'date-wt')
        descWeaths = data.find_elements(By.CLASS_NAME, 'text-temp')

####################################################################################################
####################################################################################################

    # Get element from browser
    list_datewts = [datewt.text for datewt in datewts]
    list_descWeaths = [texttemp.text for texttemp in descWeaths]

    # Get split \n
    R_list_datewts = [i.split('\n',1)[1] for i in list_datewts]
    R_list_descWeaths = [i.split(', ', 1)[1] for i in list_descWeaths]

    # Get 1 step element in list
    Date = [R_list_datewts[R_list_datewt] for R_list_datewt in range(0, len(R_list_datewts))]
    Weather = [R_list_descWeaths[R_list_descWeath] for R_list_descWeath in range(0, len(R_list_descWeaths))]

# --yield
    data = {
        "dow": Date,
        "status": Weather
    }
    WeatherDF = pd.DataFrame(data)
    # Insert Dataframe into SQL Server:
    for index, row in WeatherDF.iterrows():
        l1 = row['dow']
        l2 = row['status']

        data2 = {
            "dow": l1.split(','),
            "status": l2.split(',')
        }
        WeatherDF2 = pd.DataFrame(data2)
        for index2, row2 in WeatherDF2.iterrows():
            conn = pyodbc.connect('Driver={SQL Server};'
                                  'Server=LOANPIA\SQLEXPRESS;'
                                  'Database=Weather;'
                                  'Trusted_Connection=yes;')
            cursor = conn.cursor()

            cursor.execute("INSERT INTO weather (dow, status) values(?,?)", row2['dow'], row2['status'])
            conn.commit()
            cursor.close()

    for i in range(len(list_datewts)):
        row = "{},{}\n".format(list_datewts[i],list_descWeaths[i]) #type format string: "{}".format()
        data_save_file_csv.append(row)

    today_ = (datetime.datetime.now()).strftime('%Y%m%d') #get current timestamp and format YYYYmmdd
    filename = f"{today_}.csv" #type format string: f"{}" embbed string ez
    with open(os.path.join('data', filename),'a', encoding='utf-8') as f: #overwriting on old file - not continue to write
        f.writelines(data_save_file_csv)

    # time.sleep(3) #stop with 3s after start website page
    driver.close() #notice

    #this script update into 1 file daily --task schedule --Test: 10minutes foreach once time
    #####Author: @LoanPia#####25022023#####