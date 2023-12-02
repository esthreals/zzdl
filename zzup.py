import urllib.request
import os



def main():
    url = input("Url of the gallery \(https://zzup.com/content/ABCDEFIJKLMN/Gallery_Name/ABCD/index.html):\n")
    url = url.replace(url.split("/")[-1], "")  + "page-1.html"
    gallery_name = url.split("/")[5]
    print("\nGallery name:", gallery_name)

    gallery_file = gallery_name + ".txt"
    if os.path.isfile(gallery_file):
        while True:
            choice = input("The file " + str(gallery_file) + " already exists, do you want to overwrite it? (y=yes, n=no)")
            if (choice == "y"):
                break
            elif (choice == "n"):
                return
            else:
                print("Type either 'y' or 'n', try again")

    request =  urllib.request.Request(url, 
                                    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0'})
    response = str(urllib.request.urlopen(request).read())

    image_large_url = "https://zzup.com/viewimage/" + response.split("href=\"/viewimage/")[1].split("\"")[0]
    num_images = int(image_large_url.split("-pics-")[1].split("-")[0])
    print("Number of images:", num_images)

    request_image =  urllib.request.Request(image_large_url, 
                                            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0'})
    response_image = str(urllib.request.urlopen(request_image).read())

    image_url = "https://zzup.com/" + response_image.split("<img src=\"")[2].split("\"")[0]
    image_links = image_url + "\n"
    for i in range(2, num_images+1):
        image_links += image_url.replace("image00001", "image"+str(i).zfill(5)) + "\n"
    
    f = open(gallery_file, "w")
    f.write(image_links)
    f.close()

    print("Image links are saved to the file '" + str(gallery_file) + "' in " + str(os.getcwd()))


if __name__ == "__main__":
    main()
