from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time, random, pyautogui as pg

TIMELIMIT = 6000     # 1 hour timeout
TIMEINTERVAL = 0.05  # wait 0.05 between words
TIMEINT_ERR = 0.02   # 0.05 +- 0.02
TYPOS_RATE = 0.20    # 15% percent error
TIMECONTROL = 30     # Gamemode in monkeytype

service = Service(executable_path='chromedriver.exe')
driver = webdriver.Chrome(options=Options(), service=service)

# get the browser ready
driver.get('https://monkeytype.com/')
button = driver.find_element(by=By.XPATH, value='//*[@id="cookiePopup"]/div[2]/div[2]/button[1]')
driver.execute_script('arguments[0].click()', button)
time.sleep(0.5)

# hint program running
driver.execute_script('alert("Click ~ To Activate The Bot")')

def randomize_typing_speed( words, intervals, error_rate, typos_rate):
    def add_noise():
        if random.random() > 0.5:
            return intervals+(random.random() * error_rate)
        else:
            return intervals-(random.random() * error_rate)
    
    def add_errors():
        error_words = ['during','point','place','from','problem','which','world','begin','face','go']
        if random.random() > (1 - typos_rate):
            random_word = random.choice(error_words)
            pg.write(random_word, interval=add_noise())
            pg.press('backspace', presses=len(random_word), interval=add_noise())
        
    for i in words.split('\n'):
        add_errors()
        pg.write(i + " ", interval=add_noise())

while True:
    WebDriverWait(driver, TIMELIMIT).until_not(EC.alert_is_present())
    
    # wait for keystroke then activate bot
    driver.execute_script('''
        function keyDownTextField(e) {
            var keyCode = e.keyCode;
            console.log(keyCode)
            if (keyCode == 192) {
                document.removeEventListener("keydown", keyDownTextField, false);
                alert("Bot Activated!")
            }   
        }
        document.addEventListener("keydown", keyDownTextField, false);
    ''')
    WebDriverWait(driver, TIMELIMIT).until(EC.alert_is_present())
    time.sleep(1.5)

    # actual logic
    start = time.time()
    words = ''
    while time.time() - start < TIMECONTROL:
        temp = driver.find_element(by=By.XPATH, value='//*[@id="words"]').text
        words = temp[temp.find(words[-10:])+10:] if len(words) != 0 else temp
        randomize_typing_speed(words, TIMEINTERVAL, TIMEINT_ERR, TYPOS_RATE)
    
    # finished execution
    driver.execute_script('alert("Bot Finished Typing. Click ~ To Reactivate")')