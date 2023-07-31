import unittest
from unittest.mock import Mock

from langchain.chat_models import ChatOpenAI
from langchain.prompts.prompt import PromptTemplate

from codechain.generation import CodeChain, ModifyCodeChain, CompleteCodeChain, InputMapper

class TestCodeChain(unittest.TestCase):

    def setUp(self):
        self.llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.2)
        self.prompt = PromptTemplate(template="{input}", input_variables=["input"])
        self.template = Mock()

    def test_from_prompt(self):
        result = CodeChain.from_prompt(self.prompt, self.llm)
        self.assertIsInstance(result, CodeChain)

    def test_from_instruction(self):
        result = ModifyCodeChain.from_instruction("Instruction", self.llm)
        self.assertIsInstance(result, ModifyCodeChain)

    def test_from_llm(self):
        result = CompleteCodeChain.from_llm(self.llm)
        self.assertIsInstance(result, CompleteCodeChain)

    def test_from_mapping(self):
        result = InputMapper.from_mapping({"input": "output"})
        self.assertIsInstance(result, InputMapper)

if __name__ == '__main__':
    unittest.main()