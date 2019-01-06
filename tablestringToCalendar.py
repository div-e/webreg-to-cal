from richxerox import *
import pandas
from pandas import DataFrame
import warnings

import json

# import pdfquery
# from lxml import etree
# from tabula import read_pdf


def validateNonCourseName(subjectCourseString):
    s = str(subjectCourseString)
    # Note that this detects only "some" case not all cases
    return (len(s.split(" ")) != 2)


# pdf = pdfquery.PDFQuery("/Users/billyrao/Developer/webregToCalendar/Schedule_webregMain.pdf")
# pdf.load()
# # pdf.tree.write("test2.xml", pretty_print=True, encoding="utf-8")
# e = pdf.extract([
#     ('with_formatter', 'text'),
#     # ('with_parent', 'LTTextVertical'),
#     ('Days','LTTextBoxHorizontal')
# ])
# print(e["Days"])
#
# df = read_pdf("/Users/billyrao/Developer/webregToCalendar/Schedule_webregMain.pdf", stream=True,
#               #   output_format="json",
#               #   pandas_options={'columns': ['Subject Course', 'Title', 'Section Code', 'Type',
#               #                               'Instructor', 'Grade Option', 'Units', 'Days', 'Time',
#               #                               'BLDG', 'Room', 'Status / (Position)', 'Action']}
#
#               )
# df.columns = ['Subject Course', 'FOOBAR', 'Title', 'Section Code', 'Type',
#               'Instructor', 'Grade Option', 'Units', 'Days', 'Time',
#               'BLDG', 'Room', 'Status / (Position)']
# print(df)

htmlPasteContent = paste(format='html')
column_names = ["SubjectCourse", "Title","SectionCode","Type","Instructor","GradeOption","Units","Days","Time","BLDG","Room","Status","Action"]

tableMany = pandas.read_html(htmlPasteContent, 
    skiprows=1, # Expect row 0 to have only nan 
    attrs={"id":"list-id-table"} # Locate the table 
    )
# print(tableMany)
# print("ssssssss")
table: DataFrame = tableMany[0]
table.set_axis(column_names, axis=1, inplace=True)
print(table)

maxRowIndex = len(table) - 1
print(maxRowIndex)
currentIndex = 0
currentCourse = None
courses = dict()
while(currentIndex <= maxRowIndex):
    s: pandas.Series = table.iloc[currentIndex]
    row = s.to_dict()
    if str(row["SubjectCourse"]) != "nan":  # To be checked
        # Create new currentCourse and save courseName, object pointer pair
        courseName = row["SubjectCourse"]
        print(courseName)
        currentCourse = list()
        courses[courseName] = currentCourse
    # else:
    #     # Double check that currentCourse represents empty value
    #     if not validateNonCourseName(row["Subject Course"]):
    #         warnings.warn(
    #             message="The string: {} parsed as courseName might not be a course name"
    #                 .format(row["Subject Course"]))
    currentCourse.append(row)

    # Increment row counter
    currentIndex += 1

# print(courses)

def parse_course(subject_course, rows): 
    raise NotImplementedError

for subject_course, rows in courses.items():
    d = {
        "subjectCourse": subject_course, 
        "rows": rows
    }
    print(json.dumps(d))
    
    # parse_course(subject_course, rows)

# for courseName, courseComponent in table:
#     print(courseName)
# if row["Subject Course"] != nan:
