# -*- coding: utf-8 -*-

from .context import sample
from sample.helpers import parse_course
import json

import unittest


class BasicTestSuite(unittest.TestCase):
    """Basic test cases."""

    def test_absolute_truth_and_meaning(self):
        assert True


expected_event = {
    'summary': 'MATH 171A LE',
    # 'location': '800 Howard St., San Francisco, CA 94103',
    # 'location': "PCYNH 106",
    # 'description': 'A chance to hear more about Google\'s developer products.',
    'start': {
        # Instead of '2018-09-07T13:50:00-07:00'
        # 'America/Los_Angeles' has daylight saving, so we will not use
        #   dateTime with fixed offset
        'dateTime': '2018-09-07T13:00:00',
        'timeZone': 'America/Los_Angeles',
    },
    'end': {
        'dateTime': '2018-09-07T13:50:00',
        'timeZone': 'America/Los_Angeles',
    },
    'recurrence': [
        # MWF
        # Instruction ends: Friday, March 15 (2019)
        # Note that the time is in "Z" (which is "UTC")
        #   we intend the end date to be 11:59pm one day later,
        #   Saturday, March 16 (2019) in UTC Time
        "RRULE:FREQ=WEEKLY;BYDAY=MO,WE,FR;UNTIL=20190316T235959Z"
    ]
}


class TestParseCourse(unittest.TestCase):
    """
    Tests parse_course helper function
    """

    def setUp(self):
        JSON_FILENAME = 'math171a.json'
        with open('tests/jsons/{}'.format(JSON_FILENAME)) as json_file:
            d = json.load(json_file)
            self.subject_course = d["subjectCourse"]
            self.rows = d["rows"]

    def test_parse(self):
        parse_course(self.subject_course, self.rows)
        self.fail()
        # result =
        # self.assertEquals(result, None)


class TestGenerateEvent(unittest.TestCase):

    def test_event(self):
        pass


if __name__ == '__main__':
    unittest.main()
