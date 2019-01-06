import datetime
import re
import numpy
import math

QUARTER_START_DATE = "2019-01-07"
QUARTER_END_UTC_STR = "20190316T235959Z"
DEFAULT_TIMEZONE = 'America/Los_Angeles'

# Mapping days of the week: Sunday to 1, Monday to 2, ..., Saturday to 7
DAYS_MAP = {
    "WhateverThatIsSunday": 1,  # TODO: replace with string rep of Sunday in Webreg
    "M": 2,
    "Tu": 3,
    "W": 4,
    "Th": 5,
    "F": 6,
    "Sa": 7
}

BYDAYS_MAP = {
    1: "SU",
    2: "MO",
    3: "TU",
    4: "WE",
    5: "TH",
    6: "FR",
    7: "SA"
}

DEFAULT_FREQ = "WEEKLY"


def split_days(days: str) -> [str]:
    """
    Returns a list of strings from seperating days string by capital letters. 

        ref: https://stackoverflow.com/questions/2277352/split-a-string-at-uppercase-letters

        re.findall('[A-Z][^A-Z]*', 'TheLongAndWindingRoad')
        ['The', 'Long', 'And', 'Winding', 'Road']

        re.findall('[A-Z][^A-Z]*', 'ABC')
        ['A', 'B', 'C']

        :param days:str: 
    """
    return re.findall('[A-Z][^A-Z]*', days)


def get_answer():
    """Get an answer."""
    return True


def get_offset(time_str: str) -> datetime.timedelta:
    """ Converts time string to datetime.timedelta (hours to elapse from midnight)  
    ref: https://stackoverflow.com/questions/41308016/python-converting-time-format-1200a-to-24hour
        :param time_str:str: 
    """
    t: datetime = datetime.datetime.strptime(time_str + 'm', '%I:%M%p')
    midnight = datetime.datetime.strptime("12:00a" + 'm', '%I:%M%p')
    offset_midnight: datetime.timedelta = t - midnight
    return offset_midnight


def get_offset_pair(time_str: str) -> (datetime.timedelta, datetime.timedelta):
    """
    Converts time range to a pair of offset from midnight of a day. 
        :param time_str:str: time range, example: "11:30a-2:29p"
    """
    time_many = time_str.split("-")
    start_str: str = time_many[0]
    end_str: str = time_many[1]
    start_offset = get_offset(start_str)
    end_offset = get_offset(end_str)
    return start_offset, end_offset


def get_time_pair(start_offset: datetime.timedelta,
                  end_offset: datetime.timedelta,
                  quarter_start: datetime.datetime) -> (datetime.datetime, datetime.datetime):
    start_time = quarter_start + start_offset
    end_time = quarter_start + end_offset
    return (start_time, end_time)


def get_summary(subject_course: str, row_type: str) -> str:
    """
    Returns summary field for calendar event. 
        :param subject_course:str: 
        :param row_type:str: "LE" for lecture
    """
    return "{} {}".format(subject_course, row_type)


def get_quarter_start(quarter_start_date: str) -> datetime.datetime:
    """
    Returns quarter start day datetime. 
        :param quarter_start_date:str: must be Monday of the quarter instruction start week
    """
    start_day_datetime = datetime.datetime.fromisoformat(quarter_start_date)
    assert start_day_datetime.weekday() == 0
    return start_day_datetime


def get_first_day_of_section(quarter_start_date: str, first_day_num) -> datetime.datetime:
    """
    Returns datetime of first day of section. 
    Known issues: does not support Sunday as first day of meeting
        :param quarter_start_date:str: Monday of the quarter instruction start week 
        :param first_day_num: 1 if Sunday, 2 if Monday, ..., 6 if Sunday
    """
    quarter_start_monday = get_quarter_start(quarter_start_date)
    offset_from_monday = first_day_num - 2  # 0 for Monday
    delta = datetime.timedelta(days=offset_from_monday)
    start_day_datetime = quarter_start_monday + delta
    return start_day_datetime


def get_day_nums(days: str) -> []:
    """ Returns a list of numbers representing days of the week.  
    :param days:str: Days field of WebReg list, example: "MWF"
    """
    day_list = split_days(days)

    def day_to_num(a): return DAYS_MAP[a]  # M -> 2
    day_nums: list = [day_to_num(day) for day in day_list]
    day_nums.sort()
    return day_nums


def get_first_meeting_day_num(days: str):
    """ Returns the number representing the day of first meeting of the week 
    :param days:str: Days field of WebReg list, example: "MWF"
    """
    day_nums = get_day_nums(days)
    first_day_num = day_nums[0]
    return first_day_num


def get_byday(days: str):
    """
    Returns BYDAY field value (MO,WE,FR) for building recurrence string. 
        :param days:str: example: "MWF" for Monday, Wednesday, Friday
    """
    day_nums = get_day_nums(days)

    def num_to_bydays(a): return BYDAYS_MAP[a]  # 2 -> Monday
    bydays = [num_to_bydays(day_num) for day_num in day_nums]
    byday_str = ",".join(bydays)
    return byday_str


def get_location(building: str, room: str) -> str:
    """
    Return location string if building and room are both not "nan". 
        If any of building and room is "nan", None is returned. 
        :param building:str: 
        :param room:str: 
    """
    if building is None or room is None:
        return None
    else:
        return "{} {}".format(building, room)


def get_recurrence(days: str, until: str) -> [str]:
    """
    Returns the recurrence field that specified which days of a week do the section
        occur and until when will the recurrence end 
        https://developers.google.com/calendar/recurringevents

        Sample return: list: ["RRULE:FREQ=WEEKLY;BYDAY=MO,WE,FR;UNTIL=20190316T235959Z"]

        :param days:str: example: "MWF" for Monday, Wednesday, Friday
        :param until:str: example: "20190316T235959Z"
    """
    freq = DEFAULT_FREQ
    byday = get_byday(days)
    return ["RRULE:FREQ={};BYDAY={};UNTIL={}".format(freq, byday, until)]

def get_date_once(days: str) -> datetime.datetime:
    """ Returns datetime of the midnight(12AM) on the date specified in days. 
        :param days:str: WebReg "Days" field example: "F 03/22/2019"
    """
    date_str = days.split().pop() 
    return datetime.datetime.strptime(date_str, "%m/%d/%Y")


def get_time_pair_once(days: str, time: str) -> (datetime.datetime, datetime.datetime):
    """
    Returns a tuple of time range from WebReg Days and Time field. 
        :param days:str: WebReg "Days" field example: "F 03/22/2019"
        :param time:str: WebReg "Time" field example: "11:30a-2:29p"
    """
    start_offset, end_offset = get_offset_pair(time)
    start_day_datetime = get_date_once(days)
    start_time, end_time = get_time_pair(
        start_offset, end_offset, start_day_datetime)
    return start_time, end_time


def generate_section_event(subject_course, row: dict) -> dict:
    """
    Returns recurrent Google Calendar event dict from SubjectCourse and table row of type: 
        * "DI": Discussion
        * "LE": Lecture
        :param subject_course: course name, example: "MATH 171A"
        :param row:dict: table row obtained on WebReg 
    """
    first_meeting_day_num = get_first_meeting_day_num(row["Days"])
    start_day_datetime = get_first_day_of_section(
        QUARTER_START_DATE, first_meeting_day_num)
    start_offset, end_offset = get_offset_pair(row["Time"])
    start_time, end_time = get_time_pair(
        start_offset, end_offset, start_day_datetime)
    location = get_location(row["BLDG"], row["Room"])

    d = {
        "summary": get_summary(subject_course, row["Type"]),
        "start": {
            'dateTime': start_time.isoformat(),
            'timeZone': DEFAULT_TIMEZONE,
        },
        "end": {
            'dateTime': end_time.isoformat(),
            'timeZone': DEFAULT_TIMEZONE,
        },
        "recurrence": get_recurrence(row["Days"], QUARTER_END_UTC_STR)
    }
    if location is not None:
        d["location"] = location 
    return d


def generate_final_exam_event(subject_course, row: dict) -> dict:
    """
    Returns recurrent Google Calendar event dict from SubjectCourse and table row of type: 
        * "FI": Final Exam
        :param subject_course: course name, example: "MATH 171A"
        :param row:dict: table row obtained on WebReg 
    """
    start_time, end_time = get_time_pair_once(row["Days"], row["Time"])
    location = get_location(row["BLDG"], row["Room"])
    d = {
        "summary": get_summary(subject_course, row["Type"]),
        "start": {
            'dateTime': start_time.isoformat(),
            'timeZone': DEFAULT_TIMEZONE,
        },
        "end": {
            'dateTime': end_time.isoformat(),
            'timeZone': DEFAULT_TIMEZONE,
        }
    }
    if location is not None:
        d["location"] = location
    return d


def generate(subject_course, row: dict) -> dict:
    """
    Returns Google Calendar event dict from SubjectCourse and table row. 
        :param subject_course: 
        :param row:dict: 
    """
    row_type = row["Type"]  # examples: FI, DI, LE
    if row_type == "FI":
        return generate_final_exam_event(subject_course, row)
    elif row_type == "DI" or row_type == "LE":
        return generate_section_event(subject_course, row)
    else:
        raise ValueError("Row type: {} not supported. Course: {}, row: {}".format(
            row_type, subject_course, row))
