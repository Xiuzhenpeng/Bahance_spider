# 用于Bahance的爬虫项目
## 介绍
使用selenuim库来对Bahance爬虫

## 依赖
- 浏览器
- 浏览器驱动(同版本)

## 用法
分三步进行爬取

1. 根据精选作品的链接获取项目地址并存储在一个jsonl文件内  
project_search.py
2. 根据第一步产生的jsonl文件，对项目内的图片进行爬取
每个项目产生一个jsonl文件，存储图片名；地址；alt值  
project.py
3. 根据步骤二产生的项目图片jsonl，进行下载，每个项目单独存储文件夹  
download_batch.py 或 download.py

## License
请遵循Bahance的爬虫机器人许可  
[Bahance Robots TXT](https://www.behance.net/robots.txt)