import requests
from bs4 import BeautifulSoup
import sys
import time
from urllib.parse import urlparse


def download_url(url):
    try:
        headers = {
            "accept-encoding": "gzip, deflate, br",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"
        }
        resp = requests.get(url, headers=headers)
        return resp
    except:
        return download_url(url)


def main(url_file, max_url):
    t1 = time.time()
    urls = []
    crawled_url = []
    links = []
    domain = {
        "eecs.umich.edu",
        "eecs.engin.umich.edu",
        "ece.engin.umich.edu",
        "cse.engin.umich.edu"
    }

    files = [
        "jpg",
        "pdf",
        "png",
        "txt"
    ]

    with open(url_file, "r", encoding="utf-8") as f:
        for url in f.readlines():
            urls.append(url.strip())

    while len(crawled_url) < max_url:

        url = urls.pop(0)

        print(len(crawled_url) + 1, url)

        resp = download_url(url)
        soup = BeautifulSoup(resp.text, features="html.parser")
        for a in soup.find_all("a"):
            if not a.has_attr("href"):
                continue
            if not a["href"] or a["href"].split(".")[-1].lower() in files:
                continue
            href = a["href"]
            href = href[:-1] if href and href[-1] == "/" else href
            href = "https:" + href if href and href[0] == "/" else href
            url_parser = urlparse(href)
            if url_parser.netloc in domain:
                quote = (url, href)
                links.append(quote)
                    
                if url != href and href not in urls and href not in crawled_url:
                    urls.append(href)
                
        crawled_url.append(url)

    with open("crawler.output", "w") as f:
        f.write("\n".join(crawled_url))
        
    with open("links.output", "w") as f:
        f.write("\n".join(["\t".join(quote) for quote in links]))

    t2 = time.time()

    print(f"total times: {t2-t1}s")


if __name__ == '__main__':
    main(sys.argv[1], int(sys.argv[2]))
    # main("myseedURLs.txt", 2000)
    # total times: 4101.153804779053s