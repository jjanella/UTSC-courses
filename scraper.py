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
        

class Program:
    name: str
    code: str
    coop: bool
    url: str
    level: str
    stream: str = ""
    courses: list[Course] = []
    section: str = ""
    


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
            
            programs.append(prog)
    
    for program in programs:
        try:
            scrape_program(program, courses)
        except:
            programs.remove(program)
    



def scrape_program(program: Program, courses: list[Course]):
    program.courses = []
    soup = get_soup(program.url)
    code = str(soup.find_all("h1", class_="page-title"))
    program.code = code[code.find(" - ") + 3:code.find("</")]

    title = str(soup.find("span", string = re.compile("PROGRAM")))
    title = title[6:-7]
    title = title.replace(u'\xa0', u' ')
    if " - " not in title:
        raise()

    title = title.split(" ")
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



    for i in range(len(soup)):
        soup[i] = str(soup[i])
        code = soup[i][soup[i].find("/course/") + 8: soup[i].find("\">") - 0]

        program.courses.append(new_course(code, courses))
    

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
    
    return course
    



if __name__ == "__main__":
    # print(Course("BIOA11", []).prereqs)
    programs: list[Program] = []
    courses: list[Course] = []
    scrape_programs(programs, courses)


