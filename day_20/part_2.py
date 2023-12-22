from dataclasses import dataclass
from abc import ABC, abstractmethod
from collections import deque


def broadcast(pulse: bool, modules: str) -> list[tuple[str, bool]]:
    return [(module, pulse) for module in modules]


@dataclass
class Module(ABC):
    destination_modules: list[str]

    @abstractmethod
    def process(self, pulse: bool, from_module: str) -> list[tuple[str, bool]]:
        pass


class FlipFlop(Module):
    def __init__(self, destination_modules: list[str]) -> None:
        super().__init__(destination_modules)
        self.state = False

    def process(self, pulse: bool, from_module: str) -> list[tuple[str, bool]]:
        if pulse == True:
            return []
        self.state = not self.state
        return broadcast(self.state, self.destination_modules)


class Conjunction(Module):
    def __init__(self, destination_modules: list[str]) -> None:
        super().__init__(destination_modules)
        self.memory: dict[str, bool] = {}

    def process(self, pulse: bool, from_module: str) -> list[tuple[str, bool]]:
        self.memory[from_module] = pulse
        response = not all([state == True for state in self.memory.values()])
        return broadcast(response, self.destination_modules)


class Broadcaster(Module):
    def __init__(self, destination_modules: list[str]) -> None:
        super().__init__(destination_modules)

    def process(self, pulse: bool, from_module: str) -> list[tuple[str, bool]]:
        return broadcast(pulse, self.destination_modules)


def parse_module(line: str) -> tuple[str, Module]:
    type_and_name, destinations_str = line.split(" -> ")
    if type_and_name[0] == "%":
        cls = FlipFlop
        module_name = type_and_name[1:]
    elif type_and_name[0] == "&":
        cls = Conjunction
        module_name = type_and_name[1:]
    else:
        cls = Broadcaster
        module_name = type_and_name
    return module_name, cls(destinations_str.split(", "))


def prime_conjunctions(modules: dict[str, Module]) -> None:
    for module_name, module in modules.items():
        for destination_module in module.destination_modules:
            if destination_module in modules and isinstance(modules[destination_module], Conjunction):
                modules[destination_module].process(False, module_name)


def push_button_once(modules: dict[str, Module]) -> bool:
    signals: deque[tuple[str, str, bool]] = deque()
    signals.append(("button", "broadcaster", False))
    while len(signals) > 0:
        from_module, module, pulse = signals.popleft()
        if module not in modules:
            continue
        sent_signals = modules[module].process(pulse, from_module)
        for send_to, sent_pulse in sent_signals:
            if send_to == "rx" and sent_pulse == False:
                return True
            signals.append((module, send_to, sent_pulse))
    return False


def push_button_often(modules: dict[str, Module]) -> int:
    n_button_presses = 1
    while not push_button_once(modules):
        n_button_presses += 1
    return n_button_presses


def solution(input_file: str):
    with open(input_file, 'r') as f:
        lines = f.read().splitlines()
    modules = {name: module for name, module in map(parse_module, lines)}
    prime_conjunctions(modules)
    return push_button_often(modules)


def main():
    answer = solution("input.txt")
    print(f"<flavor text>: {answer}")


if __name__ == "__main__":
    main()
