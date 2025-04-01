#!/usr/bin/python 

from bs4 import BeautifulSoup
import requests
import re
from enum import Enum

class Course:
    name: str
    code: str
    desc: str
    url: str
    offered: bool = True
    sameas: list
    prereqs: list
    prereqs_str: str = ""
    excl: list
    breadth: str
    def __init__(self):
        pass
        
        

class Program:
    name: str
    code: str
    coop: bool = False
    url: str
    level: str
    stream: str = ""
    courses: list[Course] = []
    def __init__(self):
        pass


def get_soup(url: str):
    page = requests.get(url)
            
    return BeautifulSoup(page.content, "html.parser")


def scrape_programs(programs: list[Program], courses: list[Course]) -> list[Program]:
    # Find all sections and programs
    soup = get_soup("https://www.utsc.utoronto.ca/registrar/unlimited-and-limited-programs")
    soup = soup.find_all("a", href=re.compile("https://utsc.calendar.utoronto.ca/"))
    for i in range(len(soup)):
        soup[i] = str(soup[i])
        title = soup[i][soup[i].find(">") + 1:-4]
        if title.count("-") > 1:
            prog = Program()
            prog.url = soup[i][soup[i].find("href=") + 6:soup[i].find(">") - 1]

            title = title.replace(u'\xa0', u' ')
            title = title.replace("&amp;", "&")
            title = title.split(" - ")
            prog.name = title[0]
            prog.level = title[-1]
            if len(title) == 3:
                prog.stream = title[1]

            if prog.level[:-5] == "Co-op":
                prog.coop = True
            
            programs.append(prog)
    
    for program in programs:
        scrape_program(program, courses)
    



def scrape_program(program: Program, courses: list[Course]):
    soup = get_soup(program.url)
    code = str(soup.find_all("h1", class_="page-title"))
    program.code = code[code.find(" - ") + 3:code.find("</")]
    print("Scraping Program " + program.code + " " + program.name + " " + program.level)

    soup = soup.find_all("a", href=re.compile("/course/"))

    for i in range(len(soup)):
        soup[i] = str(soup[i])
        code = soup[i][soup[i].find("/course/") + 8: soup[i].find("\">") - 0]

        new_course(code, courses)

def is_code(s: str) -> bool:
    return len(s) == 8 and s[4:6].isdigit() and s[:4].isalpha() and s.endswith("H3")
        

def new_course(code: str, courses: list[Course]) -> Course:
    if not is_code(code):
        return None
    # Handle if course already exists
    for course in courses:
        if course.code == code:
            return course
        
    # Create a new course
    course = Course()
    course.code = code
    courses.append(course)
    url = "https://utsc.calendar.utoronto.ca/course/" + code

    soup = BeautifulSoup(requests.get(url).content, "html.parser").find(role="main")

    if "Sorry" in str(soup):
        course.name = code
        course.offered = False
        return course

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
    
    print(course.code)
    print(course.excl)
    return course
    



if __name__ == "__main__":
    programs: list[Program] = []
    courses: list[Course] = []
    scrape_programs(programs, courses)

