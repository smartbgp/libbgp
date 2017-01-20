# Copyright 2015-2017 Cisco Systems, Inc.
# All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

_FATAL_EXCEPTION_FORMAT_ERRORS = False


class BaseException(Exception):
    """Base Exception.
    """
    message = "An unknown exception occurred."

    def __init__(self, **kwargs):
        try:
            super(BaseException, self).__init__(self.message % kwargs)
            self.msg = self.message % kwargs
        except Exception:
            if _FATAL_EXCEPTION_FORMAT_ERRORS:
                raise
            else:
                # at least get the core message out if something happened
                super(BaseException, self).__init__(self.message)

    def __unicode__(self):
        return unicode(self.msg)


class MessageUncompleted(BaseException):
    message = 'Message Uncompleted'


class BGPNotification(Exception):
    """BGP Notification Exception.
    """
    message = 'BGP Notification Exception'

    def __init__(self, error_code, sub_error_code, data=''):

        try:
            super(BGPNotification, self).__init__()
            self.error_code = error_code
            self.sub_error_code = sub_error_code
            self.data = data
            self.msg = self.message
        except Exception:
            if _FATAL_EXCEPTION_FORMAT_ERRORS:
                raise
            else:
                # at least get the core message out if something happened
                super(BGPNotification, self).__init__(self.msg)

    def __unicode__(self):
        return unicode(self.msg)
