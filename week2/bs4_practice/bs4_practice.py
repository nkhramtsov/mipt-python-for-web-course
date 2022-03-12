from typing import List, Dict
from collections import deque
import bs4
import re
import os


def build_bridge(path: str, start_page: str, end_page: str) -> List[str]:
    visited = set()
    queue = deque()
    queue.append(start_page)
    children_to_parent = {}
    while queue:
        page = queue.popleft()
        if page == end_page:
            return restore_path(children_to_parent, start_page, end_page)
        for link in get_links(path, page):
            if link in os.listdir(path):
                if link not in visited:
                    visited.add(link)
                    queue.append(link)
                    children_to_parent[link] = page


def get_links(path, page) -> List[str]:
    with open(os.path.join(path, page), encoding='utf-8') as file:
        links = re.findall(r"(?<=/wiki/)[\w()]+", file.read())
    return links


def restore_path(data: Dict[str, str], start: str, end: str) -> List[str]:
    current = end
    path = [current]
    while current != start:
        path.append(data[current])
        current = data[current]
    path.reverse()
    return path


def get_statistics(path: str, start_page: str, end_page: str) -> Dict[str, List[int]]:
    statistic = {}
    pages = build_bridge(path, start_page, end_page)
    for page in pages:
        statistic[page] = parse(os.path.join(path, page))
    return statistic


def parse(path_to_file: str) -> List[int]:
    with open(path_to_file, encoding="utf-8") as file:
        soup = bs4.BeautifulSoup(file, 'html.parser')

    body = soup.find('div', id='bodyContent')

    imgs = len(body.find_all('img', width=lambda width: int(width or 0) > 199))

    headers = len([header for header in body.find_all(re.compile(r'[hH1-6]{2}')) if header.text[0] in 'ETC'])

    links_len = 0
    link_found = body.find_next('a')
    while link_found:
        local_link_len = 1
        for i in link_found.find_next_siblings():
            if i.name == 'a':
                local_link_len += 1
            else:
                break
        links_len = max(links_len, local_link_len)
        link_found = link_found.find_next('a')

    lists = 0
    html_lists = body.find_all(['ul', 'ol'])
    for html_list in html_lists:
        if not html_list.find_parents(['ul', 'ol']):
            lists += 1

    return [imgs, headers, links_len, lists]


path = 'wiki/Stone_Age'
print(parse(path))
print(get_statistics('wiki/', 'The_New_York_Times', "Binyamina_train_station_suicide_bombing"))
