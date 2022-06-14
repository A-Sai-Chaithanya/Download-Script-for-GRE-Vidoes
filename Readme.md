# GRE Videos Download Script

This repo contains a python script to download Magoosh GRE Videos in [GRE-Videos](https://1filedownload.com/magoosh-gre-videos-1-download) website.
The entire workflow is automated using a bash script.

- Run the following commands to download:
    - chmod 744 ./download.sh 
    - ./download.sh "PATH"

##

- In place of **PATH** specify  **COMPLETE PATH** as to where you want to save the videos. 
    - For eg:  	"/usr/Documents/magoosh_videos"

##

- If path not specified, 
    1. The folder is downloaded in the current directory itself.
    2. All videos will be saved under "magoosh_videos" folder.

##

- A log file is generated that contains timestamps, folder_names and files_names in the downloaded order.
