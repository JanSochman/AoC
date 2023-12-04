from dataclasses import dataclass

@dataclass
class StateMachine:
    # how to use StateMachine
    # state_machine = StateMachine(
    # ...     memory={"g": 0}, program=["set g 45", "inc g"]
    # ... )
    # >>> state_machine.run()
    # >>> state_machine.memory
    memory: dict[str, int]
    program: list[str]

    def run(self):
        """Run the program."""
        current_line = 0
        while current_line < len(self.program):
            instruction = self.program[current_line]

            # Set a register to a value
            if instruction.startswith("set "):
                register, value = instruction[4], int(instruction[6:])
                self.memory[register] = value

            # Increase the value in a register by 1
            elif instruction.startswith("inc "):
                register = instruction[4]
                self.memory[register] += 1

            # Move the line pointer
            current_line += 1


# ----------------------------------------------
# BP2BINARY = str.maketrans({"F": "0", "B": "1", "L": "0", "R": "1"})
# BP2BINARY = str.maketrans("FBLR", "0101")

# def parse(puzzle_input):
#     """Parse input."""
#     return [
#         int(bp.translate(BP2BINARY), base=2)
#         for bp in puzzle_input.split("\n")
#     ]