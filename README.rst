Introduction
============

``pycolorname`` is a python package that aims to provide common color systems
scraped from various sites.

Supported systems
-----------------

- Pantone
- RAL-Classic

Installation
============

The easiest way to install the library is using ``pip``. To install the
latest stable version run:

::

    $ pip install pycolorname

To get bightly builds from the master branch of the github repo, use:

::

    $ pip install --pre pycolorname

Usage
=====

To use a colorsystem, import a source from the module corresponsing to the
system and create an instance of it.

To use the pantone color system, find the sources available in the
``pycolorname.pantone`` module and use one of them. For example,
the PantonePaint source can be used in the following manner:

::

    >>> from pycolorname.pantone.pantonepaint import PantonePaint
    >>> pantone_colors = PantonePaint()
    >>> pantone_colors["PMS 19-4914 TPX (Deep Teal)"]
    (23, 73, 80)

Another example using the RAL-Classic color system from the Wikipedia source:

::

    >>> from pycolorname.ral.classic.wikipedia import Wikipedia
    >>> ral_colors = Wikipedia()
    >>> ral_colors["RAL 1000 (Green beige)"]
    (204, 197, 143)

Development
===========

Testing
-------

To test the code, install dependencies using:

::

    $ pip install -r test-requirements.txt

and then execute:

::

    $ python -m pytest

Running tests will automatically update the database of files used by
the color systems by fetching it from the respective sources.

Build status
------------

|CircleCI Status|

Credits
-------

This package has been derived from
`pywikibot/pycolorname <http://git.wikimedia.org/log/pywikibot%2Fpycolorname.git>`__.
Which in turn was extracted out of
`pywikibot/compat <http://git.wikimedia.org/log/pywikibot%2Fcompat.git>`__.
These packages were created by `DrTrigon <mailto:dr.trigon@surfeu.ch>`__ who
is the original author of this package.

LICENSE
=======

|MIT|

This code falls under the
`MIT License <https://tldrlegal.com/license/mit-license>`__.
Please note that some files or content may be copied from other places
and have their own licenses. Dependencies that are being used to generate
the databases also have their own licenses.

.. |CircleCI Status| image:: https://img.shields.io/circleci/project/AbdealiJK/pycolorname/master.svg?label=CircleCI%20build
   :target: https://circleci.com/gh/AbdealiJK/pycolorname
.. |MIT| image:: https://img.shields.io/github/license/AbdealiJK/pycolorname.svg
   :target: https://opensource.org/licenses/MIT
