LIBBGP
======

|Python Version| |Version| |License| |Build Status| |Test Coverage|

This is a BGP/BMP Message unpack/pack lib written by Python which is inspired by exabgp especially its code structure design.
We can use this lib to unpack or pack BGP/BMP messages both offline and online(like a live BGP speaker).


Quick Start
------------

Install from source code:

.. code-block:: bash

    $ git clone https://github.com/smartbgp/libbgp
    $ cd libbgp
    $ python setup.py install


or pip:

.. code-block:: bash

    $ pip install libbgp


Usage
-----

.. code-block:: bash

    $ python
    Python 2.7.10 (default, Jul 30 2016, 18:31:42)
    [GCC 4.2.1 Compatible Apple LLVM 8.0.0 (clang-800.0.34)] on darwin
    Type "help", "copyright", "credits" or "license" for more information.
    >>>
    >>> from pprint import pprint
    >>> from libbgp.bgp.message import Message
    >>> update_msg_dict = {
    ...     'type': 2,
    ...     'msg': {
    ...         'attr': {
    ...             1: 2,
    ...             2: [(2, [701, 71])],
    ...             3: '219.158.1.204',
    ...             5: 100,
    ...             6: 0,
    ...             7: [71, '16.96.243.103'],
    ...             8: ['NO_EXPORT', '1234:5678'],
    ...             9: '219.158.1.204',
    ...             10: ['219.158.1.209', '0.0.0.30']
    ...         },
    ...         'nlri': ['192.168.1.1/32', '172.16.1.1/32'],
    ...         'withdraw': []
    ...     }
    ... }
    >>> update_msg = Message.pack(update_msg_dict)
    >>> update_msg.hex_value
    '\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00f\x02\x00\x00\x00E@\x01\x01\x02@\x02\x06\x02\x02\x02\xbd\x00G@\x03\x04\xdb\x9e\x01\xcc@\x05\x04\x00\x00\x00d@\x06\x01\x00\xc0\x07\x06\x00G\x10`\xf3g\xc0\x08\x08\xff\xff\xff\x01\x04\xd2\x16.\x80\t\x04\xdb\x9e\x01\xcc\x80\n\x08\xdb\x9e\x01\xd1\x00\x00\x00\x1e \xc0\xa8\x01\x01 \xac\x10\x01\x01'
    >>> pprint(Message.unpack(update_msg.hex_value).dict())
    {'msg': {'attr': {1: 2,
                      2: [(2, [701, 71])],
                      3: '219.158.1.204',
                      5: 100,
                      6: 0,
                      7: [71, '16.96.243.103'],
                      8: ['NO_EXPORT', '1234:5678'],
                      9: '219.158.1.204',
                      10: ['219.158.1.209', '0.0.0.30']},
             'nlri': ['192.168.1.1/32', '172.16.1.1/32'],
             'withdraw': []},
     'type': 2}
    >>> Message.unpack(update_msg.hex_value).dict() == update_msg_dict
    True
    >>>


For more examples, Please reference ``libbgp/examples``

Support
-------

Please join our Slack http://smartbgp.slack.com/ for questions, discussion, suggestions, etc. And welcome to create issues and pull request.



.. |Python Version| image:: https://img.shields.io/pypi/pyversions/Django.svg
    :target: https://github.com/smartbgp/libbgp

.. |License| image:: https://img.shields.io/hexpm/l/plug.svg
   :target: https://github.com/smartbgp/libbgp/blob/master/LICENSE
.. |Version| image:: https://img.shields.io/pypi/v/libbgp.svg?
   :target: http://badge.fury.io/py/libbgp
.. |Build Status| image:: https://travis-ci.org/smartbgp/libbgp.svg?branch=master
   :target: https://travis-ci.org/smartbgp/libbgp

.. |Test Coverage| image:: https://coveralls.io/repos/smartbgp/libbgp/badge.svg?branch=master
   :target: https://coveralls.io/r/smartbgp/libbgp
