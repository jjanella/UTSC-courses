from bs4 import BeautifulSoup
import requests
import re
from enum import Enum

class Course:
    name: str
    code: str
    desc: str
    url: str
    sameas: list = []
    exclusions: list = []
    breadth: str
    prereqs: list = []
    def __init__(self, code: str, courses: list):
        scrape_course(self, code, courses)
        

class Program:
    name: str
    code: str
    coop: bool = False
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
        program.coop == True
        title.pop(0)
    
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
    


            # title = title.replace("&amp;", "&")
            # title = title.split(" - ")
            # prog.name = title[0]
            # prog.level = title[-1]
            # if len(title) == 3:
            #     prog.stream = title[1]

            # if prog.level[:-5] == "Co-op":
            #     prog.coop = True

    soup = soup.find_all("a", href=re.compile("/course/"))

    for i in range(len(soup)):
        soup[i] = str(soup[i])
        code = soup[i][soup[i].find("/course/") + 8: soup[i].find("\">") - 2]


        add = True
        for course in courses:
            if (course.code == code):
                add = False
                program.courses.append(course)
                print("Already found " + code)
                break
        
        if add:
            try:
                course = Course(code, courses)
                program.courses.append(course)
                courses.append(course)
            except:
                print("Error Scraping " + code + ", Probably no longer exists")



def scrape_course(course: Course, code: str, courses: list[Course]):


    course.code = code
    course.url = "https://utsc.calendar.utoronto.ca/course/" + code + "H3"



    site = requests.get(course.url)
    soup = BeautifulSoup(site.content, 'html.parser')

    title = str(soup.find_all("h1", class_="page-title"))
    course.name = title[title.find(":" ) + 1: title.find("</")]
    if "Sorry" in title:
        raise()
    print("Found Course " + course.code + " " + course.name)


    prereqs = soup.find_all('div', class_="w3-row field field--name-field-prerequisite field--type-text-long field--label-inline clearfix")

    for prereq in prereqs:
        if "Prerequisite</label>" in str(prereq):
            # print(str(relation))
            # print(str(relation))

            reqs = str(prereq.find_all('div', class_=['w3-bar-item field__item']))

            while reqs.find("<") != -1:
                start = reqs.index("<")
                end = reqs.index(">")
                reqs = reqs[0:start] + reqs[end+1:]
            
            reqs = reqs.removesuffix(" and [CGPA 3.5 or enrolment in a CSC Subject POSt]")

            reqs = reqs.replace("or", "and")
            reqs = reqs.replace("[", "")
            reqs = reqs.replace("]", "")
            reqs = reqs.replace("H3", "")
            reqs = reqs.split(" and ")
            for i in range(len(reqs) - 1, -1, -1):
                if len(reqs[i]) != 6 or reqs[i].find("(") != -1:
                    reqs.pop(i)
            
            add = True
            for req in reqs:
                for course in courses:
                    if course.code == req:
                        add = False
                        break
                if add:
                    course.prereqs.append(Course(req, courses))

    exclusions = soup.find_all("div", class_="w3-row field field--name-field-exclusion field--type-text-long field--label-inline clearfix")

    for exclusion in exclusions:
        if "Exclusion" in str(exclusion):
            print(str(exclusion))

            exls = str(exclusion.find_all('div', class_=['w3-bar-item field__item']))

            while exls.find("<") != -1:
                start = exls.index("<")
                end = exls.index(">")
                exls = exls[0:start] + exls[end+1:]



if __name__ == "__main__":
    # print(Course("BIOA11", []).prereqs)
    programs: list[Program] = []
    courses: list[Course] = []
    scrape_programs(programs, courses)


