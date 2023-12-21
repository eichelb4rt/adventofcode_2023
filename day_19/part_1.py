from dataclasses import dataclass
from enum import Enum

Part = dict[str, int]

class Comparison(Enum):
    LessThan = "<"
    GreaterThan = ">"
    

@dataclass
class Instruction:
    compared_attribute: str
    comparison: Comparison
    compared_to: int
    send_to: str
    
    def matches(self, part: Part) -> bool:
        if self.comparison == Comparison.LessThan:
            return part[self.compared_attribute] < self.compared_to
        return part[self.compared_attribute] > self.compared_to


@dataclass
class Workflow:
    instructions: list[Instruction]
    else_send_to: str
    
    def process(self, part: Part) -> str:
        for instruction in self.instructions:
            if instruction.matches(part):
                return instruction.send_to
        return self.else_send_to


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


def parse_part(part_str: str) -> Part:
    assignment_strings = part_str[1:-1].split(",")
    part = {}
    for assignment_string in assignment_strings:
        attribute_name, attribute_value_str = assignment_string.split("=")
        part[attribute_name] = int(attribute_value_str)
    return part


def is_accepted(part: Part, workflows: dict[str, Workflow]) -> bool:
    workflow_name = "in"
    while workflow_name not in ["A", "R"]:
        workflow_name = workflows[workflow_name].process(part)
    return workflow_name == "A"


def rating(part: Part) -> int:
    return sum(part.values())


def solution(input_file: str):
    with open(input_file, 'r') as f:
        text = f.read()
    workflows_text, parts_text = text.split("\n\n")
    workflow_lines = workflows_text.splitlines()
    part_lines = parts_text.splitlines()
    workflows = {name: workflow for name, workflow in map(parse_workflow, workflow_lines)}
    parts = list(map(parse_part, part_lines))
    accepted_parts = list(filter(lambda part: is_accepted(part, workflows), parts))
    return sum(map(rating, accepted_parts))


def main():
    assert solution("test_input.txt") == 19114
    answer = solution("input.txt")
    print(f"<flavor text>: {answer}")


if __name__ == "__main__":
    main()
