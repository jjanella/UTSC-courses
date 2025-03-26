#!/usr/bin/python

from bs4 import BeautifulSoup
import requests
import re
import sys

def na(css_class):
    return css_class is None

def get_prereqs(code: str):
    site = requests.get("https://utsc.calendar.utoronto.ca/course/" + code + "H3")
    soup = BeautifulSoup(site.content, 'html.parser')
    reqs = str(soup.find_all('div', class_=['w3-bar-item field__item'])[0])

    while reqs.find("<") != -1:
        start = reqs.index("<")
        end = reqs.index(">")
        reqs = reqs[0:start] + reqs[end+1:]
    
    reqs = reqs.removesuffix(" and [CGPA 3.5 or enrolment in a CSC Subject POSt]")

    # reqs = reqs.replace("or", "and")
    # reqs = reqs.replace("[", "")
    # reqs = reqs.replace("]", "")
    reqs = reqs.replace("H3", "")
    reqs = reqs.split(" and ")
    for i in range(len(reqs) - 1, -1, -1):
        if len(reqs[i]) != 6 or reqs[i].find("(") != -1:
            reqs.pop(i)
    return reqs



if __name__ ==  "__main__":
    assert(len(sys.argv) == 2)
    pres = []
    queue = [sys.argv[1]]
    while queue != []:
        code = queue.pop()
        if code not in pres:
            queue.extend(prereqs(code))
            pres.append(code)
    
    print(pres)
    

