#!/usr/bin/python 

from bs4 import BeautifulSoup
import requests
import re
from enum import Enum
from datetime import datetime
import json

class Course:
    name: str = ""
    code: str = ""
    desc: str = ""
    url: str = ""
    offered: bool = True
    sameas: list
    prereqs: list
    prereqs_str: str = ""
    postreqs: list
    excl: list
    breadth: str = ""
        

class Program:
    name: str = ""
    code: str = ""
    coop: bool = False
    url: str = ""
    level: str = ""
    stream: str = ""
    courses: list[Course]
    section: str = ""
    


def get_soup(url: str):
    page = requests.get(url)
            
    return BeautifulSoup(page.content, "html.parser")


def scrape_programs(programs: list[Program], courses: list[Course]) -> list[Program]:
    print("0 courses found from 0 programs")
    # Find all sections and programs
    soup = get_soup("https://www.utsc.utoronto.ca/registrar/unlimited-and-limited-programs").find("div", class_="clearfix text-formatted field field--name-body field--type-text-with-summary field--label-hidden field__item").find_all("tr")
    for tr in soup:
        a = str(tr.find("a"))
        url = a[a.find("href=") + 6:a.find(">") - 1]
        if "-program-" in url:
            new_program(url, programs, courses)

    # soup = soup.find_all("a", href=re.compile("https://utsc.calendar.utoronto.ca/"))
    # for i in range(len(soup)):
    #     soup[i] = str(soup[i])
    #     title = soup[i][soup[i].find(">") + 1:-4]
    #     if title.count("-") > 1:
    #         url = soup[i][soup[i].find("href=") + 6:soup[i].find(">") - 1]
    #         new_program(url, programs, courses)
            
    




def new_program(url: str, programs: list[Program], courses: list[Course]):
    soup = get_soup(url).find(role="main")
    if soup == None or soup.h1 == None or soup.h1.get_text().strip() == "Page not found" or soup.h1.get_text().strip() == "Program Search" or "DOUBLE" in soup.h1.get_text().strip().upper():
        return None
    
    program = Program()
    programs.append(program)

    program.url = url
    
    title = soup.h1.get_text().upper().replace(u'\xa0', u' ').replace("\n", "").split(" ")



    program.level = title[0]
    title.pop(0)
    program.code = title[-1]
    title.pop(-1)
    title.pop(-1)
    
    if title[0] == "(CO-OPERATIVE)":
        program.coop = True
        title.pop(0)
    else:
        program.coop = False
    
    
    title = title[2:]

    if title[-1] == "(ARTS)":
        program.section = "ARTS"
        title.pop(-1)
    elif title[-1] == "(SCIENCE)":
        program.section = "SCIENCE"
        title.pop(-1)
    else:
        program.section = "BACHELOR OF BUSINESS ADMINISTRATION"
        title = title[:-4]

    title = " ".join(title)
    title = title.split(" - ")

    program.name = title[0]
    if len(title) > 1:
        program.stream = title[1][:-7]

    soup = soup.find_all("a", href=re.compile("/course/"))

    program.courses = []

    for i in range(len(soup)):
        soup[i] = str(soup[i])
        code = soup[i][soup[i].find("/course/") + 8: soup[i].find("\">") - 0]
        new = new_course(code, courses)
        if new != None:
            program.courses.append(new)
    

def is_code(s: str) -> bool:
    return len(s) == 8 and s[4:6].isdigit() and s[:4].isalpha() and s.endswith("H3")
        

def new_course(code: str, courses: list[Course]) -> Course:
    code = code.upper()
    if not is_code(code) :
        return None
    # Handle if course already exists
    for course in courses:
        if course.code == code:
            return course
    
    url = "https://utsc.calendar.utoronto.ca/course/" + code
    soup = BeautifulSoup(requests.get(url).content, "html.parser").find(role="main")
    if "Sorry" in str(soup.h1):
        return None
        
    # Create a new course
    course = Course()
    course.code = code
    courses.append(course)
    print("\033[F" + str(len(courses)) + " courses found from " +str(len(programs)) + " programs") 
    course.postreqs = []

    course.url = url
    course.name = soup.h1.string[10:]
    course.desc = soup.p.get_text()
    
    course.prereqs = []
    course.prereqs_str = soup.find(class_="field--name-field-prerequisite")
    if course.prereqs_str != None:
        course.prereqs_str = course.prereqs_str.get_text().strip().replace("\n", "")[12:]

        for c in course.prereqs_str.replace("s and V", "s And V").replace(" and ", "$").replace(" or ", "$").split("$"):
            new = new_course(c.upper(), courses)
            if new != None:
                course.prereqs.append(new)
                new.postreqs.append(course)
       
    course.excl = []
    s = soup.find(class_="field--name-field-exclusion")
    if (s != None):
        for c in s.get_text().strip().replace("\n", "")[9:].replace(",", "").split(" "):
            new = new_course(c.upper(), courses)
            if new != None:
                course.excl.append(new)
    
    course.sameas = []
    for c in soup.p.find_all("a"):
        new = new_course(c.get_text().strip().upper(), courses)
        if new != None:
            course.sameas.append(new)
    
    s = soup.find(class_="field--name-field-breadth-requirements")
    if s != None:
        course.breadth = s.get_text().strip().replace("\n", " ").removeprefix("Breadth Requirements").strip()
    
    return course


def save_data(courses: list, programs: list, fname: str):
    pdata = {}
    for p in programs:
        pdata[p.code] = {}
        pdata[p.code]["name"] = p.name
        pdata[p.code]["coop"] = p.coop
        pdata[p.code]["url"] = p.url
        pdata[p.code]["level"] = p.level
        pdata[p.code]["stream"] = p.stream
        pdata[p.code]["section"] = p.section
        pdata[p.code]["courses"] = []
        for c in p.courses:
            pdata[p.code]["courses"].append(c.code)

    cdata = {}
    for c in courses:
        print(c.code)
        cdata[c.code] = {}
        cdata[c.code]["name"] = c.name
        cdata[c.code]["description"] = c.desc
        cdata[c.code]["prereqs_str"] = c.prereqs_str
        cdata[c.code]["breadth"] = c.breadth
        cdata[c.code]["url"] = c.url
        cdata[c.code]["offered"] = c.offered
        cdata[c.code]["sameas"] = []
        for s in c.sameas:
            cdata[c.code]["sameas"].append(s.code)
        cdata[c.code]["prereqs"] = []
        for p in c.prereqs:
            cdata[c.code]["prereqs"].append(p.code)
        cdata[c.code]["exclusions"] = []
        for e in c.prereqs:
            cdata[c.code]["exclusions"].append(e.code)
        cdata[c.code]["postreqs"] = []
        for p in c.postreqs:
            cdata[c.code]["postreqs"].append(p.code)

    with open(fname, "w") as fp:
        json.dump([datetime.today().strftime('%Y-%m-%d'), pdata, cdata], fp, sort_keys=True, indent=1)


if __name__ == "__main__":
    programs: list[Program] = []
    courses: list[Course] = []
    scrape_programs(programs, courses)
    save_data(courses, programs, "data.txt")

    
        


