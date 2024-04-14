from typing import List
import unittest
from unittest.mock import patch
from anthropic.types import Message, MessageParam
from alana import *

class TestFunctions(unittest.TestCase):
    def test_get_xml_pattern(self):
        self.assertEqual(first=get_xml_pattern(tag="tag"), second=r"<tag>(.*?)</tag>")
        with self.assertRaises(expected_exception=ValueError):
            get_xml_pattern(tag="<tag>")

    def test_get_xml(self):
        content = "<tag>Hello</tag><tag>World</tag>"
        self.assertEqual(first=get_xml(tag="tag", content=content), second=["Hello", "World"])

    def test_remove_xml(self):
        content = "<tag>Hello</tag> <tag>World</tag>"
        self.assertEqual(first=remove_xml(tag="tag", content=content), second=" ")
        with self.assertRaises(expected_exception=ValueError):
            remove_xml(tag="<tag>", content=content)

    def test_respond(self):
        messages: list[MessageParam] = [MessageParam(role="user", content="Hi"), MessageParam(role="assistant", content="Hi")]
        updated_messages: List[MessageParam] = respond(user="Hello", messages=messages)
        self.assertEqual(first=len(updated_messages), second=3)
        self.assertEqual(first=updated_messages[-1]["role"], second="user")
        self.assertEqual(first=updated_messages[-1]["content"], second="Hello")

if __name__ == "__main__":
    unittest.main()