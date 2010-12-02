from parser.models import Section, DAY_MAPPER

from solver import Problem

INVERSE_DAY_MAPPER = {}
for k,v in DAY_MAPPER.iteritems():
    INVERSE_DAY_MAPPER[v.lower()] = k
    
def convert_days(days):
    "Returns integer for of the tuple of days."
    int_days = []
    mind, maxd = min(INVERSE_DAY_MAPPER.values()), max(INVERSE_DAY_MAPPER.values())
    for day in days:
        if type(day) in (int, long):
            if mind <= day <= maxd:
                int_days.append(day)
            else:
                raise TypeError, "Day of week int is not in range %r, %r" % (
                    mind, maxd
                )
            continue
        if day.lower() not in INVERSE_DAY_MAPPER:
            raise TypeError, "Unknown day of week: %r" % day
        int_days.append(INVERSE_DAY_MAPPER[day.lower()])
    return int_days

class TimeRange(object):
    "Represents a time range to be restricted."
    def __init__(self, start, end, days=()):
        self.start = start
        self.end = end
        self.days = days
        self.int_days = convert_days(days)
        
    def __repr__(self):
        return "<TimeRange: %r to %r on %r>" % (
            self.start, self.end, self.int_days
        )
    
    def __contains__(self, days_start_stop_tuple):
        days, start, end = days_start_stop_tuple
        
        days = convert_days(days)
        
        same_day = False
        for day in days:
            if day in self.int_days:
                same_day = True
                break
        if not same_day:
            return False
        
        return self.start <= start <= self.end or \
            start <= self.start <= end or \
            self.start <= end <= self.end or \
            start <= self.end <= end
                
    def conflicts_with(self, section):
        "Returns True if the given section conflicts with this time range."
        for p in section.periods:
            t = (p.int_days, p.start, p.end)
            if t in self:
                return True
        return False
    
def course_constraint(section1, section2):
    "Returns True if the two sections are acceptable."
    return not section1.conflicts_with(section2)

def compute_schedules(courses, excluded_times=()):
    """
    Returns all possible schedules for the given courses.
    """
    p = Problem()
    for course in courses:
        p.addVariable(course, course.sections)
    
    for course1 in courses:
        for course2 in courses:
            if course1 == course2:
                continue
            p.addConstraint(course_constraint, [course1, course2])
        for time_range in excluded_times:
            p.addConstraint(lambda x: not time_range.conflicts_with(x), [course1])
    
    return p.getSolutions()
