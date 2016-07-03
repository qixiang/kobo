#!/usr/bin/python
# -*- coding: utf-8 -*-


import os
import sys
import unittest

PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_DIR)

# Following lines fix: django.core.exceptions.ImproperlyConfigured: The SECRET_KEY setting must not be empty.
import imp
module_name = "test_types_settings"
settings_module = imp.new_module(module_name)
settings_module.SECRET_KEY = "foo"
sys.modules[module_name] = settings_module
os.environ["DJANGO_SETTINGS_MODULE"] = module_name

from kobo.django.fields import StateEnumField


class TestStateEnumField(unittest.TestCase):
    def setUp(self):

        self.state_enum = StateEnum(
            State(
                name="NEW",
                next_states=["ASSIGNED", "MODIFIED"],
                check_perms=[],
            ),
            State(
                name="ASSIGNED",
                next_states=["MODIFIED"]
            ),
            State(
                name="MODIFIED",
                next_states=[]
            ),
        )
        self.state_enum.set_state("NEW")

        self.field = StateEnumField(self.state_enum, default='NEW')

    def test_to_python(self):
        t = self.field.to_python('0')
        self.assertEqual(type(t), StateEnum)
        self.assertEqual(t._current_state, 'NEW')
        t = self.field.to_python('1')
        self.assertEqual(t._current_state, 'ASSIGNED')
        t = self.field.to_python('NEW')
        self.assertEqual(type(t), StateEnum)
        self.assertEqual(t._current_state, 'NEW')
        t = self.field.to_python(t)
        self.assertEqual(type(t), StateEnum)
        self.assertEqual(t._current_state, 'NEW')
        t = self.field.to_python(2)
        self.assertEqual(type(t), StateEnum)
        self.assertEqual(t._current_state, 'MODIFIED')

    def test_choices(self):
        correct = ((0, 'NEW'), (1, 'ASSIGNED'), (2, 'MODIFIED'))
        self.assertEqual(correct, self.field.choices)


if __name__ == '__main__':
    unittest.main()
