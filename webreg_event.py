from richxerox import paste
import pandas
from pandas import DataFrame
import warnings
from sample import helpers
from sample.helpers import SECTION_TYPE_SUPPORTED

import json

WEBREG_LABELS = ["SubjectCourse", "Title", "SectionCode", "Type", "Instructor",
                 "GradeOption", "Units", "Days", "Time", "BLDG", "Room", "Status", "Action"]


def get_table(htmlPasteContent, column_names):
    tableMany = pandas.read_html(htmlPasteContent,
                                 skiprows=1,  # Expect row 0 to have only nan
                                 # Locate the table
                                 attrs={"id": "list-id-table"}
                                 )
    table: DataFrame = tableMany[0]
    table.set_axis(column_names, axis=1, inplace=True)
    table_none = table.where(pandas.notnull(table), None)
    return table_none


def get_courses(table: DataFrame):
    maxRowIndex = len(table) - 1
    currentIndex = 0
    currentCourse = None
    courses = dict()
    while(currentIndex <= maxRowIndex):
        s: pandas.Series = table.iloc[currentIndex]
        row = s.to_dict()
        # print(json.dumps(row)) # To generate test data
        if row["SubjectCourse"] is not None:  # To be checked
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
                warnings.warn("Unsupported section type: {} for course: {}. Skipping row: {}".format(
                    row["Type"], subject_course, row))
                continue
            e = helpers.generate(subject_course, row)
            events.append(e)
    return events


def generate_events_from_pasteboard() -> []:

    htmlPasteContent = paste(format='html')
    table = get_table(htmlPasteContent, WEBREG_LABELS)
    courses = get_courses(table)
    events = get_events(courses)

    return events
