from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import re
from config import *
import os,sys

count = 0 #记录中断位置

if os.path.exists(NEW_NAME):# 若存在则删掉
    os.remove(NEW_NAME)

def creat_driver():
    try:
        SET = ['--disk-cache=true','--load-images=false'] #phantomjs的一些配置，详见http://phantomjs.org/api/
        driver = webdriver.PhantomJS(service_args = SET)
        driver.set_window_size(1080,960)
        print("虚拟浏览器创建成功！")
        return driver
    except:
        print("虚拟浏览器创建失败！")

def translate_line(wait , keyword):
    print('Translating:',keyword)
    try:
        #控制输入
        input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#source')))  # 选择CSS选择器，创建输入框对象，并等待成功
        input.send_keys(keyword)
        sleep(SLEEP_TIME) #等待翻译成功
        # 获取结果
        result = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'body > div.frame > div.page.tlid-homepage.homepage.translate-text > div.homepage-content-wrap > div.tlid-source-target.main-header > div.source-target-row > div.tlid-results-container.results-container > div.tlid-result.result-dict-wrapper > div.result.tlid-copy-target > div.text-wrap.tlid-copy-target')))
        input.clear()
        return result.text
    except TimeoutException:
        input.clear()
        translate_line(wait,keyword)

def get_text(driver):
    wait = WebDriverWait(driver, 10)  # 创建wait对象

    if re.match(r'.*?\.ass$', FILE_NAME):
        print('This a ASS file: ',FILE_NAME,'\n')
        ass_file(wait)
    elif re.match(r'.*?\.srt$', FILE_NAME):
        print('This a SRT file: ',FILE_NAME,'\n')
        srt_file(wait)
    else:
        print('文件选择出错！')
        sys.exit()

def ass_file(wait):
    global count
    pattern_1 = re.compile(P_1, re.S)
    pattern_2 = re.compile(P_2, re.S)

    with open(NEW_NAME, 'a', encoding='utf-8') as new:

        with open(FILE_NAME, 'r', encoding='utf-8') as f:
            for line in f.readlines()[count:]:
                if re.match(pattern_2, line):
                    keyword = re.findall(pattern_2, line)[0].replace("\n", "")
                    result = translate_line(wait, keyword)
                    print('Result:', result)
                    print('After:', line.replace(keyword, result))
                    new.write(line.replace(keyword, result))
                elif re.match(pattern_1, line):
                    keyword = re.findall(pattern_1, line)[0].replace("\n", "")
                    result = translate_line(wait, keyword)
                    print('Result:', result)
                    print('After:', line.replace(keyword, result))
                    new.write(line.replace(keyword, result))
                else:
                    new.write(line)
                count += 1
        f.close()
    new.close()

def srt_file(wait):
    global count

    with open(NEW_NAME, 'a', encoding='utf-8') as new:

        with open(FILE_NAME, 'r', encoding='utf-8') as f:
            for line in f.readlines()[count:]:
                if re.match(r'^([a-zA-Z]).*?', line):
                    keyword = line.replace("\n", "")
                    result = translate_line(wait, keyword)
                    print('Result:', result,'\n')
                    new.write(line.replace(keyword, result))
                    new.write(line)
                else:
                    new.write(line)
                count += 1
        f.close()
    new.close()

#保存
def save_new():
    if re.match(r'.*?\.ass$', FILE_NAME):
        end = '.ass'
    elif re.match(r'.*?\.srt$', FILE_NAME):
        end = '.srt'
    new_file_path = FILE_NAME + '_backup'+ end
    if os.path.exists(new_file_path):
        os.remove(new_file_path)
    with open(NEW_NAME,'r',encoding='utf-8') as new:
        with open(new_file_path, 'w',encoding='utf-8') as f_back:
            f_back.writelines(new.readlines())
            f_back.close()
    new.close()

def main():
    global count
    try:
        driver = creat_driver()
        print("Start Point:",count)
        driver.get(URL)
        get_text(driver)
    except Exception:
        print('\n出错，正在重试...\n')
        driver.close()
        main()
    finally:
        print('翻译结束！')
        save_new()
        driver.close()

if __name__ == '__main__':
    main()
    