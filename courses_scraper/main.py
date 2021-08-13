import sys
import requests
import csv
import time
from bs4 import BeautifulSoup

CATALOG_BASE_URL = "https://courses.illinois.edu/cisapp/explorer/catalog"
SCHEDULE_BASE_URL = "https://courses.illinois.edu/cisapp/explorer/schedule"

def crawl(outfile, term, semester):
    with open(outfile, 'w') as outcsv:
        csvwriter = csv.writer(outcsv)
        instrs = []
        for subject in crawl_subjects(term, semester)[3:]:
            for course in crawl_courses(term, semester, subject):
                print('.', end='', flush=True)
                for instr in crawl_instructors(term, semester, subject, course):
                    row = [subject, course, term, semester, instr]
                    instrs.append(row)
                    csvwriter.writerow(row)
                    outcsv.flush()
            print('', flush=True)
        return instrs

# Get the list of subject for the term & semester
def crawl_subjects(term, semester):
    url = f"{CATALOG_BASE_URL}/{term}/{semester}.xml"
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'lxml')
    subject_tags = soup.find_all('subject')
    subjects = [s['id'] for s in subject_tags]
    return subjects

# Get all the course numbers for the subject
def crawl_courses(term, semester, subject):
    url = f"{CATALOG_BASE_URL}/{term}/{semester}/{subject}.xml"
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'lxml')
    course_tags = soup.find_all('course')
    courses = [c['id'] for c in course_tags]
    return courses

# Get all the instructors who teach the course as a set
def crawl_instructors(term, semester, subject, course):
    try:
        url = f"{SCHEDULE_BASE_URL}/{term}/{semester}/{subject}/{course}.xml?mode=detail"
        page = requests.get(url, timeout=5)
        soup = BeautifulSoup(page.text, 'lxml')
        instr_tags = soup.find_all('instructor')
        instrs = [(i['lastname'] + ', ' + i['firstname']) for i in instr_tags]
        return set(instrs)
    except requests.exceptions.ReadTimeout as e:
        print('#', end='', flush=True)
        return set([])

def main(*args):
    print('UIUC courses instructor scraper')

    term = "2021"
    semester = "fall"

    t = int(time.time())
    outfile = f"out_{t}.csv"
    res = crawl(outfile, term, semester)



if __name__ == "__main__":
    main(*sys.argv[1:])
