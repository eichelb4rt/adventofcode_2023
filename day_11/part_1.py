import numpy as np
import numpy.typing as npt


def find_empty_rows(is_galaxy: npt.NDArray[np.bool8]) -> npt.NDArray[np.int64]:
    return np.array([y for y in range(is_galaxy.shape[0]) if np.all(is_galaxy[y, :] == False)])


def find_empty_columns(is_galaxy: npt.NDArray[np.bool8]) -> npt.NDArray[np.int64]:
    return np.array([x for x in range(is_galaxy.shape[1]) if np.all(is_galaxy[:, x] == False)])


def parse_galaxies(lines: list[str]) -> npt.NDArray[np.bool8]:
    return np.array([[c == "#" for c in line] for line in lines])


def distance(galaxy_coords_1: npt.NDArray[np.int64], galaxy_coords_2: npt.NDArray[np.int64], empty_rows: npt.NDArray[np.int64], empty_columns: npt.NDArray[np.int64]) -> int:
    min_x, max_x = min(galaxy_coords_1[1], galaxy_coords_2[1]), max(galaxy_coords_1[1], galaxy_coords_2[1])
    min_y, max_y = min(galaxy_coords_1[0], galaxy_coords_2[0]), max(galaxy_coords_1[0], galaxy_coords_2[0])
    empty_columns_between = np.count_nonzero((empty_columns > min_x) & (empty_columns < max_x))
    empty_rows_between = np.count_nonzero((empty_rows > min_y) & (empty_rows < max_y))
    return (max_x - min_x) + (max_y - min_y) + empty_columns_between + empty_rows_between


def solution(input_file: str):
    with open(input_file, 'r') as f:
        lines = f.read().splitlines()
    is_galaxy = parse_galaxies(lines)
    galaxy_coords = np.transpose(np.nonzero(is_galaxy))
    empty_rows = find_empty_rows(is_galaxy)
    empty_columns = find_empty_columns(is_galaxy)
    n_galaxies = len(galaxy_coords)
    return sum([distance(galaxy_coords[i], galaxy_coords[j], empty_rows, empty_columns) for i in range(n_galaxies) for j in range(i + 1, n_galaxies)])


def main():
    assert solution("test_input.txt") == 374
    answer = solution("input.txt")
    print(f"<flavor text>: {answer}")


if __name__ == "__main__":
    main()
