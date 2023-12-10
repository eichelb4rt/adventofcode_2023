import numpy as np
import itertools


Neighbours = dict[str, tuple[str, str]]


def read_neighbours(lines: str) -> Neighbours:
    neighbours: Neighbours = {}
    for line in lines:
        name, nodes_neighbours = map(str.strip, line.split("="))
        left, right = nodes_neighbours[1:-1].split(", ")
        neighbours[name] = (left, right)
    return neighbours


def walk(direction: str, from_node: str, neighbours: Neighbours) -> str:
    left, right = neighbours[from_node]
    return left if direction == "L" else right


def compute_jump_map(directions: str, neighbours: Neighbours) -> dict[str, str]:
    """Computes the map that maps every node to the node it lands on after walking through the complete direction string."""

    jump_map: dict[str, str] = {}
    for from_node in neighbours.keys():
        current_node = from_node
        for direction in directions:
            current_node = walk(direction, current_node, neighbours)
        jump_map[from_node] = current_node
    return jump_map


def is_starting_node(node: str) -> bool:
    return node[-1] == "A"


def is_destination_node(node: str) -> bool:
    return node[-1] == "Z"


def get_starting_nodes(neighbours: Neighbours) -> list[str]:
    return list(filter(is_starting_node, neighbours.keys()))


def is_repeated_by_first_n_numbers(numbers: list[int], n: int) -> bool:
    assert n > 0
    for i, number in enumerate(numbers):
        if number != numbers[i % n]:
            return False
    return True


def find_length_of_shortest_repeating_sequence(numbers: list[int]) -> int:
    for length in range(1, len(numbers)):
        if is_repeated_by_first_n_numbers(numbers, length):
            return length
    return len(numbers)


def find_loop_size(node: str, directions: str, neighbours: Neighbours) -> int:
    """Finds the length of the loop, assuming node is already in a loop."""

    destination_steps = []
    max_loop_size = len(directions) * len(neighbours)
    # walk the whole loop at least twice, save the number of steps we found a destination node on
    for i in range(2 * max_loop_size):
        direction = directions[i % len(directions)]
        node = walk(direction, node, neighbours)
        if is_destination_node(node):
            destination_steps.append(i + 1)
    # figure out the distances between destinations
    distances = [destination_steps[i + 1] - destination_steps[i] for i in range(len(destination_steps) - 1)]
    # how many destinations do we cross in 1 loop?
    destination_loop_size = find_length_of_shortest_repeating_sequence(distances)
    # destination_steps[destination_loop_size] will be the same destination as destination_steps[0], so the difference between steps is the loop size
    return destination_steps[destination_loop_size] - destination_steps[0]


def find_destination_steps_in_loop(node: str, loop_size: int, directions: str, neighbours: Neighbours) -> list[str]:
    destination_steps = []
    # walk the whole loop at least twice, save the number of steps we found a destination node on
    for i in range(loop_size):
        direction = directions[i % len(directions)]
        node = walk(direction, node, neighbours)
        if is_destination_node(node):
            destination_steps.append(i + 1)
    return destination_steps


def gcd(a: int, b: int) -> int:
    while b != 0:
        a, b = b, a % b
    return a


def eea(a: int, b: int) -> tuple[int, int]:
    """Finds p,q such that p * a + q * b == 1."""

    original_a, original_b = a, b
    p_0 = 1  # p_{n}
    p_1 = 0  # p_{n+1}
    q_0 = 0  # q_{n}
    q_1 = 1  # q_{n+1}
    while b != 0:
        d = a // b
        a, b = b, a % b  # a_{i} = b_{i-1}, b_{i} = a_{i-1} % b_{i-1}
        p_0, p_1 = p_1, p_0 - d * p_1  # p_{i} (new)   = p_{i} (old),  p_{i+1} (new)   = p_{i-1} (old) - d * p_{i} (old)
        q_0, q_1 = q_1, q_0 - d * q_1  # q_{i}         = q_{i},        q_{i+1}         = q_{i-1}       - d * q_{i}
    assert p_0 * original_a + q_0 * original_b == 1, "Something went wrong during eea."
    return p_0, q_0


def smallest_prime_factor(n: int) -> int:
    for k in range(2, int(np.sqrt(n)) + 1):
        if n % k == 0:
            return k
    return n


def factorize(n: int) -> list[int]:
    factors = []
    while n > 1:
        k = smallest_prime_factor(n)
        factors.append(k)
        n //= k
    return factors


def make_moduli_prime(offsets: list[int], moduli: list[int]) -> tuple[list[int], list[int]]:
    """Adapts the list of offsets and ms such that the moduli are prime."""

    module_to_offset: dict[int, int] = {}
    for a_i, m_i in zip(offsets, moduli):
        factors = factorize(m_i)
        for factor in factors:
            if factor in module_to_offset:
                assert module_to_offset[factor] == a_i % factor, "No solutions."
            else:
                module_to_offset[factor] = a_i % factor
    # [(m_1, a_1), ..., (m_n, a_n)] -> [m_1, ..., m_n], [a_1, ..., a_n]
    new_moduli, new_offsets = zip(*module_to_offset.items())
    return new_offsets, new_moduli


def find_solution_of_simultaneous_congruencies(offsets: list[int], moduli: list[int]) -> int:
    """Finds a solution for the simultaneous congruencies x = a_i mod m_i, if it exists. Returns None if there is none."""

    offsets, moduli = make_moduli_prime(offsets, moduli)
    moduli_product = int(np.prod(moduli))
    n_is = [moduli_product // module for module in moduli]
    # p_i * m_i + q_i * M_i == 1
    q_is = [eea(m_i, n_i)[1] for m_i, n_i in zip(moduli, n_is)]
    e_is = [q_i * n_i for q_i, n_i in zip(q_is, n_is)]
    x = sum([offset_i * e_i for offset_i, e_i in zip(offsets, e_is)]) % moduli_product
    for offset, module in zip(offsets, moduli):
        assert x % module == offset % module, "Something went wrong during chinese remainder theorem."
    return x


def compute_path_length(directions: str, neighbours: Neighbours) -> int:
    nodes = get_starting_nodes(neighbours)
    # jump into all loops, and check if we reach a destination before
    max_loop_size = len(directions) * len(neighbours)
    for i in range(max_loop_size):
        direction = directions[i % len(directions)]
        nodes = [walk(direction, node, neighbours) for node in nodes]
        # i = 0 is one step
        if all(map(is_destination_node, nodes)):
            return i + 1
    # find out how big the individual loops are
    loop_sizes = [find_loop_size(node, directions, neighbours) for node in nodes]
    destination_steps_in_loops = [find_destination_steps_in_loop(node, loop_size, directions, neighbours) for node, loop_size in zip(nodes, loop_sizes)]
    # numbers of steps where we have reached a destination on all nodes
    # for all combinations of destination nodes in different loops, solve the system of simultaneous congruencies
    all_real_destinations = [find_solution_of_simultaneous_congruencies(offsets, loop_sizes) for offsets in itertools.product(*destination_steps_in_loops)]
    return min(all_real_destinations) + max_loop_size


def solution(input_file: str):
    with open(input_file, 'r') as f:
        lines = f.read().splitlines()
    directions = lines[0].strip()
    neighbours = read_neighbours(lines[2:])
    return compute_path_length(directions, neighbours)


def main():
    assert gcd(2, 7) == 1
    assert gcd(2, 10) == 2
    assert gcd(4, 10) == 2
    assert solution("test_input_part_2.txt") == 6
    answer = solution("input.txt")
    print(f"<flavor text>: {answer}")


if __name__ == "__main__":
    main()
