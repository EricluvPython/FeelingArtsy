from __future__ import print_function

import shutil
import imghdr
import os
import concurrent.futures
import requests
import socket

from PIL import Image

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Proxy-Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
    "Accept-Encoding": "gzip, deflate, sdch",
} # for pretending to be a human

# download a single image from one image url
def download_image(image_url, dst_dir, file_name, timeout=20):

    response = None
    file_path = os.path.join(dst_dir, file_name)
    try_times = 0 # I will try to download a picture multiple times
    while True:
        try:
            try_times += 1
            response = requests.get(image_url, headers=headers, timeout=timeout)
            with open(file_path, 'wb') as f:
                f.write(response.content)
            response.close()
            file_type = imghdr.what(file_path) # get image file type
            if file_type in ["jpg", "jpeg", "png", "bmp", "webp"]:
                new_file_name = "{}.{}".format(file_name, file_type)
                new_file_path = os.path.join(dst_dir, new_file_name)
                shutil.move(file_path, new_file_path) # rename valid files
                # resize image
                with Image.open(new_file_path) as img:
                    resized = img.resize((100,100)) # resize and save
                    resized.save(new_file_path)
            else:
                os.remove(file_path)
            break
        except Exception as e:
            if try_times < 3:
                continue
            if response:
                response.close()
            break

# automatically download images from image urls with multithread
def download_images(image_urls, dst_dir="./downloaded", file_prefix="img", timeout=40):
    
    socket.setdefaulttimeout(timeout)
    # proletariats
    with concurrent.futures.ThreadPoolExecutor(max_workers=200) as executor:
        future_list = []
        count = 0
        if not os.path.exists(dst_dir): # create folder
            os.makedirs(dst_dir)
        for image_url in image_urls:
            file_name = file_prefix + "_" + "%04d" % count
            future_list.append(executor.submit(download_image, image_url, dst_dir, file_name, timeout))
            count += 1
        concurrent.futures.wait(future_list, timeout=180)
