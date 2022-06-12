import urllib.request
import re
import bs4 as bs
import time
import concurrent.futures

t1 = time.time()


def get_site_text(link):
    source = urllib.request.urlopen(link.replace("\"", "")).read()
    bs_source = bs.BeautifulSoup(source, 'lxml')
    raw_text = str(bs_source).strip()
    raw_text = " ".join(raw_text.split())
    text = bs_source.get_text()
    text = text.strip()
    text = " ".join(text.split())
    sentences_re = re.compile(r'([A-Z][^\.!?]*[\.!?])', re.M)
    sentences = sentences_re.findall(text)
    return sentences, raw_text


def find_occurrences(sentence_list, word):
    new_list = []
    for sentence in sentence_list:
        if sentence.count(word) > 0:
            new_list.append(sentence)
    return new_list


def unique(unique_links, new_link_list):
    for link in new_link_list:
        if link not in unique_links:
            unique_links.append(link)
    return unique_links


def find_links(text):
    links = []
    link_list = re.findall(r"\<a\shref=\"https[^\"]*\"", text)
    for link in link_list:
        links.extend(re.findall(r"\".*[^\.svg]\"", link))

    return links


def search_site(url, distance, unique_link_list, result_list, action, word):
    source = get_site_text(url)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        temp_link_list = executor.submit(find_links, source[1]).result()
        temp_sentence_list = executor.submit(action, source[0], word).result()
        unique_link_list = executor.submit(unique, unique_link_list, temp_link_list).result()

    if len(temp_sentence_list) > 0:
        result_list[url] = temp_sentence_list

    if distance == 0:
        return result_list

    with concurrent.futures.ThreadPoolExecutor() as link_executor:
        for link in temp_link_list:
            if link in unique_link_list:
                print(link)
                link_executor.submit(search_site, link, distance - 1, unique_link_list, result_list, action, word)


def crawl_iterator(link, distance, action, word):
    result_list = {}
    link_list = []
    search_site(link, distance, link_list, result_list, action, word)
    return result_list


def crawl(link, distance, action):
    return crawl_iterator(link, distance, action, "Python")


link_1 = "https://www.ii.uni.wroc.pl/~marcinm/dyd/python/"
link_2 = "https://www.python.org/"

sentence_list = crawl(link_2, 1, find_occurrences)

for link in sentence_list.keys():
    print(link, sentence_list[link])

t2 = time.time()

print(t2 - t1)
