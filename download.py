import requests
import os
import json
from tqdm import tqdm

# 下载图片
def download(url, dict):
    pic_name = url.split("/")[-1]
    response = requests.get(url)
    if response.status_code == 200:
        with open(f"{dict}/{pic_name}", 'wb') as file:
            file.write(response.content)
    else:
        print('File to download pic, Error:', response.status_code)

def pic_urls(file_path):
    file_name = file_path.split("/")[-1]
    print(f"Starting reading {file_name}")
    with open(file_path, "r", encoding="utf-8") as f:
        urls = []
        for line in f:
            url = json.loads(line).get("url")
            urls.append(url)
        
        return urls

def json_paths(folder_path):
    jsonl_path = [f for f in os.listdir(folder_path) if f.endswith(".jsonl")]
    return jsonl_path

if __name__ == "__main__":
    url = 'https://mir-s3-cdn-cf.behance.net/project_modules/1400/718e0d49306961.58b08aec5044d.jpg'
    json_path = "./results/Myth-002-Custom-BMW-R100GS-Touring-Motorcycletracking_source=curated_galleries_product-design.jsonl"
    folder_path = "./results/"

    for file_path in tqdm(json_paths(folder_path)):
        jsonl_path = (f"{folder_path}{file_path}")
        file_name = file_path.split(".")[0]
        image_path = f"download/{file_name}"
        os.makedirs(f"{image_path}", exist_ok=True)
        for url in tqdm(pic_urls(jsonl_path)):
            download(url, image_path)        
