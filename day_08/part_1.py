STARTING_NODE = "AAA"
DESTINATION_NODE = "ZZZ"


Neighbours = dict[str, tuple[str, str]]


def read_neighbours(lines: str) -> Neighbours:
    neighbours: Neighbours = {}
    for line in lines:
        name, nodes_neighbours = map(str.strip, line.split("="))
        left, right = nodes_neighbours[1:-1].split(", ")
        neighbours[name] = (left, right)
    return neighbours


def compute_path_length(directions: str, neighbours: Neighbours) -> int:
    current_node = STARTING_NODE
    n_steps = 0
    while True:
        direction = directions[n_steps % len(directions)]
        left, right = neighbours[current_node]
        current_node = left if direction == "L" else right
        n_steps += 1
        if current_node == DESTINATION_NODE:
            return n_steps


def solution(input_file: str):
    with open(input_file, 'r') as f:
        lines = f.read().splitlines()
    directions = lines[0].strip()
    neighbours = read_neighbours(lines[2:])
    return compute_path_length(directions, neighbours)


def main():
    assert solution("test_input_1_part_1.txt") == 2
    assert solution("test_input_2_part_1.txt") == 6
    answer = solution("input.txt")
    print(f"<flavor text>: {answer}")


if __name__ == "__main__":
    main()
