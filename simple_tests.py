from typing import List
import unittest
from unittest.mock import patch
from anthropic.types import Message, MessageParam, ContentBlock, Usage
from alana import *
from flaky import flaky

class TestFunctions(unittest.TestCase):
    def test_get_xml_pattern(self):
        """Check the pattern against hard-coded regex."""
        self.assertEqual(first=get_xml_pattern(tag="tag"), second=r"<tag>(.*?)</tag>")
        with self.assertRaises(expected_exception=ValueError):
            get_xml_pattern(tag="<tag>")

    def test_get_xml(self):
        """Check XML extraction against a hard-coded example."""
        content = "<tag>Hello</tag><tag>World</tag>"
        self.assertEqual(first=get_xml(tag="tag", content=content), second=["Hello", "World"])

    def test_remove_xml(self):
        """Check XML removal against a hard-coded example."""
        content = "<tag>Hello</tag> <tag>World</tag>"
        self.assertEqual(first=remove_xml(tag="tag", content=content), second=" ")
        with self.assertRaises(expected_exception=ValueError):
            remove_xml(tag="<tag>", content=content)

    def test_respond(self):
        """Check that respond correctly appends a user message."""
        messages: list[MessageParam] = [MessageParam(role="user", content="Hi"), MessageParam(role="assistant", content="Hi")]
        updated_messages: List[MessageParam] = respond(user="Hello", messages=messages)
        self.assertEqual(first=len(updated_messages), second=3)
        self.assertEqual(first=updated_messages[-1]["role"], second="user")
        self.assertEqual(first=updated_messages[-1]["content"], second="Hello")
    
    def test_gen(self):
        """Check that `gen` correctly appends to `messages`."""
        messages: list[MessageParam] = [MessageParam(role="user", content="Hi")]
        gen(messages=messages, model="haiku", system="Respond in Spanish", loud=False)
        green(var=f"Confirm output in Spanish {messages[-1]['content']}")
        self.assertEqual(first=len(messages), second=2)
        self.assertEqual(first=messages[-1]["role"], second="assistant")
        self.assertEqual(first=messages[0]["content"], second="Hi")
        self.assertEqual(first=messages[0]["role"], second="user")
 
    def test_gen_prefill(self):
        """Check that `gen` correctly appends to last message of `messages` when the last message is from an assistant."""
        messages: list[MessageParam] = [MessageParam(role="user", content="Hi"), MessageParam(role="assistant", content="Hi")]
        gen(messages=messages, model="haiku", loud=False)
        green(var=f"Manually confirms this looks alright: {messages}")
        self.assertEqual(first=len(messages), second=2)
        self.assertEqual(first=messages[-1]["role"], second="assistant")
        self.assertEqual(first=messages[-1]["content"][:2], second="Hi") # type: ignore
        self.assertGreater(a=len(messages[-1]["content"]), b=len("Hi")) # type: ignore
    
    def test_gen_with_user(self):
        """Check that `gen` correctly appends a user message to `messages` when specified, and does so before responding."""
        messages: list[MessageParam] = [MessageParam(role="user", content="Hi"), MessageParam(role="assistant", content="Hi")]
        gen(messages=messages, user="Say Hello")
        self.assertEqual(first=messages[2]["content"], second="Say Hello")
        for i in range(4):
            self.assertEqual(first=messages[i]["role"], second=["user", "assistant", "user", "assistant"][i])
    
    @flaky(max_runs=3)
    def test_gen_msg_with_default_args(self):
        messages = [MessageParam(role="user", content="Test message. Respond with 'Test response'")]
        response = gen_msg(messages, model="haiku")
        self.assertEqual(response.content[0].text, "Test response")

    @flaky(max_runs=3)
    def test_gen_msg_with_custom_args(self):
        messages = [MessageParam(role="user", content="Ping.")]
        response = gen_msg(
            messages,
            system="When the user says Ping, respond with 'Pong. Pong.'.",
            model="sonnet",
            max_tokens=500,
            temperature=0.5,
            loud=False,
            stop_sequences=['.']
        )
        self.assertEqual(response.content[0].text, "Pong")
        
    @flaky(max_runs=3)
    def test_gen_msg_with_invalid_model(self):
        messages = [MessageParam(role="user", content="Test message")]
        response = gen_msg(messages, model="not_a_model", system="Respond with the phrase `Test response`")
        
        self.assertEqual(response.content[0].text, "Test response")

if __name__ == "__main__":
    unittest.main()