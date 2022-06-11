import os,sys,requests,io
from bs4 import BeautifulSoup as bs
from urllib.parse import urlparse

def download_file(link,path):
    
    headers = {"User Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36"}
    encode_url = "https://1filedownload.com/encode.php?url=" + link
    res = requests.get(encode_url,headers=headers)
    
    req_url = res.history[-2].url
    parsed_url = urlparse(req_url)
    capture_value = parsed_url.query
    download_link = "https://1filedownload.com/download.php?" + capture_value
    res_file = requests.get(download_link,headers=headers,stream=True)
    filename = link.split("/")[-1]
    
    buffer = io.BytesIO()
    print("Starting Download....{0}".format(filename))
    for chunk in res_file.iter_content(chunk_size=1024*256):
        if(chunk):
            buffer.write(chunk)
    file = open(path + filename,"wb")
    file.write(buffer.getvalue())
    file.close()
    print("Download Complete!!!")


def create_directory_hierarchy(path):

    headers = {"User Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36"}
    res = requests.get("https://1filedownload.com/magoosh-gre-videos-1-download/",headers=headers)
    parser = bs(res.text,"html.parser")
    
    
    #get all folder names
    folder_names = []
    for tag in parser.select("h3,h2"):
        folder_names.append(tag.text.split())


    #get all video links
    temp = ""
    video_links = []
    num_links = 0
    for link in parser.find_all("a",href=True):
        temp = link["href"].split("/")[-1]
        if(temp.split("-")[0].isdigit()):
            video_links.append(link["href"])
            num_links += 1

    
    #check for existing path
    if path.split("/")[-1] != "":
        path = path + "/"
    if os.path.exists(path) == False:
        try:
            os.mkdir(path)
            print("Folder Created Successfully")
        except OSError as error:
            print(error)


    #creating folder and adding videos
    temp_path = ""
    check = -1
    index = 0
    folder_name_tostr = ""

    for folder_name in folder_names[0:-2]:
        if(folder_name[0].isdigit() == False):
            folder_name_tostr = '_'.join(map(str,folder_name)).lower()
            sub_path = path + folder_name_tostr + "/"
            temp_path = sub_path
            if(folder_name_tostr == "intro_to_the_gre"):
                check = 1
        else:
            folder_name_tostr = '_'.join(map(str,folder_name)).lower()
            if(folder_name_tostr == "02_arithmetic_and_fractions"):
                download_file("https://1filedownload.com/wp-content/uploads/2020/11/How-To-Use-A-Gre-Study-Schedule.mp4",temp_path)
            temp_path = sub_path + folder_name_tostr + "/"
            check = 1    

        try:
            os.mkdir(temp_path)
            print("Folder {0} Created Successfully".format(folder_name_tostr))
        except OSError as error:
            print(error)

        if(check == 1):
            value = 0
            while(index < num_links):
                if(int(video_links[index].split("/")[-1].split("-")[0]) == 1):
                    value += 1
                    if(value == 2):
                        break
                
                download_file(video_links[index],temp_path)
                index += 1

        check = -1


if __name__ == "__main__":
    create_directory_hierarchy(sys.argv[1])
