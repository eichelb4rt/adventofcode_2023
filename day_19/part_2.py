import numpy as np
from enum import Enum
from dataclasses import dataclass


@dataclass
class Interval:
    start: int
    end: int

    def __post_init__(self):
        self.length = self.end - self.start + 1

    def __repr__(self) -> str:
        return f"{self.start} - {self.end}"


PartSpace = dict[str, Interval]
INITIAL_PART_SPACE = {attribute_name: Interval(1, 4000) for attribute_name in ["x", "m", "a", "s"]}


class Comparison(Enum):
    LessThan = "<"
    GreaterThan = ">"


@dataclass
class Instruction:
    compared_attribute: str
    comparison: Comparison
    compared_to: int
    send_to: str

    def split(self, part_space: PartSpace) -> tuple[PartSpace, PartSpace]:
        """Returns (condition true, condition false) part spaces."""

        compared_interval = part_space[self.compared_attribute]
        if self.comparison == Comparison.LessThan:
            if compared_interval.end < self.compared_to:
                return part_space, None
            if self.compared_to < compared_interval.start:
                return None, part_space
            interval_true = Interval(compared_interval.start, self.compared_to - 1)
            interval_false = Interval(self.compared_to, compared_interval.end)
        else:
            if compared_interval.start > self.compared_to:
                return part_space, None
            if self.compared_to > compared_interval.end:
                return None, part_space
            interval_true = Interval(self.compared_to + 1, compared_interval.end)
            interval_false = Interval(compared_interval.start, self.compared_to)
        part_space_true = part_space.copy()
        part_space_false = part_space.copy()
        part_space_true[self.compared_attribute] = interval_true
        part_space_false[self.compared_attribute] = interval_false
        return part_space_true, part_space_false


@dataclass
class Workflow:
    instructions: list[Instruction]
    else_send_to: str

    def process(self, part_space: PartSpace) -> list[str, PartSpace]:
        split_part_spaces = []
        for instruction in self.instructions:
            part_space_sent, part_space = instruction.split(part_space)
            if part_space_sent is not None:
                split_part_spaces.append((instruction.send_to, part_space_sent))
            if part_space is None:
                return split_part_spaces
        split_part_spaces.append((self.else_send_to, part_space))
        return split_part_spaces


def parse_instruction(instruction: str) -> Instruction:
    first_part, send_to = instruction.split(":")
    if "<" in first_part:
        comparison_str = "<"
    else:
        comparison_str = ">"
    compared_property, compared_to_str = first_part.split(comparison_str)
    return Instruction(compared_property, Comparison(comparison_str), int(compared_to_str), send_to)


def parse_workflow(workflow: str) -> tuple[str, Workflow]:
    name_end = workflow.index("{")
    name = workflow[:name_end]
    instruction_texts = workflow[name_end + 1:-1].split(",")
    instructions = list(map(parse_instruction, instruction_texts[:-1]))
    else_send_to = instruction_texts[-1]
    return name, Workflow(instructions, else_send_to)


def _compute_n_accepted_parts(input_space: PartSpace, workflow_name: str, workflows: dict[str, Workflow]) -> int:
    if workflow_name == "A":
        return n_combinations_in(input_space)
    elif workflow_name == "R":
        return 0
    split_part_spaces = workflows[workflow_name].process(input_space)
    return sum([_compute_n_accepted_parts(part_space, send_to, workflows) for send_to, part_space in split_part_spaces])


def n_combinations_in(part_space: PartSpace) -> int:
    return int(np.prod([interval.length for interval in part_space.values()], dtype=np.uint64))


def compute_n_accepted_parts(workflows: dict[str, Workflow]) -> int:
    return _compute_n_accepted_parts(INITIAL_PART_SPACE, "in", workflows)


def solution(input_file: str):
    with open(input_file, 'r') as f:
        text = f.read()
    workflows_text, _ = text.split("\n\n")
    workflow_lines = workflows_text.splitlines()
    workflows = {name: workflow for name, workflow in map(parse_workflow, workflow_lines)}
    return compute_n_accepted_parts(workflows)


def main():
    assert solution("test_input.txt") == 167409079868000
    answer = solution("input.txt")
    print(f"<flavor text>: {answer}")


if __name__ == "__main__":
    main()

# 167_409_079_868_000
# 73_048_368_552_456
