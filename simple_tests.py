from typing import List
import unittest
from unittest.mock import patch
from anthropic.types import Message, MessageParam, ContentBlock, Usage
from anthropic import RateLimitError, InternalServerError
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
        gen(messages=messages, model="haiku", loud=False, temperature=0.0)
        self.assertEqual(first=len(messages), second=2)
        self.assertEqual(first=messages[-1]["role"], second="assistant")
        self.assertEqual(first=messages[-1]["content"][:2], second="Hi") # type: ignore
        self.assertGreater(a=len(messages[-1]["content"]), b=len("Hi")) # type: ignore

        self.assertEqual(first=messages[-1]["content"], second="Hi there! How can I assist you today?")
    
    def test_gen_with_user(self):
        """Check that `gen` correctly appends a user message to `messages` when specified, and does so before responding."""
        messages: list[MessageParam] = [MessageParam(role="user", content="Hi"), MessageParam(role="assistant", content="Hi")]
        gen(messages=messages, user="Say Hello")
        self.assertEqual(first=messages[2]["content"], second="Say Hello")
        for i in range(4):
            self.assertEqual(first=messages[i]["role"], second=["user", "assistant", "user", "assistant"][i])
    
    @flaky(max_runs=1, min_passes=1)
    def test_gen_msg_with_default_args(self):
        """Hard-coded check that `gen_msg` works in a normal use-case"""
        messages: List[MessageParam] = [MessageParam(role="user", content="Test message. Respond with 'Test response'")]
        model = "haiku"
        response: Message = gen_msg(messages=messages, model=model, temperature=0.0) # NOTE: This is potential source of flake, bc even temp=0.0 is non-deterministic
        self.assertEqual(first=response.content[0].text, second="Test response")
        self.assertEqual(first=response.stop_reason, second="end_turn") # NOTE: This is potential source of flake.
        self.assertEqual(first=response.role, second="assistant")
        self.assertEqual(first=response.type, second="message")
        self.assertEqual(first=response.model, second=globals.MODELS[model]) # type: ignore

    @flaky(max_runs=1, min_passes=1)
    def test_gen_msg_with_custom_args(self):
        """Hard-coded check that `gen_msg` works with custom arguments"""
        messages: List[MessageParam] = [MessageParam(role="user", content="Ping.")]
        model = "sonnet"
        response: Message = gen_msg(
            messages,
            system="When the user says Ping, respond with 'Pong. Pong.'.",
            model=model,
            max_tokens=500,
            temperature=0.0,
            loud=False,
            stop_sequences=['.']
        )
        self.assertEqual(response.content[0].text, "Pong")
        self.assertEqual(first=response.stop_reason, second="stop_sequence") # NOTE: This is potential source of flake.
        self.assertEqual(first=response.role, second="assistant")
        self.assertEqual(first=response.type, second="message")
        self.assertEqual(first=response.stop_sequence, second=".") # NOTE: This is potential source of flake.
        self.assertEqual(first=response.model, second=globals.MODELS[model]) # type: ignore
        
    @flaky(max_runs=1, min_passes=1)
    def test_gen_msg_with_invalid_model(self):
        """Hard-coded check that `gen_msg` reverts to default model when passed in an invalid model."""
        messages: List[MessageParam] = [MessageParam(role="user", content="Test message")]
        response: Message = gen_msg(messages, model="not_a_model", system="Respond with the phrase `Test response`", temperature=0.0)
        self.assertEqual(first=response.content[0].text, second="Test response")
        self.assertEqual(first=response.model, second=globals.DEFAULT_MODEL) # type: ignore
        self.assertEqual(len(messages), second=1)
    
    @flaky(max_runs=2, min_passes=1)
    def test_gen_matches_example(self):
        """Hard-coded check that `gen` correctly handles a case very similar to the usage example shown in the README."""
        messages = []
        output: str = alana.gen(user="Hello, Claude!", messages=messages, temperature=0.0, model="sonnet")
        self.assertEqual(first=messages[0]['role'], second='user')
        self.assertEqual(first=messages[0]['content'], second='Hello, Claude!')
        self.assertEqual(first=messages[1]['role'], second='assistant')
        self.assertEqual(first=messages[1]['content'], second="Hello! It's nice to meet you. How can I assist you today?")
        self.assertEqual(first=messages[1]['content'], second=output)
        self.assertEqual(first=len(messages), second=2)

    @flaky(max_runs=1, min_passes=1)
    def test_integration_gen_response_gen(self):
        """Use `gen` and `respond` to carry on a hard-coded simulated multi-turn conversation."""
        messages: List[MessageParam] = [
            MessageParam(
                role="user",
                content="Hello, Claude!"
            ),
            MessageParam(
                role="assistant",
                content="Hello! It's nice to meet you. How can I assist you"
            )
        ]
        output: str = alana.gen(messages=messages, temperature=0.0, model="sonnet")
        self.assertEqual(first=len(messages), second=2)
        self.assertEqual(first=messages[-1]["role"], second="assistant")
        self.assertEqual(first=messages[-1]["content"], second="Hello! It's nice to meet you. How can I assist you today?")
        self.assertEqual(first=output, second=" today?")
        respond(user="What is the name of your favorite Pokemon? Mine is Pikachu.", messages=messages)
        self.assertEqual(first=messages[-1]["role"], second="user")
        self.assertEqual(first=messages[-1]["content"], second="What is the name of your favorite Pokemon? Mine is Pikachu.")
        output = gen(messages=messages, temperature=0.0, model="sonnet")
        self.assertIn(member="Pikachu", container=output)
        self.assertEqual(first=messages[-1]["role"], second="assistant")
        self.assertEqual(first=messages[-1]["content"], second=output)
        self.assertNotEqual(first=messages[-1]["content"], second=messages[-2]["content"])
        self.assertEqual(first=len(messages), second=4)

        respond(user="One more response!", messages=messages)
        self.assertEqual(first=len(messages), second=5)
        gen(messages=messages, append=False)
        self.assertEqual(first=len(messages), second=5)
    
    @flaky(max_runs=1, min_passes=1)
    def test_gen_examples_list(self):
        """Hard-coded check that generating a list of examples generates a list of strings of appropriate length."""
        instruction = "Write a one-sentence story about a magical adventure."
        n_examples = 3
        examples: List[str] = gen_examples_list(instruction=instruction, n_examples=n_examples, temperature=0.0, model="opus", loud=False)
        self.assertEqual(first=len(examples), second=n_examples)
        for example in examples:
            self.assertIsInstance(obj=example, cls=str)
            self.assertGreater(a=len(example), b=1)

    @flaky(max_runs=1, min_passes=1)
    def test_gen_examples(self):
        """Hard-coded test for gen_examples via regex parsing"""
        instruction = "Write a two-sentence story about a magical adventure."
        n_examples = 3
        examples_str: str = gen_examples(instruction, n_examples=n_examples, temperature=0.0, model="sonnet", loud=False)
        self.assertIsInstance(obj=examples_str, cls=str)

        examples = get_xml(tag="examples", content=examples_str)
        self.assertEqual(first=len(examples), second=1)
        self.assertGreater(a=len(examples[0]), b=1)

        examples: List[str] = get_xml(tag="example", content=examples[0])
        self.assertEqual(first=len(examples), second=n_examples)
        for example in examples:
            self.assertIsInstance(obj=example, cls=str)
            self.assertTrue(expr=len(example) > 0)

    @flaky(max_runs=1, min_passes=1)
    def test_gen_prompt(self):
        """Check that `gen_prompt`'s output at least looks reasonable."""
        instruction = "Write a story about a robot learning to love."
        try:
            prompts = gen_prompt(instruction=instruction, temperature=0.0, model="haiku", loud=False)
            self.assertIsInstance(obj=prompts, cls=dict)
            self.assertIn(member="system", container=prompts)
            self.assertIn(member="user", container=prompts)
            self.assertIn(member="full", container=prompts)
            self.assertIsInstance(obj=prompts["system"], cls=(str, list))
            self.assertIsInstance(obj=prompts["user"], cls=(str, list))
            self.assertIsInstance(obj=prompts["full"], cls=str)
        except InternalServerError as e:
            red(var=f"`test_gen_prompt`: Internal server error {e}") # NOTE: I ran into this a few times.

    @flaky(max_runs=1, min_passes=1)
    def test_pretty_print(self):
        """Check that pretty print contains all requested data."""
        var = {"name": "John", "age": 30, "city": "New York"}
        pretty_output: str = pretty_print(var=var, loud=False)
        self.assertIsInstance(obj=pretty_output, cls=str)
        self.assertTrue(len(pretty_output) > 0)
        self.assertIn(member="'John'", container=pretty_output)
        self.assertIn(member="30", container=pretty_output)
        self.assertIn(member="'New York'", container=pretty_output)

if __name__ == "__main__":
    unittest.main()