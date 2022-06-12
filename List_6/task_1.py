import urllib.request
import re
import bs4 as bs

link_1 = "https://www.ii.uni.wroc.pl/~marcinm/dyd/python/"
link_2 = "https://www.python.org/"


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


def unique(list_of_unique_links, new_list):
    for link in new_list:
        if link not in list_of_unique_links:
            list_of_unique_links.append(link)
    return list_of_unique_links


def find_links(text):

    links = []
    link_list = re.findall(r"\<a\shref=\"http[^\"]*\"", text)
    for link in link_list:
        links.extend(re.findall(r"\".*[^\.svg]\"", link))

    return links


def search_site(link, distance, result_list, action, word):

    source = get_site_text(link)
    text = source[1]
    sentence_list = source[0]
    list_of_sentences = action(sentence_list, word)
    result = (link, sentence_list)
    print(result)
    if distance == 0:
        return
    else:
        link_list = find_links(text)
        unique_list = unique(result_list, link_list)

        for link in link_list:
            if link in unique_list:
                search_site(link, distance - 1, result_list, action, word)


def crawl_iterator(link, distance, action, word):
    result_list = []
    search_site(link, distance, result_list, action, word)



def crawl(link, distance, action):
    return crawl_iterator(link, distance, action, "Python")


link_1 = "https://www.ii.uni.wroc.pl/~marcinm/dyd/python/"
link_2 = "https://www.python.org/"

crawl(link_1, 1, find_occurrences)
crawl(link_2, 1, find_occurrences)