import numpy as np
import numpy.typing as npt


def parse_patterns(content: str) -> npt.NDArray:
    pattern_strings = content.split("\n\n")
    return [np.array([[c for c in line] for line in pattern_string.splitlines()]) for pattern_string in pattern_strings]


def find_vertical_symmetry(pattern: npt.NDArray) -> int:
    for x in range(1, pattern.shape[1]):
        min_elements = min(x, pattern.shape[1] - x)
        if np.all(pattern[:, x:x + min_elements] == pattern[:, x - 1::-1][:, :min_elements]):
            return x
    return 0


def find_horizontal_symmetry(pattern: npt.NDArray) -> int:
    for y in range(1, pattern.shape[0]):
        min_elements = min(y, pattern.shape[0] - y)
        if np.all(pattern[y:y + min_elements, :] == pattern[y - 1::-1, :][:min_elements, :]):
            return y
    return 0


def symmetry_score(pattern: npt.NDArray) -> int:
    return find_vertical_symmetry(pattern) + 100 * find_horizontal_symmetry(pattern)


def solution(input_file: str):
    with open(input_file, 'r') as f:
        content = f.read()
    patterns = parse_patterns(content)
    return sum(map(symmetry_score, patterns))


def main():
    assert solution("test_input.txt") == 405
    answer = solution("input.txt")
    print(f"<flavor text>: {answer}")


if __name__ == "__main__":
    main()
