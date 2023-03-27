# -*- coding: UTF-8 -*-
# Copyright (c) 2023, Daniel Patrick <daniel.patrick@netways.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import datetime
import locale
from ansible.errors import AnsibleFilterError
from ansible.module_utils.common.text.converters import to_native

DOCUMENTATION = '''
  name: to_datetime_by_locale
  short_description: Convert datestring with custom defined locale
  description:
    - Converts date strings by custom defined locale to Python C(datetime)
      object.
  options:
    _input:
      description: A date string to convert with language code and encoding
      type: string
      required: true
    language_code:
      description:
        - The language code for the locale e.g "en_US"
      required: false
      type: string
      default: The language code of the locale of the controller
    encoding:
      description:
        - The encoding for the locale e.g. "UTF-8"
      required: false
      type: string
      default: The encoding of the locale of the controller
'''

EXAMPLES = '''
- name: Convert 'Mär 16 15:55:01 2026' with to_datetime_by_locale()
  debug:
    msg: "{{ 'Mär 16 15:55:01 2026' | to_datetime_by_locale( '%b %d %H:%M:%S %Y', 'de_DE', 'UTF-8') }}"
- name: Convert 'Mar 16 15:55:01 2026' with to_datetime_by_locale()
  debug:
    msg: "{{ 'Mär 16 15:55:01 2026' | to_datetime_by_locale('%b %d %H:%M:%S %Y') }}"
'''

RETURN = '''
  _value:
    description: String converted to datetime
    type: string
'''


class FilterModule(object):
    def filters(self):
        return {
            'to_datetime_by_locale': self.to_datetime_by_locale
        }

    def to_datetime_by_locale(
            self,
            string,
            format="%Y-%m-%d %H:%M:%S",
            language_code=locale.getlocale()[0],
            encoding=locale.getlocale()[1]
            ):
        try:
            string = to_native(string)
            sequence = (language_code, encoding)
            locale.setlocale(locale.LC_ALL, sequence)
            result = datetime.datetime.strptime(string, format)
        except Exception as e:
            raise AnsibleFilterError("Exception: %s" % to_native(e))
        return to_native(result)
