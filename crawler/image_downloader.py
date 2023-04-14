from __future__ import print_function

import crawler
import downloader

def main():

    keyword = input("Input search keyword:")

    crawled_urls = crawler.crawl_image_urls(keywords=keyword)
    downloader.download_images(crawled_urls,dst_dir="./"+keyword.replace(" ","_"))

    print("Finished.")


if __name__ == '__main__':
    main()
