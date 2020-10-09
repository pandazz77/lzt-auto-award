from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
import time, requests
from bs4 import BeautifulSoup
import pytesseract, cv2
from urllib.request import urlopen
from PIL import Image
from progressbar import Percentage, ProgressBar,Bar,ETA

def getcaptcha(url):
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html,  "html.parser")
    with open("soup.txt","w",encoding="UTF-8") as file:
        file.write(str(soup))
    stroka = (str(soup.findAll('div', class_='ddText')))
    i1 = (stroka.rfind('<img src="'))+len('<img src="')
    i2 = (stroka.rfind('"/></label>'))
    captcha = (stroka[i1:i2])
    image = urlopen(captcha).read()
    with open("image.jpg", "wb") as f:
        f.write(image)
    img = cv2.imread('image.jpg')
    img = cv2.resize(img, None, fx=9, fy=9)

    pytesseract.pytesseract.tesseract_cmd ='Tesseract-OCR/tesseract.exe'
    result = pytesseract.image_to_string(img, config='--psm 6 -c tessedit_char_whitelist=0123456789+=?*')
    result = eval(result[:-3])

    i1 = (stroka.rfind('<label for="'))+len('<label for="')
    i2 = (stroka.rfind('"><img src='))
    
    inputfield = (stroka[i1:i2])
    xpath = '//*[@id="'+inputfield+'"]'
    driver.find_element_by_xpath(xpath).send_keys(result)
    driver.find_element_by_xpath(xpath).send_keys('\n')
def larray():
    driver.get('https://lolz.guru/forums/contests/')
    print('Прогрузка розыгрышей')
    for i in range(10):
        driver.find_element_by_tag_name('body').send_keys(Keys.END)
        time.sleep(2)
    time.sleep(2)
    html = driver.page_source
    soup = BeautifulSoup(html,  "html.parser")
    larray = []
    larray2 = []
    mydivs = soup.findAll("div", {"class": "discussionListItem unread prefix75"})
    for i in mydivs:
        larray.append(str(i))
    for i in range(len(larray)):
        larray2.append(larray[i][(larray[i].find('thread-'))+7:(larray[i].find('thread-'))+14])
    return(larray2)
def cycle():
    s=0
    e=0
    for i in larray():
        try:
            getcaptcha('https://lolz.guru/threads/'+i)
            s+=1
            print('Success!')
        except Exception as error:
            e+=1
            print('Error! '+str(error))
        time.sleep(5)
    print('End!\nSuccess: '+str(s)+'\nErrors: '+str(e))
options = webdriver.ChromeOptions()
options.add_argument("--enable-javascript")
driver = webdriver.Chrome(executable_path = "chromedriver.exe",chrome_options=options)
driver.get("https://lolz.guru/")
time.sleep(8)
print(input('Войдите в аккаунт и нажмите "Enter"'))
cookies = driver.get_cookies()
for cookie in cookies:
    driver.add_cookie(cookie)

while True:
    cycle()
    print('Restart in 60 minutes')
    N = 3600

    pbar = ProgressBar(widgets=[Bar('█', '[', ']'), ' ', Percentage(), ' ', ETA()],
                   maxval=N).start()
    for i in range(N+1):
        time.sleep(1)
        pbar.update(i)
    continue
driver.quit()