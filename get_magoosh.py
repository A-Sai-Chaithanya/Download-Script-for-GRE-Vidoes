import os,sys,requests,io,threading,logging,time,colorama
from bs4 import BeautifulSoup as bs
from urllib.parse import urlparse

logging.basicConfig(filename="download.log",format="%(asctime)s %(message)s",filemode="w",force=True,level=logging.INFO)
link_count = 0
num_links = 0

def progress_bar(progress, total, color=colorama.Fore.WHITE):
    percent = 100 * (progress / float(total))
    bar = '█' * int(percent) + '-' * (100 - int(percent))
    print(color + "\r|{0}| {1:.2f}%".format(bar,percent),end="\r")
    if(progress == total):
        print(colorama.Fore.GREEN + "\r|{0}| {1:.2f}%".format(bar,percent),end="\r")


def finish_thread_exec():
    main_thread = threading.current_thread()
    for t in threading.enumerate():
        if t is not main_thread:
            t.join()


def download_file(link,path):
    global link_count,num_links
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
    logging.info("Starting Download....{0}".format(filename))
    for chunk in res_file.iter_content(chunk_size=1024*256):
        if(chunk):
            buffer.write(chunk)
    file = open(path + filename,"wb")
    file.write(buffer.getvalue())
    file.close()
    logging.info("Download Complete!!!")
    link_count += 1
    progress_bar(link_count, num_links+1)


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
    global num_links
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
            logging.info("Folder Created Successfully")
        except OSError as error:
            logging.info(error)


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
            logging.info("Folder {0} Created Successfully".format(folder_name_tostr))
        except OSError as error:
            logging.info(error)

        if(check == 1):
            value = 0
            while(index < num_links):
                if(int(video_links[index].split("/")[-1].split("-")[0]) == 1):
                    value += 1
                    if(value == 2):
                        break
                
                t = threading.Thread(target=download_file,args=(video_links[index],temp_path,))
                t.start()
                index += 1

                if(threading.active_count() >= 20):
                    finish_thread_exec()

        check = -1


if __name__ == "__main__":
    print("Download Started.....")
    start = time.time()
    create_directory_hierarchy(sys.argv[1])
    finish_thread_exec()
    end = time.time()
    print(colorama.Fore.RESET)
    print("Download Finished!!!")
    print("Total Download time : %02d minutes %02d seconds" % divmod(end-start,60))