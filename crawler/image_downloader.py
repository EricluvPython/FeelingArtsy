from __future__ import print_function

import crawler
import downloader

def main():

    keywords = ['happiness','love','excitement','sadness','loneliness','fear']
    for keyword in keywords:
        print("Processing",keyword)
        crawled_urls = crawler.crawl_image_urls(keywords=keyword)
        downloader.download_images(crawled_urls,dst_dir="./"+keyword.replace(" ","_"))
        print("Finished",keyword)
    print("Completed all searches!")


if __name__ == '__main__':
    main()
