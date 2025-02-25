#!/usr/bin/python3
""""Tests the file_storage module"""
import unittest
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel


class TestFileStorage(unittest.TestCase):
    """Class tests file_storage class"""
    def setUp(self):
        """setup before each test"""
        self.fs = FileStorage()

    def tearDown(self):
        """clean up after each test"""
        with open("file.json", "w") as f:
            blankDict = {}
            f.write("{}".format(blankDict))

    def testAll(self):
        """Test the all method"""
        self.assertEqual(self.fs.all(), {})
        a = BaseModel(id=69, created_at="1000-07-29T12:14:07.132263",
                      updated_at="1020-02-13T07:10:03.134263")
        self.fs.new(a)
        self.assertEqual(self.fs.all(), {"BaseModel.69": a})

    def testNew(self):
        """test the new method"""
        with self.assertRaises(TypeError):
            self.fs.new()

    def testSave(self):
        """tests the save method"""
        # file created
        a = BaseModel(id=69, created_at="1000-07-29T12:14:07.132263",
                      updated_at="1020-02-13T07:10:03.134263")
        self.fs.new(a)
        self.fs.save()
        with open("file.json") as f:
            line = f.readline()
            string = ['{"BaseModel.69": {"id": 69, "created_at"',
                      ': "1000-07-29T12:14:07.132263", "updated_at": ',
                      '"1020-02-13T07:10:03.134263",',
                      ' "__class__": "BaseModel"}}']
            fullstr = string[0] + string[1] + string[2] + string[3]
            self.assertEqual(line, fullstr)

    def testReload(self):
        """tests the reload method"""
        self.fs.reload()
        self.assertEqual(self.fs.all(), {})
        a = BaseModel(id=69, created_at="1000-07-29T12:14:07.132263",
                      updated_at="1020-02-13T07:10:03.134263")
        self.fs.new(a)
        self.fs.save()
        self.fs.reload()
        self.assertEqual(str(self.fs.all().get("BaseModel.69")), str(a))
