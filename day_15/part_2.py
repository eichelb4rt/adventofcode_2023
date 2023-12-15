from collections import deque


def parse_instructions(line: str) -> list[str]:
    return line.split(",")


def hash_instruction(instruction: str) -> int:
    hash_result = 0
    for c in instruction:
        hash_result += ord(c)
        hash_result *= 17
        hash_result %= 256
    return hash_result


def parse_instruction(instruction: str) -> tuple[str, str, int]:
    if instruction[-1] == "-":
        return instruction[:-1], "-", 0
    return instruction[:-2], "=", int(instruction[-1])


def remove_lens(box: deque, label: str) -> None:
    for label_in_box, lens_in_box in box:
        if label_in_box == label:
            box.remove((label_in_box, lens_in_box))
            return


def replace_lens(box: deque, label: str, lens: int) -> None:
    for i, (label_in_box, lens_in_box) in enumerate(box):
        if label_in_box == label:
            box.remove((label_in_box, lens_in_box))
            box.insert(i, (label, lens))
            return
    box.append((label, lens))


def init_boxes() -> list[deque]:
    return [deque() for _ in range(256)]


def execute_instruction(instruction: str, boxes: list[deque]) -> None:
    label, operation, lens = parse_instruction(instruction)
    box = boxes[hash_instruction(label)]
    if operation == "-":
        remove_lens(box, label)
    else:
        replace_lens(box, label, lens)


def compute_focusing_power(boxes: list[deque]) -> int:
    return sum([box_number * sum([lens_number * lens for lens_number, (_, lens) in enumerate(box, 1)]) for box_number, box in enumerate(boxes, 1)])


def solution(input_file: str):
    with open(input_file, 'r') as f:
        line = f.read().strip()
    instructions = parse_instructions(line)
    boxes = init_boxes()
    for instruction in instructions:
        execute_instruction(instruction, boxes)
    return compute_focusing_power(boxes)


def main():
    assert solution("test_input.txt") == 145
    answer = solution("input.txt")
    print(f"<flavor text>: {answer}")


if __name__ == "__main__":
    main()
