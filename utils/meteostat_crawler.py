# Reference: I referenced the code from a friend and tweaked it accordingly.
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import date, timedelta
import os
import shutil
import glob
import unidecode
import argparse
import sys
from selenium_stealth import stealth
import random

def preprocess_province_name(province_name):
    provinces=["An Giang", "Bắc Giang", "Bắc Kạn", "Bạc Liêu", "Bắc Ninh", "Vũng Tàu", 
    "Bến Tre", "Bình Định", "Bình Dương", "Bình Phước", "Bình Thuận", "Cà Mau", 
    "Cao Bằng", "Đắk Lắk", "Đắk Nông", "Điện Biên", "Đồng Nai", "Đồng Tháp", "Gia Lai", 
    "Hà Giang", "Hà Nam", "Hà Tĩnh", "Hậu Giang", "Hòa Bình", "Hưng Yên", "Khánh Hòa", 
    "Kiên Giang", "Kon Tum", "Lai Châu", "Lâm Đồng", "Lạng Sơn", "Lào Cai", "Long An", 
    "Nam Định", "Nghệ An", "Ninh Bình", "Ninh Thuận", "Phú Thọ", "Phú Yên", "Quảng Bình", 
    "Quảng Nam", "Quảng Ngãi", "Quảng Ninh", "Quảng Trị", "Sóc Trăng", "Sơn La", 
    "Tây Ninh", "Thái Bình", "Thái Nguyên", "Thanh Hóa", "Huế", "Tiền Giang", 
    "Trà Vinh", "Tuyên Quang", "Vĩnh Long", "Vĩnh Phúc", "Yên Bái", "Cần Thơ", "Hải Phòng", 
    "Hà Nội", "Hồ Chí Minh", "Đà Nẵng", "Hải Dương"]
    new_province_name = unidecode.unidecode(province_name).lower().replace(" ", "")
    for province in provinces:
      element_province_name =unidecode.unidecode(province).lower().replace(" ", "")
      if element_province_name == new_province_name:
        return province

parser = argparse.ArgumentParser()
print(sys.executable)
parser.add_argument('--province_name', type=str, required=True)# Province name to search
parser.add_argument('--days', type=int, required=True)# Days to search
args = parser.parse_args()
extension_path = os.path.join(os.getcwd(),'Extension')
province_name = preprocess_province_name(args.province_name)
days = args.days


pd.set_option("display.width",None) # Không giới hạn chiều rộng hiển thị dữ liệu, pandas tự động xac định chiều rộng hiển thị phù hợp với cửa sổ hiện tại
dir_path = os.path.join(os.getcwd(),'data/meteostat/un_preprocessed') 
os.chdir(dir_path) # Thay đổi thư mục làm việc hiện tại sang thư mục dir_path

def Initialize_driver():
  user_agents = [
    # Add your list of user agents here
    # Bạn có thể xem thêm tại đây: https://www.whatismybrowser.com/guides/the-latest-user-agent/windows
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
  ]

  # select random user agent
  user_agent = random.choice(user_agents)
  # Bạn cũng có thể tùy chọn cấu hình cho phù hợp với như cầu sử dụng
  chrome_options = webdriver.ChromeOptions()
  chrome_options.add_argument("--no-sandbox") # Không sử dụng sandbox
  chrome_options.add_argument("--headless=new") # không sử dụng giao diện
  chrome_options.add_argument("--disable-gpu") # disable gpu
  chrome_options.add_argument("--start-maximized") 
  chrome_options.add_argument("--disable-infobars")
  # chrome_options.add_argument("--disable-extensions") # Có cho phép sử dụng extensions trên agent hay không
  chrome_options.add_argument('--log-level=3') # Log cấp 3: log error, warning and information
  chrome_options.set_capability("browserVersion", "117")
  chrome_options.add_extension(os.path.join(extension_path,"AdBlock.crx")) # Extension bạn sẽ sử dụng
  chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
  chrome_options.add_experimental_option("prefs", {
        "download.default_directory": os.path.abspath(dir_path),
        # "download.prompt_for_download": False,
        # "download.directory_upgrade": True,
        # "safebrowsing_for_trusted_sources_enabled": False,
        # "safebrowsing.enabled": False
        })
  chrome_options.add_argument("--window-size=1366x768") # Kích thước của cửa sổ làm việc (nên là kích thước mìn hình máy tính của bạn)
  chrome_options.add_argument(f'user-agent={user_agent}')
  driver = webdriver.Chrome(options=chrome_options)
  stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True)
  wait = WebDriverWait(driver, 20)
  driver.implicitly_wait(20)
  return driver,wait

"""
Sử dụng selenium thì trước tiên bạn cần phải thử trực tiếp bằng tay trên trang web, sau đó 
bạn sẽ nắm được các bước mà bạn muốn agent của mình thực hiện theo các bước đó.

Hãy chú ý đến quảng cáo của trang web, nếu quảng cáo gây ảnh hưởng đến toàn bộ của sổ làm việc
cũng như làm thay đổi url của trang web thì chắc chắn rằng bạn cần phải sử dụng một công cụ chặn quảng cáo.
Nếu quảng cáo không gây ảnh hưởng thì có thể không cần sử dụng công cụ chặn quảng cáo.

Để sự dụng tốt selenium bạn cần phải kiểm tra cấu trúc source code của trang web bằng f12. Bạn cần biết chính xác từng nút
cũng như event của chúng như nào, có làm thay đổi url không, nếu có hãy chia nhỏ các url này.

"""

def download_csv(dir_path,province_name,wait,driver): # Màb hình download dữ liệu, với định dạng được chọn là CSV
  old_filepath = os.path.join(dir_path,'export.csv')# This is where the downloaded save
  new_province_name = unidecode.unidecode(province_name.lower().replace(" ", "_"))
  new_filepath = os.path.join(dir_path,f'meteostat_dataset_{new_province_name}.csv')# This is where and new name we want to save it
  #Find download button
  download_but = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH,'//*[@id="app"]/div/main/div/div/div/div[1]/div[1]/div[1]/button[1]')))
  print("Now wait to install")
  if(download_but.is_enabled()):
    driver.execute_script("arguments[0].click();", download_but)# click on download button
    csv_button = wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="formatSelect"]/option[4]')))# Choose csv as file format
    csv_button.click()
    save_button = wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="export-modal"]/div/div/div[3]/button')))#Find save button
    driver.execute_script("arguments[0].click();", save_button)# click on save button
    #Wait until the file is downloaded
    print("Installing ...")
    while not os.path.exists(old_filepath):
      print('Wait until file is download!!!')
      time.sleep(2)
    #Rename the file
    shutil.copy(old_filepath,new_filepath)
    os.remove(old_filepath)

def merge_csv(province_name):
  province_dataset_path = os.path.join(dir_path,f'meteostat_dataset_{province_name}')
  csv_files = glob.glob(f'{province_dataset_path}*.csv')# Get all .csv file that contain province_name in its name
  if len(csv_files)!=0:# If we found more than 1 file, we need to concatenate them together
    df_csv_concat = pd.concat([pd.read_csv(file) for file in csv_files], ignore_index=True)
    df_csv_concat = df_csv_concat.loc[:, ~df_csv_concat.columns.str.contains('^Unnamed')]
    df_csv_concat = df_csv_concat.drop_duplicates()
    df_csv_concat = df_csv_concat.sort_values(by='time').reset_index(drop=True)
    for csv_file in csv_files:# Remove all file we found
      os.remove(csv_file)
    df_csv_concat.to_csv(f'{dir_path}/meteostat_dataset_{province_name}.csv')
  else: # If there is no file, return 
    return

def crawl_meteostat_data(province_name, days):
  print(province_name)
  # We can search the province name by 2 ways
  # 1. With no space between letters: hochiminh
  # 2. With space between letters: ho chi minh
  # province name need to be in lowercase, and need to be removed Vietnamese Accents
  province_name_types=[province_name,''.join(unidecode.unidecode(province_name).split()).lower(),unidecode.unidecode(province_name).lower()]
  num_unsearchable=0
  # while (not success) and (num_unsearchable<3):# search until we succeed or we get 5 errors
  for province_name_type in province_name_types:# Search with 3 ways
    continual_error=0
    ran = False
    start_date='' #The start day of our historical data
    end_date=''   #The end day of our historical data
    hold_date=date.today()  #This will hold the start day everytime you get error
    search_url = 'https://meteostat.net/en/'
    # The maximum of every search is about 10 years
    # Show if we search more than 10 years, we need to search more than 1 time
    remain_days = days# The day remain after every time we search
    while remain_days > 0 and (continual_error<5):#Loop until we get all days of data
      print('Number of countinual error:',continual_error)
      print("Remain days:", remain_days)
      try:#we may get error, when it does we need to start again
          if not ran:#If this is the first time we access https://meteostat.net/en/ in a specific way of searching
            #Click on reject cookie button
            driver,wait = Initialize_driver()#Innitial driver
            driver.get(search_url)  # Get the website
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,"//*[@id='cookieModal']/div/div/div[3]/button[1]"))).click()
            inputElement = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='search']")))
            inputElement.click()#click on search text box
            #Searching
            inputElement.send_keys(province_name_type)
            #Get first result            
            search_box= wait.until(EC.presence_of_element_located((By.XPATH,"//*[@id='app']/div/div[2]/nav/div/div[1]/div")))
            results = search_box.find_elements(By.XPATH,"./child::*")
            if len(results)==0:
              print("Province unsearchable!!!")
              num_unsearchable+=1
              break
            # print(len(first_result))
            new_province_name=unidecode.unidecode(province_name_type).lower().replace(" ", "")
            found_province=False
            for result in results:
              preprocessed_result = unidecode.unidecode(result.text).lower().replace(" ", "")
              if preprocessed_result == new_province_name or preprocessed_result == new_province_name+'city' :
                driver.execute_script("arguments[0].click();", result)
                print("Result clicked!!")
                time.sleep(10)
                found_province=True
                break
            if not found_province:
              print("No result matched!!!")
              break
            if(driver.current_url=='https://meteostat.net/en/#google_vignette' or driver.current_url=='https://meteostat.net/en/'):
              print('Ad block! Run from the begining!!!')
              driver.close()
              driver.quit() 
              continue
            end_date = date.today()#So the end day would be today
            ran =True
          else:
            end_date = start_date - timedelta(days=1)# If this is not the first time, the end_date is to continue the last start day we searched
          #The search range is 7 days or less
          start_date = end_date - timedelta(days=min(7,remain_days)-1)
          hold_date = end_date
          print("From ",start_date,"to ",end_date )
          new_page_url = driver.current_url.split('?')[0]+f'?t={start_date}/{end_date}'
          if 'vn'not in new_page_url: break
          # driver.get_screenshot_as_file("/content/screenshot.png")
          driver.close()
          driver.quit()
          #Incase of getting error: Max retries exceeded, we need to close and reinitalize the driver
          driver,wait = Initialize_driver()
          driver.get(new_page_url) # access the result website
          print(driver.current_url)
          wait.until(EC.element_to_be_clickable((By.XPATH,"//*[@id='cookieModal']/div/div/div[3]/button[1]"))).click()#Click the reject cookie button
          print("Reject Cookie clicked!")
          continual_error=0
          remain_days-= 7 #update the remain_days after we search
          download_csv(dir_path, province_name, wait, driver)


      except Exception as err:
          print(f"{type(err).__name__} was raised!!!")#print the error
          start_date = hold_date + timedelta(days=1)
          if type(err).__name__ == 'MaxRetryError':
            time.sleep(20)
          else:
            continual_error+=1
            time.sleep(2)
    if remain_days <=0:
      # success=True #mark that we succeed
      break
  time.sleep(2)
  merge_csv(unidecode.unidecode(province_name).lower().replace(" ", ""))# merge all csv file belonged to the same province after we search
crawl_meteostat_data(province_name,days)
