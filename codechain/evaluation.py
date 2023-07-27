from typing import Optional

from langsmith.evaluation import RunEvaluator, EvaluationResult
from langsmith.schemas import Run, Example

from human_eval.execution import check_correctness
from human_eval.data import read_problems

class HumanEvalEvaluator(RunEvaluator):
    """ This is a wrapper around the HumanEval evaluator. """

    def __init__(self):
        self.problems = read_problems()

    def evaluate_run(self, run: Run, example: Optional[Example] = None) -> EvaluationResult:
        print("Evaluating " + run.inputs["task_id"])
        problem = HumanEvalEvaluator.self.problems[run.inputs["task_id"]]
        solution = run.outputs["output"]

        # The HumanEval evaluator, which runs the Python code against unit tests
        result = check_correctness(problem, solution, 5)

        return EvaluationResult(
            key = "Correctness",
            score = bool(result["passed"])
            )