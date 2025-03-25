import requests
import os
import json
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

def download(url, dir_path):
    pic_name = url.split("/")[-1]
    response = requests.get(url)
    if response.status_code == 200:
        with open(f"{dir_path}/{pic_name}", 'wb') as file:
            file.write(response.content)
    else:
        print(f'Failed to download pic: {url}, Error: {response.status_code}')

def process_jsonl(file_path):
    image_path = f"download/{os.path.splitext(os.path.basename(file_path))[0]}"
    os.makedirs(image_path, exist_ok=True)
    
    urls = []
    with open(file_path, "rb") as f:
        for line in f:
            try:
                for encoding in ['utf-8', 'iso-8859-1', 'windows-1252']:
                    try:
                        decoded_line = line.decode(encoding)
                        url = json.loads(decoded_line).get("url")
                        if url:
                            urls.append(url)
                        break
                    except UnicodeDecodeError:
                        continue
                    except json.JSONDecodeError:
                        print(f"Invalid JSON in file {file_path}")
                        break
            except Exception as e:
                print(f"Error processing line in {file_path}: {e}")
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(lambda url: download(url, image_path), urls)
    
    return len(urls)

def main(folder_path):
    jsonl_paths = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith(".jsonl")]
    
    total_urls = 0
    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_file = {executor.submit(process_jsonl, file_path): file_path for file_path in jsonl_paths}
        
        with tqdm(total=len(jsonl_paths), desc="Processing JSONL files") as pbar:
            for future in as_completed(future_to_file):
                file_path = future_to_file[future]
                try:
                    urls_count = future.result()
                    total_urls += urls_count
                    pbar.update(1)
                    pbar.set_postfix({"Total URLs": total_urls})
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")
    
    print(f"Total URLs processed: {total_urls}")

if __name__ == "__main__":
    folder_path = r".\from_wangchunhui\results"
    main(folder_path)
