import time
import warnings
import json

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

chrome_driver_path = r'D:\Download\Chrome Download\134.0.6998.35 chromedriver-win64\chromedriver-win64\chromedriver.exe'

warnings.filterwarnings("ignore", module="PIL")

def bahance_project_search(url):
    chrome_service = Service(chrome_driver_path)

    wd = webdriver.Chrome(service=chrome_service)
    wd.implicitly_wait(30)

    wd.get(url)

    input()

    wd.get(url)
    time.sleep(5)

    previous_height = wd.execute_script("return document.body.scrollHeight")
    
    while True:
        wd.execute_script('window.scrollBy(0, 20000)')
        time.sleep(2)  # 等待新内容加载
    
        new_height = wd.execute_script("return document.body.scrollHeight")
    
        if new_height == previous_height:
            break  # 如果高度没有变化，停止滚动
    
        previous_height = new_height

    elements = wd.find_elements(By.CSS_SELECTOR, '.ProjectCoverNeue-coverLink-U39')

    project_href = []
    for element in elements:
        href = element.get_attribute('href')
        project_href.append(href)
        
    print(f"Find {len(project_href)} project")
    
    wd.quit()
    return project_href

if __name__ == "__main__":
    initial_url = 'https://www.behance.net/galleries/product-design/industrial-design'
    with open(f"behance-industrial.jsonl", "w") as f:
        for project_url in bahance_project_search(initial_url):
            json.dump(project_url, f, ensure_ascii=False)
            f.write("\n")
