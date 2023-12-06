# destination range start, source range start, range length
MapEntry = tuple[int, int, int]
# source category, destination category, entries
AlmanacMap = tuple[str, str, list[MapEntry]]


def parse_seeds(line: str) -> list[int]:
    return list(map(int, line[len("seeds: "):].split()))


def parse_map_entry(line: str) -> MapEntry:
    return tuple(map(int, line.split()))


def parse_map(lines: list[str]) -> AlmanacMap:
    # example: "seed-to-soil map:"
    source_category, destination_category = lines[0].split()[0].split("-to-")
    return source_category, destination_category, list(map(parse_map_entry, lines[1:]))


def partition_map_lines(lines: list[str]) -> list[list[str]]:
    map_lines: list[list[str]] = []
    map_start = 0
    for i, line in enumerate(lines):
        # source-to-destination starts a map
        if "-to-" in line:
            map_start = i
        # empty line ends the map
        elif len(line.strip()) == 0:
            map_lines.append(lines[map_start:i])
    # append last map
    map_lines.append(lines[map_start:])
    return map_lines


def parse_maps(lines: list[str]) -> list[AlmanacMap]:
    partitioned_lines = partition_map_lines(lines)
    return list(map(parse_map, partitioned_lines))


def is_mapped_by(source_value: int, map_entry: MapEntry) -> bool:
    _, source_range_start, range_length = map_entry
    return source_range_start <= source_value < source_range_start + range_length


def apply_map_entry(source_value: int, map_entry: MapEntry) -> bool:
    """Assumes that the value is mapped by the entry."""

    destination_range_start, source_range_start, _ = map_entry
    offset = destination_range_start - source_range_start
    return source_value + offset


def apply_map(source_value: int, almanac_map: AlmanacMap) -> int:
    _, _, map_entries = almanac_map
    for map_entry in map_entries:
        if is_mapped_by(source_value, map_entry):
            return apply_map_entry(source_value, map_entry)
    return source_value


def solution(input_file: str):
    with open(input_file, 'r') as f:
        lines = f.read().splitlines()
    source_values = parse_seeds(lines[0])
    maps = parse_maps(lines[2:])
    for almanac_map in maps:
        source_values = list(map(lambda source_value: apply_map(source_value, almanac_map), source_values))
    return min(source_values)


def main():
    assert solution("test_input.txt") == 35
    answer = solution("input.txt")
    print(f"<flavor text>: {answer}")


if __name__ == "__main__":
    main()
