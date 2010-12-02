Overview
========

``rpi_courses`` is a simple Python_ library for reading and using RPI_'s
course schedule.

It can parse the `XML files`_ provided on RPI's SIS system and provides a
primitive object-oriented API layer to access the course information.

Also, it provides rudimentary method to computing schedules using constraints.

.. _Python: http://python.org/
.. _RPI: http://rpi.edu/
.. _XML files: http://sis.rpi.edu/reg/rocs/

Usage
----

To install::

  pip install rpi_courses

Then you can import it to your python scripts::

  from rpi_courses import CourseCatalog, list_xml_files

``list_xml_files`` accepts an optional URL argument, the default url is
assumed to be "http://sis.rpi.edu/reg/rocs/". This function expects to
read an apache-style file listing page. It scrapes all the files listed
there that end with a xml file extension and returns the full URLs to those
files::

  >>> files = list_xml_files()
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

With the most important being the Course object with contains::

 - ``


.. _BeautifulSoup: http://www.crummy.com/software/BeautifulSoup/documentation.html#Parsing HTML
.. _BeautifulStoneSoup: http://www.crummy.com/software/BeautifulSoup/documentation.html#Parsing XML
.. _Datetime: http://docs.python.org/library/datetime.html

TODOs
=====

Provide way to hook into the `Academic Catalog`_ for course descriptions.
This would require being able to parse with catalog to load and then scrape
the appropriate information from the ajax-y page.

.. _Academic Catalog: http://www.rpi.edu/academics/catalog/