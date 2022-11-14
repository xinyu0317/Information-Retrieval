import numpy as np
import sys
from tqdm import tqdm


def main(crawler_file, links_file, tol):
    d = 0.85
    init = 0.25

    with open(crawler_file, "r", encoding="utf-8") as f:
        urls = [x.strip() for x in f.readlines()]

    links_dict = dict()
    with open(links_file, "r", encoding="utf-8") as f:
        links = [x.strip().split() for x in f.readlines()]

    for link_in, link_out in tqdm(links):
        if link_in in urls and link_out in urls:
            if link_in in links_dict:
                links_dict[link_in].append(link_out)
            else:
                links_dict[link_in] = [link_out]

    A = np.zeros((len(urls), len(urls)))
    for i in range(len(urls)):
        url_i = urls[i]
        n = len(links_dict.get(url_i, []))
        for url_j in links_dict.get(url_i, []):
            j = urls.index(url_j)
            A[i][j] = links_dict.get(url_i, []).count(url_j) / n

    A = A.T
    N = len(urls)
    A_p = d * A + ((1 - d) / N) * np.ones_like(A)

    p = init * np.ones(len(urls))

    e = np.inf
    step = 0
    while e > tol:
        step += 1
        r = np.dot(A_p, p)
        e = np.sum(np.abs(r - p))
        p = r

    p = p / float(sum(p))

    print(step)

    links_order = sorted(zip(urls, p), key=lambda x: x[1], reverse=True)
    with open("pagerank.output", "w", encoding="utf-8") as f:
        f.write("\n".join([
            f"{x[0]}\t{x[1]:.8f}" for x in links_order
        ]))


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], float(sys.argv[3]))
    # main("crawler.output", "links.output", 0.001)