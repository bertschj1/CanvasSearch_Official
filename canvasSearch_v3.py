import json
import time
from canvasapi import Canvas
import MyToken

# secret token and course ID
# secret token is called by a separate file (MyToken.py)
# Canvas API key

API_URL = "https://uc.instructure.com"
API_KEY = MyToken.secret

# Initialize a new Canvas object
canvas = Canvas(API_URL, API_KEY)

###### Code that begins Canvas provisioning report

# Code to flush courses.txt and courseData.json files to start fresh
file = open("courses.txt",'w') 
file.close()
file = open("courseData.json",'w') 
file.close()

# Prints college sub accounts
subAccount = [
    "CCM = 16748",
    "CECH = 16751",
    "CEAS = 16752",
    "Social Work = 16759",
    "CoB = 16757",
    "DAAP = 16750",
    "Law = 16763",
    "Pharm = 16755",
    "CoM = 16753",
    "UCBA = 16760",
    "A&S = 16758",
    "CoN = 16754",
    "Clermont = 16747",
    "Allied Health = 16749",
    "ELCE = 16756"
    ]
for school in subAccount:
    print(school)

# establishes subaccount code
collegeCode = input("Enter the numerical subaccount code (from above) you want to pull: ")
account = canvas.get_account(collegeCode)
print()
print("You selected: " + str(account))
print()


# prints out term IDs
tID = canvas.get_account(1939)
term = tID.get_enrollment_terms()
for id in term:
    print(id)

# establishes term ID code
termCode = input("Enter the term code you want to search: ")
courses = account.get_courses(enrollment_term_id=termCode)

for course in courses:
    print(course.id) 
    f = open("courses.txt", "a")
    f.write(str(course.id)+'\n')

###### End provisioning report code

# Start timer for code to run :)
t = time.localtime()
current_time = time.strftime("%H:%M:%S", t)
print("\nYour program began at: " + current_time)
start = time.time()

# Opens courses.txt with all courseIDs, and creates the report file (courseData.json)
DataFile = open("./courses.txt","r")

###### Code to start reading from courses.txt file
course_id = DataFile.read().split()

###### Code that begins Canvas scraping
for c in course_id:
    print(c)
    
    htmlUrlVariable = []
    bodyVariable = []
    assigmentVariable = []
    assignmentURL = []
    instructorVariable = []

    ###### Code to Get course name:
    course = canvas.get_course(c)
    coursename = course.name
    courseId = course.course_code
    courseNameVariable = coursename+" : "+courseId

    ###### Code to Get course pages URL and HTML Body
    coursePage = course.get_pages()
    for page in coursePage:
        page_url = page.url
        page_body = course.get_page(page_url)
        htmlUrlVariable.append(page.html_url)
        bodyVariable.append(page_body.body)

    ###### Code to find course instructor with id role of 'teacher'
    course = canvas.get_course(c)
    instructor = course.get_users(enrollment_type=['teacher'])
    for teachers in instructor:
        instructorVariable.append(str(teachers))

    ###### Code to find Assignment URL and HTML Body
    coursePage = course.get_assignments()
    for AP in coursePage:
        assigment_body = AP.description
        assignment_url = AP.html_url
        assigmentVariable.append(assigment_body)
        assignmentURL.append(assignment_url)

    ###### Code that creates the JSON object
    canvasData = {
        'instructor': instructorVariable,
        'course_Name': courseNameVariable,
        'page_url': htmlUrlVariable,
        'body' : bodyVariable,
        'assignment_body' : assigmentVariable,
        'assignment_url' : assignmentURL
    }

    ###### Code to create the JSON file
    json_object = json.dumps(canvasData, indent=4)
    with open("./courseData.json", "a") as outfile:
        outfile.write(json_object + ",")

print(">>>>Process complete! It took", time.time()-start, "seconds to complete.\n")