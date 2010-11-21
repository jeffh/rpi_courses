from ..parser import CourseCatalog
import os
import unittest
from time import mktime
from constants import XML_FILE

with open(XML_FILE) as f:
    CONTENTS = f.read()

# TODO: use a smaller XML file instead of the one from the RPI site
# we can get away with this because the catalog never mutates
catalog = CourseCatalog.from_xml_str(CONTENTS)

class TestCatalog(unittest.TestCase):
    # TOO SLOW:
    #def setUp(self):
    #    self.c = CourseCatalog(CONTENTS)
    
    def test_get_timestamp(self):
        expected_timestamp = 1290023154
        timestamp = int(mktime(catalog.datetime.timetuple()))
        
        self.assertEquals(timestamp, expected_timestamp)
    
    def test_get_year(self):
        self.assertEquals(catalog.year, 2011)
        
    def test_get_semester(self):
        self.assertEquals(catalog.semester, 'Spring')
        
    def test_get_crosslisting_count(self):
        self.assertEquals(len(catalog.crosslistings), 266)
        
    def test_crosslisting(self):
        crns = catalog.crosslisted_with(75537)
        self.assertEquals(crns, (75603,))
        
    def test_get_course_by_name_count(self):
        self.assertEquals(len(catalog.courses_by_name), 700)
        
    def test_get_course_by_code_count(self):
        self.assertEquals(len(catalog.courses_by_code), 871)
        
    def test_get_courses_count(self):
        self.assertEquals(len(catalog.courses), 880)
        
    def test_get_ta_training_seminar(self):
        course = catalog.courses_by_name['TA TRAINING SEMINAR']
        self.assertEquals(course.name, 'TA TRAINING SEMINAR')
        self.assertEquals(course.dept, 'ADMN')
        self.assertEquals(course.num, 6800)
        self.assertEquals(course.credits, 0)
        self.assertTrue(course.is_pass_or_fail)
        
        self.assertEquals(len(course.sections), 1)
        
        section = course.sections[0]
        self.assertEquals(section.crn, 76285)
        self.assertEquals(section.num, 1)
        self.assertEquals(section.seats_taken, 0)
        self.assertEquals(section.seats_total, 200)
        
        self.assertEquals(len(section.periods), 1)
        self.assertEquals(len(section.notes), 2)
        
        period = section.periods[0]
        self.assertTrue(period.is_lecture)
        self.assertFalse(period.is_testing_period)
        self.assertTrue(period.tba)
        self.assertEquals(period.days, ())
        
        notes = section.notes
        self.assertEquals(notes[0], 'REQUIRED FOR ALL NEW OR CURRENT STUDENTS WHO WILL TA')
        self.assertEquals(notes[1], 'MEETING ON THUR, 1/20 IN PM AND ALL DAY 1/21')
        
    def test_get_intro_to_hci(self):
        course = catalog.courses_by_name['INTRODUCTION TO HCI']
        self.assertEquals(course.name, 'INTRODUCTION TO HCI')
        self.assertEquals(course.dept, 'ITWS')
        self.assertEquals(course.num, 2210)
        self.assertEquals(course.credits, 4)
        self.assertFalse(course.is_pass_or_fail)
        
        self.assertEquals(len(course.sections), 1)
        
        section = course.sections[0]
        self.assertEquals(section.crn, 76041)
        self.assertEquals(section.num, 1)
        self.assertEquals(section.seats_taken, 26)
        self.assertEquals(section.seats_total, 40)
        
        self.assertEquals(len(section.periods), 1)
        self.assertEquals(len(section.notes), 1)
        
        period = section.periods[0]
        self.assertEquals(period.instructor, 'Grice')
        self.assertEquals(period.start, 1200)
        self.assertEquals(period.end, 1350)
        self.assertEquals(period.location, "LALLY 102")
        self.assertTrue(period.is_lecture)
        self.assertFalse(period.is_testing_period)
        self.assertFalse(period.tba)
        self.assertEquals(period.days, ('Monday', 'Thursday'))
        
        notes = section.notes
        self.assertEquals(notes[0], 'RESTRICTED TO COMM, ITWS & EMAC MAJORS')


if __name__ == '__main__':
    unittest.main()