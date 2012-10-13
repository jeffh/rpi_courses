Overview
========

``rpi_courses`` is a simple Python_ library for reading and using RPI_'s
course schedule. This has been extracted from YACS_.

It can parse the `XML files`_ provided on RPI's SIS system and provides a
primitive object-oriented API layer to access the course information.

Also, it provides rudimentary method to computing schedules using constraints.

.. _Python: http://python.org/
.. _RPI: http://rpi.edu/
.. _XML files: http://sis.rpi.edu/reg/rocs/
.. _YACS: https://github.com/jeffh/YACS

Usage
-----

To install::

    pip install RPICourses

Then you can import it to your python scripts::

    from rpi_courses import CourseCatalog, list_sis_files

``list_sis_files`` accepts an optional URL argument, the default url is
assumed to be "http://sis.rpi.edu/reg/". This function expects to
read an apache-style file listing page. It scrapes all the files listed
there that end with a xml file extension and returns the full URLs to those
files::

    >>> files = list_sis_files()
    >>> files
    [u'http://sis.rpi.edu/reg/rocs/201001.xml',
     u'http://sis.rpi.edu/reg/rocs/201005.xml',
     u'http://sis.rpi.edu/reg/rocs/201009.xml',
     u'http://sis.rpi.edu/reg/rocs/201101.xml']


``CourseCatalog`` is the class that parses and stores all the course info.

The constructor accepts a BeautifulSoup_ or BeautifulStoneSoup_ instance. You
really should use the Stone variant.

But you don't even need to touch that at all! Just use the static methods::

  >>> c = CourseCatalog.from_url(files[-1])
  # wait a bit... and then you own the data, muhahaha!

There's also ``CourseCatalog.from_stream`` to read from an file-handle-like
stream; ``CourseCatalog.from_file`` to read from a given file path; and
finally ``CourseCatalog.from_xml_str`` to read from a string.

Each one of the static methods will instantiate a BeautifulStoneSoup instance
behind the curtains an.

Now there are the following properties to access after parsing:

- ``timestamp`` is the raw timestamp (int) when the xml file was last updated.
- ``datetime`` is the python Datetime_ object of the raw timestamp.
- ``year`` the year the xml course catalog refers to.
- ``month`` the starting month of the semester the course catalog refers to.
- ``semester`` the english representation of the semester this catalog refers to.
- ``name`` the SEMESTER and YEAR as a string.
- ``crosslistings`` a dict mapping a CRN to it's associated CRNs. Related CRNs
            refer to similar classes (ie - same class in different dept).
- ``courses`` a dict mapping a string of (name, dept, code) to a Course object.

With the most important being the Course object with contains:

- ``name`` the name of the course.
- ``dept`` the department code that provides this course.
- ``num`` the course number the department provides. (e.g. dept + num = "PHYS 2100")
- ``cred`` the credit range the course provides.
- ``sections`` a collection of sections this course has.
- ``available_sections`` a collection of sections that are still availble (has seats).
 
There is also a ``grade_type`` property, which seems unused. For sections have the following
properties:

- ``crn`` the CRN this section refers to.
- ``seats_taken`` the number of seats already taken.
- ``seats_total`` the number of seats total for this section..
- ``num`` the section number.
- ``periods`` the time periods this section meets.
- ``notes`` a tuple of notes about the section.
 
Finally, the periods are instanced that have the following properties:

- ``type`` the type of session.
- ``instructor`` the instructor that teaches/oversees this period
- ``start`` the starting time of the period. Times are in military integer format (e.g. - 2100)
- ``end`` the ending time of the period. Times are in miliary integer format (e.g. - 2100)
- ``location`` the location of the period.
- ``int_days`` the collection of days (as integers) which the period meets. 0 is Monday.
 
But there are also additional computed properties which aid in analysis of a period:

- ``time_range`` returns a tuple of (start, end) properties
- ``tba`` returns True if the course's time range is not yet specified (To Be Announced)
- ``is_lecture`` returns True if the period is a lecture time slot.
- ``is_studio`` returns True if the period is a studio time slot.
- ``is_lab`` returns True if the period is a lab time slot.
- ``is_testing_period`` returns True if the period is test-taking time slot.
- ``is_recitation`` returns True if the period is a recitation time slot.
- ``days`` returns a tuple of english-friendly names of int_days.
 
Each object has a ``conflicts_with`` method to determine of another like object has a time
conflict.

.. _BeautifulSoup: http://www.crummy.com/software/BeautifulSoup/documentation.html#Parsing HTML
.. _BeautifulStoneSoup: http://www.crummy.com/software/BeautifulSoup/documentation.html#Parsing XML
.. _Datetime: http://docs.python.org/library/datetime.html

Scheduler
---------

Besides just fetching courses, you can also generate schedules::

    from rpi_schedule import compute_schedules
    # get selected courses
    
    # returns a collection of dictionaries whose keys=courses and values=sections
    compute_schedules(courses)
    
Alternatively, a you can restrict the time ranges available to compute by passing in
an iterable of TimeRange objects as the second argument::

    from rpi_schedule import compute_schedules, TimeRange
    
    # ensure the schedule has 12pm - 2pm open.
    compute_schedules(courses, (TimeRange(start=1200, end=1400, days=(0,1)),))

Underneath the hood, ``compute_schedule`` is a simple wrapper to the Scheduler object::

    def compute_schedules(courses, excluded_times=(), free_sections_only=True, problem=None, return_generator=False):
        s = Scheduler(free_sections_only, problem)
        s.exclude_times(*tuple(excluded_times))
        return s.find_schedules(courses, return_generator)


TODOs
=====

Major/Minor Requirements
------------------------

If possible, provide some way to access the course requirements for every major. This would
require a massive undertaking.

Solver Optimizations
--------------------

The current course solver is a naive implementation. Optimize it by providing more
detailed constraints and apply better solver algorithms.

The solver library has been moved to a `separate library`_.

.. separate library: http://github.com/jeffh/pyconstraints

Notes Analysis
--------------

There are a lot of data that can be extracted from the section.notes attribute that
could be placed into their own properties for easier & abstracted access.

Ideally, the notes that are properly analyzed should be removed from the notes property.

Prerequisites and Co-requisites
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Automatically detect & lookup course prereqs, which are detailed in section NOTES::

    <NOTE>PRE-REQ: PHYS 23330 &amp; MATH 4600</NOTE>
	<NOTE>PRE-REQ: PHYS 1100 OR 1150 AND PHYS 1200 OR 1250</NOTE>
	<NOTE>PRE-REQ: PHYS 2110 OR PHYS 2510, AND MATH 2010 AND MATH 2400</NOTE>
	<NOTE>PRE-REQ: STSS 2300 OR PERMISSION OF INSTRUCTOR</NOTE>
	<NOTE>PRE-REQ: PHYS 2330 AND MATH 4600</NOTE>
	<NOTE>PRE-REQ: BIOL 4620 AND BIOL 4760 OR CHEM 4760 OR BCBP 4760</NOTE>
	<NOTE>PRE-REQ: CSCI 2300</NOTE>
    <NOTE>PRE-REQ; INTRODUCTORY COMM OR SOCIAL SCIENCE COURSE</NOTE>
	<NOTE>PRE-REQ: ENGR 2250 &amp; ENGR 2530 &amp; CIVL 2670</NOTE>
	<NOTE>PRE-REQ: ANY FILM COURSE OR PERMISION OF INSTRUCTOR</NOTE>
	<NOTE>PRE-REQ:  MANE 4480</NOTE>
  
This text needs to be parsed, but relaxed enough to gloss over inconsistencies of the
text provided. The API should provide properties in section and course objects to see
course prereqs, the course object needs to filter out duplicates that the collective
sections would provide.

Prereqs can span multiple lines::

    <NOTE>PRE-REQ: PHYS 1100 OR 1150 AND PHYS 1200 OR 1250</NOTE> 
    <NOTE>AND CSCI 1100</NOTE>

Co-requisites are similar to prereqs::

    <NOTE>CO-REQ: MANE-4010</NOTE>
  
There are a few prereqs that is different::  

	<NOTE>ANY 1000/2000 LEVEL WRITING COURSE</NOTE>
	<NOTE>PRE-REQ: ANY WRIT COURSE</NOTE>
    <NOTE>PRE-REQ: ONE WRIT OR COMM COURSE</NOTE><NOTE>OR ONE COMM INTENSIVE COURSE</NOTE>

"Meets with" Courses
~~~~~~~~~~~~~~~~~~~~~~

Automatically detect and lookup when a course/section meets with X course::

    <NOTE>MEETS WITH PHIL 2961 / COGS 2960</NOTE>
	<NOTE>MEETS WITH ERTH 4690/ ENVE 4110</NOTE>
    <NOTE>MEETS WITH PSYC 4967</NOTE>
    <NOTE>MEETS WITH COGS 4960 &amp; CSCI 4969</NOTE>
	<NOTE>MEETS WITH ARTS 4010 &amp; ITWS 4961</NOTE>
	<NOTE>MEETS WITH BIOL 4710/01</NOTE>
	<NOTE>MEETS WITH BIOL 4770, CHEM 4770</NOTE>
	<NOTE>MEETS WITH BCBP 4640 &amp; BIOL 4640/6640</NOTE>
	<NOTE>MEETS WITH MANE 4750/6830</NOTE>
	<NOTE>MEETS WITH CSCI 6960, ITWS 4962/6961, ERTH 4963/6963</NOTE>
	<NOTE>MEETS WITHENGR 4100, ITWS 4300/6300</NOTE>
  
The good part is that this format is pretty consistent, but harder to parse out the
specific course(s). Since more than one course can be listed, the API should support
more than one course. A section number may be provided to the other course it meets with.

Fulfills requirements
~~~~~~~~~~~~~~~~~~~~~~~

Certain courses/sections are noted to fulfill a given requirement::

    <NOTE>COMMUNICATION INTENSIVE</NOTE>
	<NOTE>FULFILLS COMM INTENSIVE REQUIREMENT</NOTE>
	<NOTE>COMM INTENSIVE</NOTE>
	<NOTE>FULFILLS EMAC THESIS</NOTE>
	<NOTE>FULFILLS EMAC THESIS REQUIREMENT</NOTE>
  
This is simple to check, as all are marked identically. There may
be an edge case where some (but not all) sections contain this note -- then is
a course communication intensive?

Course Restrictions
~~~~~~~~~~~~~~~~~~~

Some courses are restricted by majors or other requirements::

    <NOTE>RESTRICTED TO ARCH MAJORS</NOTE>
	<NOTE>OPEN TO ALL MAJORS EXCEPT ARCH</NOTE>
	<NOTE>RESTRICTED TO EART, EMAC, GSAS MAJORS, OTHERS 12/13</NOTE>
	<NOTE>RESTRICTED TO EMAC, COMM, COMM-IT MAJORS</NOTE>
	<NOTE>RESTRICTED TO SENIOR CHME MAJORS</NOTE>
	<NOTE>RESTRICTED TO HCIN,TCOM, CMRT, ITWS MAJORS</NOTE>
	<NOTE>RESTRICTED TO IT MAJORS</NOTE>
	<NOTE>RESTRICTED TO COMM, ITWS &amp; EMAC MAJORS</NOTE>
	<NOTE>RESTRICTED TO EMAC, EART AND ITWS MAJORS</NOTE>
	
These are varied and hard to analysis without matching the direct strings. Be careful
that some sections make it multi-lined::

  <NOTE>RESTRICTED TO EMAC, COMM, COMM-IT, EART,GSAS</NOTE> 
  <NOTE>DSIS, IT-ARTS MAJORS</NOTE>

Certain sections are available only to particular students in a particular region::

    <NOTE>INDIA STUDENTS ONLY</NOTE>
	<NOTE>NYC STUDENTS ONLY</NOTE>
	<NOTE>NEW YORK CITY STUDENTS ONLY</NOTE>
	<NOTE>INDIA ARCH STUDENTS ONLY</NOTE>
	<NOTE>INDIA PROGRAM STUDENTS ONLY</NOTE>
	<NOTE>RESTRICTED TO BIAM STUDENTS</NOTE>

The ones listed above are the only ones found at the time of writing (Jul 25, 2011), but
auto-detecting others kinds shouldn't be too hard to do. There seems to be only one of these
per section/course -- so a property that defines this only restriction will suffice.

Wait-Listed / By Permission
~~~~~~~~~~~~~~~~~~~~~~~~~~~

This course is waitlisted and requires contacting a designated person::

    <NOTE>CONTACT E. LARGE (LARGEE@RPI.EDU) TO BE PUT ON WAITLIST</NOTE>
	<NOTE>CONTACT ELIZABETH LARGE (LARGEE@RPI.EDU) TO BE ADDED</NOTE><NOTE>TO WAIT LIST</NOTE>
	
This seems pretty rare -- should wait listed be implemented?
Alternatively a course may be blocked until approved by some process::

    <NOTE>BY AUDITION ONLY</NOTE>
    <NOTE>ENROLLMENT BY PERMISSION OF INSTRUCTOR</NOTE>
	<NOTE>PERMISSION OF INSTRUCTOR REQUIRED</NOTE>
	<NOTE>PERMISSION OF INSTRUCTOR</NOTE>

Remember that the permission of instructor may also be in a PRE-REQS note::

    <NOTE>PRE-REQ; INTRODUCTORY COMM OR SOCIAL SCIENCE COURSE</NOTE><NOTE>OR PERMISSION OF INSTRUCTOR</NOTE>
  
Section Availability
~~~~~~~~~~~~~~~~~~~~

Some courses are available on a particular semester::

    <NOTE>COURSE TAUGHT 2ND HALF OF SEMESTER</NOTE>
	<NOTE>COURSE TAUGHT SECOND HALF OF SEMESTER</NOTE>
	<NOTE>COURSE TAUGHT FIRST HALF OF SEMESTER</NOTE>

Miscellaneous 
~~~~~~~~~~~~~

PhD. Courses::

    <NOTE>PhD COURSE</NOTE>
  
This are listed under the COMMUNICATION INTERNSHIP course::

    <NOTE>ORGANIZATIONAL MEETING WED 1/26</NOTE>
	<NOTE>ORGANIZATIONAL MEETING WED. 1/26/11</NOTE>
  
This is listed under the INTERFACE DESIGN course::

    <NOTE>KNOWLEDGE OF AUTHORING SOFTWARE FOR</NOTE> 
    <NOTE>MULTIMEDIA OR WEB DEVELOPMENT</NOTE>

or::

    <NOTE>KNOWLEDGE OF INTERACTICE AUTHORING SOFTWARE</NOTE>
  
Under HUMAN-MEDIA INTERACTION::  

	<NOTE>COUNTS AS ADVANCED HCI TOPICS</NOTE>

What's the point of a location for this section? This is noted in COMPUTER AIDED MACHINE II::
  
	<NOTE>COURSE WILL MEET IN JEC 2323</NOTE>

I don't know what this means (noted under INVENTOR'S STUDIO; SOLAR DEV. &amp;
ENERGY RENEW.; and RADIOLOGICAL ENGINEERING)::

    <NOTE>SENIOR STANDING</NOTE>
	<NOTE>JUNIOR OR SENIOR STANDING</NOTE>
	<NOTE>THIS SECTION RESTRICTED TO SENIORS</NOTE>
	<NOTE>ANY 1000/2000 LEVEL WRITING COURSE</NOTE><NOTE>OR JR/SR STATUS</NOTE>
  
Course Continuation? Filed under SENIOR DESIGN PROJECT::

    <NOTE>CONTINUATION OF MANE 4380</NOTE>

Past grade requirements (SPACECRAFT ATTITUDE DYNAMICS)::

	<NOTE>STUDENTS SHOULD HAVE EARNED AT LEAST A 'B+' IN</NOTE> 
	<NOTE>MANE 4100 AND MANE 4170 TO REGISTER FOR THIS COURSE</NOTE>
	
Specific dates the course meets (GLOBAL BUSINESS &amp; SOCIAL RESPO)::

    <NOTE>CLASS MEETS ON 12/13, 12/10, 1/3, 1/10 &amp; 1/17</NOTE>
