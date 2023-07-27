from typing import Dict

from langchain.chains import LLMChain, SimpleSequentialChain, SequentialChain, TransformChain
from langchain.prompts import PromptTemplate
from langchain.schema import BaseLanguageModel
import re

class CodeChain(SimpleSequentialChain):
    """ Chain that generates code from a prompt. """
    
    @staticmethod
    async def extract_code(inputs: dict) -> dict:
        text = inputs["text"]
        result = re.search(r'```.*?\n(.*?)\n```', text, re.DOTALL)
        result = result.group(1) if result else text
        return {"output": result}

    @classmethod
    def from_prompt(cls, prompt, llm: BaseLanguageModel) -> "CodeChain":
        """ Return the code block from a Markdown chat response. """

        llm_chain = LLMChain(prompt=prompt, llm=llm)
        transform_chain = TransformChain(
            input_variables=["text"],
            output_variables=["output"],
            transform=CodeChain.extract_code,
            atransform=CodeChain.extract_code
        )
        return cls(
            chains=[llm_chain, transform_chain]
        )

class ModifyCodeChain(CodeChain):
    """ Chain that modifies code according to the given instruction. """

    @classmethod
    def from_instruction(cls, instruction: str, llm: BaseLanguageModel) -> "ModifyCodeChain":

      template = f"```\n{{input}}\n```\{instruction}\n"
      prompt = PromptTemplate(template=template, input_variables=["input"])
      return cls.from_prompt(prompt, llm)

class CompleteCodeChain(ModifyCodeChain):
  """ Chain that takes an incomplete fragment of Python code and returns the complete block. """

  @classmethod
  def from_llm(cls, llm: BaseLanguageModel) -> "CompleteCodeChain":

    # This prompt template has been tested with GPT-3.5 and GPT-4.
    instruction = "The above is an incomplete Python code fragment. Return the complete and correct code with no additional text."

    return cls.from_instruction(instruction=instruction, llm=llm)

class InputMapper(TransformChain):
  """ Chain that maps input variables to output variables. """

  @classmethod
  def from_mapping(cls, mapping: Dict) -> "InputMapper":

      async def map_dict(input_dict: Dict) -> Dict:
        return {mapping[input]: value for input, value in input_dict.items() if input in mapping}

      return TransformChain(
          input_variables=[input for input in mapping.keys()],
          output_variables=[output for output in mapping.values() if output is not None],
          transform=map_dict,
          atransform=map_dict
      )

class HumanEvalChain(SequentialChain):
  """ Chain that generates a solution to a HumanEval problem. """

  @classmethod
  def from_chain(cls, chain: CodeChain) -> "HumanEvalChain":

    transform_chain = InputMapper.from_mapping(
        mapping={
            "prompt" : "input",
            "task_id" : None
            }
    )
    return cls(
        input_variables=transform_chain.input_keys,
        output_variables=["output"],
        chains = [transform_chain, chain]
    )
  
  @classmethod
  def from_instruction(cls, instruction: str, llm: BaseLanguageModel) -> "HumanEvalChain":

    return cls.from_chain(
       CompleteCodeChain.from_instruction(instruction=instruction, llm=llm)
    )
  
  @classmethod
  def from_llm(cls, llm: BaseLanguageModel) -> "HumanEvalChain":

    return cls.from_chain(
        CompleteCodeChain.from_llm(llm=llm)
    )