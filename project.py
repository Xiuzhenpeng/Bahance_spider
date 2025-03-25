import time
import os
import json
import re
import warnings
from tqdm import tqdm

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from project_search import *

## Setup
warnings.filterwarnings("ignore", module="PIL")

chrome_driver_path = r'D:\Download\Chrome Download\134.0.6998.35 chromedriver-win64\chromedriver-win64\chromedriver.exe'
initial_url = 'https://www.behance.net/galleries/product-design/industrial-design'

chrome_service = Service(chrome_driver_path)

wd = webdriver.Chrome(service=chrome_service,)
wd.implicitly_wait(30)


# for now_url in project_urls:
def get_img(url):
    wd.get(url)
    time.sleep(5)

    # 滚动到底
    def scroll_to_bottom():
        previous_height = wd.execute_script("return document.body.scrollHeight")
        while True:
            wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)  # 等待新内容加载
            new_height = wd.execute_script("return document.body.scrollHeight")
            if new_height == previous_height:
                break
            previous_height = new_height

    scroll_to_bottom()

    # 循环滚动
    # previous_height = wd.execute_script("return document.body.scrollHeight")

    # while True:
    #     wd.execute_script('window.scrollBy(0, 5000)')
    #     time.sleep(2)  # 等待新内容加载
    
    #     new_height = wd.execute_script("return document.body.scrollHeight")
    
    #     if new_height == previous_height:
    #         break  # 如果高度没有变化，停止滚动
    
    #     previous_height = new_height

    # 等待图片元素加载
    wait = WebDriverWait(wd, 10)
    
    try:
        elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.ImageElement-image-SRv, .grid__item-image')))
    except:
        elements = []

    print(f"找到 {len(elements)} 个图片元素")

    srcs = []
    alts = []
    for element in elements:
        src = element.get_attribute('src')
        alt = element.get_attribute('alt')
        srcs.append(src)
        alts.append(alt)
    
    # wd.quit()
    return srcs, alts

def runner(url):
    src_list, alt_list = get_img(url)
    names = []
    urls = []
    alts = []
    for url, alt in zip(src_list, alt_list):
        name = url.split("/")[-1]
        names.append(name)
        urls.append(url)
        alts.append(alt)
    
    return names, urls, alts

def main(input_jsonl_path:str, output_path:str):
    os.makedirs(output_path, exist_ok=True)
    with open(input_jsonl_path, "r", encoding="utf-8") as f:
        for line in tqdm(f.readlines(), desc="处理项目"):
            new_url = json.loads(line.strip())
            project_name = re.sub(r'[\\/*?:"<>|]', "", new_url.split("/")[-1])
            new_json_path = os.path.join(output_path, f"{project_name}.jsonl")
            with open(new_json_path, "w", encoding="utf-8") as out_f:
                for name, url, alt in zip(*runner(new_url)):
                    json.dump({"name": name, "url": url, "alt": alt}, out_f, ensure_ascii=False,)
                    out_f.write("\n")

if __name__ == "__main__":
    output_dir = r"D:\Ai\projects\Bahance\from_wangchunhui\results"
    input_jsonl_path = r"D:\Ai\projects\Bahance\from_wangchunhui\wch_behance-car.jsonl"

    main(input_jsonl_path, output_dir)




    # for new_url in bahance_project_search(initial_url):
    #     project_name = new_url.split("/")[-1]
    #     sanitized_project_name = re.sub(r'[\\/*?:"<>|]', "", project_name)
    #     with open(f"results/{sanitized_project_name}.jsonl", "w") as f:
    #         for name, url, alt in zip(*runner(new_url)):
    #             json.dump({"name": name, "url":url, "alt": alt}, f, ensure_ascii=False,)
    #             f.write("\n")
    