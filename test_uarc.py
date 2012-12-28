#!/usr/bin/env python
import unittest

import uarc


class UaRcTests(unittest.TestCase):
    def setUp(self):
        self.sample_files = ['sample.ini', 'sample2.ini']
        self.rc = uarc.Uarc(filenames=self.sample_files)

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
        app = self.rc.get_app('test-app')
        self.assertEqual(app.key, '-22-character-app-key-')
        self.assertEqual(app.secret, None)
        self.assertEqual(app.master, None)
        self.assertEqual(app.apids.get('some_alias'), 'lolwat')
        self.assertEqual(len(app.device_tokens), 0)


if __name__ == '__main__':
    unittest.main()
