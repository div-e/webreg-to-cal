from richxerox import *
import pandas
from pandas import DataFrame
import warnings
from sample import helpers

import json

SECTION_TYPE_SUPPORTED = ["LE", "DI"]
WEBREG_LABELS = ["SubjectCourse", "Title","SectionCode","Type","Instructor","GradeOption","Units","Days","Time","BLDG","Room","Status","Action"]

def get_table(htmlPasteContent, column_names):
    tableMany = pandas.read_html(htmlPasteContent, 
        skiprows=1, # Expect row 0 to have only nan 
        attrs={"id":"list-id-table"} # Locate the table 
        )
    # print(tableMany)
    # print("ssssssss")
    table: DataFrame = tableMany[0]
    table.set_axis(column_names, axis=1, inplace=True)
    return table

def get_courses(table: DataFrame):
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
            currentCourse = list()
            courses[courseName] = currentCourse
        currentCourse.append(row)

        # Increment row counter
        currentIndex += 1
    return courses


def get_events(courses: dict):
    events = list()
    for subject_course, rows in courses.items():
        for row in rows:
            if row["Type"] not in SECTION_TYPE_SUPPORTED:
                warnings.warn("Unsupported section type. Skipping row: {}".format(row) )
                continue
            e = helpers.generate_event(subject_course, row)
            events.append(e)
    return events

def generate_events_from_pasteboard() -> []:

    htmlPasteContent = paste(format='html')
    table = get_table(htmlPasteContent, WEBREG_LABELS)
    courses = get_courses(table)
    events = get_events(courses)

    return events
