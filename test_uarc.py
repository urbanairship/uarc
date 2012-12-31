#!/usr/bin/env python
import unittest

import uarc


class UaRcTests(unittest.TestCase):
    def setUp(self):
        self.sample_files = ['sample.ini', 'sample2.ini']
        self.rc = uarc.Uarc(filenames=self.sample_files)
        self.app = self.rc.get_app('test-app')

    def test_sample_files_loaded(self):
        """Test that sample files were loaded"""
        self.assertEqual(self.rc.files, self.sample_files)

    def test_missing_files_ignored(self):
        """Missing files should be ignored"""
        f = ['lol', 'wat'] + self.sample_files
        rc = uarc.Uarc(filenames=f)
        self.assertEqual(rc.files, self.sample_files)

    def test_get_app(self):
        """Test sample app's values"""
        self.assertEqual(self.app.key, '-22-character-app-key-')
        self.assertEqual(self.app.secret, None)
        self.assertEqual(self.app.master, None)

    def test_get_device(self):
        """Test sample app's alias retrieval"""
        d = self.app.get_device('some_alias')
        self.assertEqual(d.alias, 'some_alias')
        self.assertEqual(d.family, 'apid')
        self.assertEqual(d.id, 'lolwat')
        self.assertFalse(self.app.get_device('not-a-real-alias'))
        self.assertEqual(self.app.apids, {'lolwat': 'some_alias'})
        self.assertEqual(self.app.device_tokens, {})
        self.assertEqual(self.app.device_pins, {})


if __name__ == '__main__':
    unittest.main()
