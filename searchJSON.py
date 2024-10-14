from ast import excepthandler
import json
import csv

# open/load in the JSON file:
data = open('courseData.json')
final = json.load(data)

#allow user to input a term they want to search for:
query = input("What term are you searching for? ")

#for loop to find 1) the faculty name, 2) the html code that the query variable is located
# and 3) print out the corresponding index location from html_body to page_url

for employee in final:
    f = open("finalresults.csv", "a")
    facultyName = str(employee["instructor"])
    courseName = employee["course_Name"]
    assignment_Name = employee["assignment_body"]
    assignment_URL = employee["assignment_url"]
        
    # print(facultyName + ": " + courseName)

    results = []
    try: 

########original, working code#######
        for index, b in enumerate(employee["body"]):
            if query in b:
                # print(index) this just to search the index for debugging and testing
                result = employee["page_url"][index]

                # results.append(result)
                print(result)
                f.write('\n'+facultyName+",")
                f.write(courseName) 
                f.write(","+result)

#### code works to search ASSIGNMENT body and URL
        for index, ab in enumerate(employee["assignment_body"]):
            if query in ab:
                #this just to search the index for debugging and testing
                # print(index) 
                aresult = employee["assignment_url"][index]
                results.append(aresult)
                print(aresult)
                f.write('\n'+facultyName+",")
                f.write(courseName+",") 
                f.write("," + aresult)
          
    except TypeError:
        print("null found")
    f.close()

#search for term:    
# iframeembed=true
