# -*- coding: utf-8 -*-

from .context import sample
import sample.helpers as helpers
import json
import datetime
import numpy

import webreg_event

import unittest


class TestHelper(unittest.TestCase):

    def test_generate_quarter_start(self):
        result = helpers.get_quarter_start("2019-01-07")
        expected_value = datetime.datetime(2019, 1, 7)

        self.assertEquals(expected_value, result)

    def test_summary(self):
        result = helpers.get_summary("MATH 171A", "LE")
        expected_value = 'MATH 171A LE'

        self.assertEquals(expected_value, result)

    def test_get_offset(self):
        result = helpers.get_offset("1:50p")
        expected_offset = datetime.timedelta(
            hours=13, minutes=50)  # 13 hours 50 minutes

        self.assertEquals(expected_offset, result)

    def test_time_pair(self):
        quarter_start = datetime.datetime(2019, 1, 5)
        start_offset = datetime.timedelta(hours=13)  # 13 hours
        end_offset = datetime.timedelta(
            hours=13, minutes=50)  # 13 hours 50 minutes
        result = helpers.get_time_pair(start_offset, end_offset, quarter_start)
        expected_value = (datetime.datetime(2019, 1, 5, 13, 00),
                          datetime.datetime(2019, 1, 5, 13, 50))
        self.assertTupleEqual(result, expected_value)

    def test_split_days(self):
        result = helpers.split_days("TuTh")
        expected_value = ["Tu", "Th"]

        self.assertListEqual(result, expected_value)

    def test_get_byday(self):
        result = helpers.get_byday("TuTh")
        expected_value = "TU,TH"
        self.assertEquals(result, expected_value)

    def test_get_recurrence(self):
        result = helpers.get_recurrence("MWF", "20190316T235959Z")
        expected_recurrence = [
            "RRULE:FREQ=WEEKLY;BYDAY=MO,WE,FR;UNTIL=20190316T235959Z"]

        self.assertEqual(result, expected_recurrence)

    def test_get_first_day_of_section_monday(self):
        result = helpers.get_first_day_of_section(
            "2019-01-07", 2)  # Monday: 2nd day of week
        expected_value = datetime.datetime(2019, 1, 7)

        self.assertEquals(expected_value, result)

    def test_get_first_day_of_section_tuesday(self):
        result = helpers.get_first_day_of_section(
            "2019-01-07", 3)  # Tuesday: 3rd day of week
        expected_value = datetime.datetime(2019, 1, 8)

        self.assertEquals(expected_value, result)


class TestFinalExamEventHelper(unittest.TestCase):

    def test_get_time_pair(self):
        """
            "Days": "F 03/22/2019",
            "Time": "11:30a-2:29p",
        """
        days = "F 03/22/2019"
        time = "11:30a-2:29p"
        result = helpers.get_time_pair_once(days, time)
        expected_value =  (datetime.datetime(2019, 3, 22, 11, 30),
                          datetime.datetime(2019, 3, 22, 14, 29))
        self.assertEqual(result, expected_value)
        
    def test_get_date_once(self):
        days = "F 03/22/2019"
        result = helpers.get_date_once(days)
        expected_value = datetime.datetime(2019, 3, 22)
        self.assertEqual(result, expected_value)
    
    def test_get_location_none(self):
        """ Tests that get_location returns None if building and room are not published yet. 
        """
        self.assertIsNone(helpers.get_location("APM", None))
        self.assertIsNone(helpers.get_location(None, None))


expected_event = {
    'summary': 'MATH 171A LE',
    # 'location': '800 Howard St., San Francisco, CA 94103',
    'location': "PCYNH 106",
    # 'description': 'A chance to hear more about Google\'s developer products.',
    'start': {
        # Instead of '2018-09-07T13:50:00-07:00'
        # 'America/Los_Angeles' has daylight saving, so we will not use
        #   dateTime with fixed offset
        'dateTime': '2019-01-07T13:00:00',
        'timeZone': 'America/Los_Angeles',
    },
    'end': {
        'dateTime': '2019-01-07T13:50:00',
        'timeZone': 'America/Los_Angeles',
    },
    # MWF
    # Instruction ends: Friday, March 15 (2019)
    # Note that the time is in "Z" (which is "UTC")
    #     we intend the end date to be 11:59pm one day later,
    #     Saturday, March 16 (2019) in UTC Time
    'recurrence': [
        "RRULE:FREQ=WEEKLY;BYDAY=MO,WE,FR;UNTIL=20190316T235959Z"
    ]
}

class TestPasteBoard(unittest.TestCase):

    def test_paste(self):
        result = webreg_event.generate_events_from_pasteboard()
        self.assertIsNotNone(result)


class TestGenerateEvent(unittest.TestCase):
    """
    Tests generating event with a single row. 
    """

    def setUp(self):
        self.maxDiff = None
        JSON_FILENAME = 'math171a.json'
        with open('tests/jsons/{}'.format(JSON_FILENAME)) as json_file:
            d = json.load(json_file)
            self.subject_course = d["subjectCourse"]
            self.rows = d["rows"]

    def test_lecture_event(self):
        result = helpers.generate_section_event(self.subject_course, self.rows[0])
        self.assertDictEqual(result, expected_event)

    def test_discussion_event(self):
        row = self.rows[1]
        print(row)
        result = helpers.generate_section_event(self.subject_course, row)
        expected_section_event = {
            'summary': 'MATH 171A DI',
            # 'location': '800 Howard St., San Francisco, CA 94103',
            'location': "APM 2402",
            # 'description': 'A chance to hear more about Google\'s developer products.',
            'start': {
                # Instead of '2018-09-07T13:50:00-07:00'
                # 'America/Los_Angeles' has daylight saving, so we will not use
                #   dateTime with fixed offset
                'dateTime': '2019-01-10T21:00:00',
                'timeZone': 'America/Los_Angeles',
            },
            'end': {
                'dateTime': '2019-01-10T21:50:00',
                'timeZone': 'America/Los_Angeles',
            },
            'recurrence': [
                # MWF
                # Instruction ends: Friday, March 15 (2019)
                # Note that the time is in "Z" (which is "UTC")
                #   we intend the end date to be 11:59pm one day later,
                #   Saturday, March 16 (2019) in UTC Time
                "RRULE:FREQ=WEEKLY;BYDAY=TH;UNTIL=20190316T235959Z"
            ]
        }

        self.assertDictEqual(result, expected_section_event)

    def test_final_exam_event(self):
        """
        MATH 171A: 
            "SubjectCourse": NaN,
            "Title": "Final Exam",
            "SectionCode": NaN,
            "Type": "FI",
            "Instructor": NaN,
            "GradeOption": NaN,
            "Units": NaN,
            "Days": "F 03/22/2019",
            "Time": "11:30a-2:29p",
            "BLDG": "TBA",
            "Room": "TBA",
            "Status": NaN,
            "Action": NaN
        """
        row = self.rows[2]
        result = helpers.generate(self.subject_course, row)

        expected_final_exam_event = {
            'summary': 'MATH 171A FI',
            # 'location': '800 Howard St., San Francisco, CA 94103',
            # There should be no location 
            # 'description': 'A chance to hear more about Google\'s developer products.',
            'start': {
                'dateTime': '2019-03-22T11:30:00',
                'timeZone': 'America/Los_Angeles',
            },
            'end': {
                'dateTime': '2019-03-22T14:29:00',
                'timeZone': 'America/Los_Angeles',
            }
        }


if __name__ == '__main__':
    unittest.main()
