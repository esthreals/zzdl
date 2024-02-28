import os
import urllib.request, urllib.parse
import requests
from multiprocessing import Pool



def clean_dirname(name:str)->str:
    name = name.strip()
    illegal_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
    for char in illegal_chars:
        name = name.replace(char, '')
    return name
    

def dl(url:str, name:str)->None:
    r = requests.get(url, allow_redirects=True)
    open(name, "wb").write(r.content)


def download_collection(url:str, num_processes:int=6)->None:
    url_base = '/'.join(url.split("/")[:-1])
    url = url_base+"/index.html"
    dir = clean_dirname(url.split("/")[4])
    collection_page = scrape(url)
    num_pages = int(collection_page.split("1 / ")[1].split(" ")[0])

    for i in range(1, num_pages+1):
        url = url_base + "/page-"+str(i)+".html"
        collection_page = scrape(url)
        collection_list = collection_page.split("<a target=\"_blank\" href=\"/content/")
        for j in range(1, len(collection_list)):
            gallery_page_url = "https://zzup.com/content/" + collection_list[j].split("\"")[0]
            download_gallery(dir, gallery_page_url, num_processes)


def download_gallery(dir:str, url:str, num_processes:int=6)->None:
    url = '/'.join(url.split("/")[:-1])+"/index.html"
    gallery_page = scrape(url)
    gallery_name = gallery_page.split("<span style=\"font-weight: bold;font-size: 30px;\">")[1].split("<")[0]
    gallery_name = clean_dirname(gallery_name)
    total_dir = dir + "/" + gallery_name

    if not os.path.isdir(dir):
        os.mkdir(dir)
    if not os.path.isdir(total_dir):
        os.mkdir(total_dir)

    image_page_url = "https://zzup.com/viewimage/" + gallery_page.split("href=\"/viewimage/")[1].split("\"")[0]
    image_page = scrape(image_page_url)
    num_images = int(image_page.split("1 | ")[1].split(" ")[0])
    image_url = "https://zzup.com/" + image_page.split("<a href=\"/")[1].split("\"")[0]

    print("Downloading gallery: \""+gallery_name+"\" - " + str(num_images) + " images")
    pool = Pool(num_processes)
    params = []
    for i in range(1, num_images+1):
        params.append([image_url.replace("image00001", "image"+str(str(i).zfill(5))), total_dir+"/"+str(i).zfill(4)+".jpg"])
    pool.starmap(dl, params)


def scrape(url:str, data:dict=None)->str:
    if data != None:
        data = urllib.parse.urlencode(data).encode()
    user_agent = "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7"
    headers = {"User-Agent": user_agent}
    request = urllib.request.Request(url,data,headers)
    response = urllib.request.urlopen(request)
    data = response.read()
    return str(data)


def main():
    NUM_PROCESSES = 10
    url = input("URL: ")

    # Categorize URL
    if "https://zzup.com/search/" in url:
        download_collection(url, NUM_PROCESSES)
    elif "https://zzup.com/content/" in url:
        dir = clean_dirname(input("Directory name:"))
        download_gallery(dir, url, NUM_PROCESSES)
    else:
        print("Invalid URL. \nExamples: \nhttps://zzup.com/search/my_search/index.html, \nhttps://zzup.com/search/my_search/page-i.html, \nhttps://zzup.com/content/ABCDEFGHIJ==/Gallery_Name/ABC=/index.html")


if __name__ == "__main__":
    main()
