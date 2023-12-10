def read_sequence(line: str) -> list[int]:
    return list(map(int, line.split()))


def produce_difference_sequence(sequence: list[int]) -> list[int]:
    return [sequence[i + 1] - sequence[i] for i in range(len(sequence) - 1)]


def predict_previous(sequence: list[int]) -> int:
    sequences: list[list[int]] = [sequence]
    while any([value != 0 for value in sequences[-1]]):
        sequences.append(produce_difference_sequence(sequences[-1]))
    return sum([sequence[0] if i % 2 == 0 else -sequence[0] for i, sequence in enumerate(sequences)])


def solution(input_file: str):
    with open(input_file, 'r') as f:
        lines = f.read().splitlines()
    sequences = list(map(read_sequence, lines))
    predictions = list(map(predict_previous, sequences))
    return sum(predictions)


def main():
    assert solution("test_input.txt") == 2
    answer = solution("input.txt")
    print(f"<flavor text>: {answer}")


if __name__ == "__main__":
    main()
