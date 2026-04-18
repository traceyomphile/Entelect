
class InputOutput:
    def __init__(self, input_file: str, output_file: str):
        self.input_file: str = input_file
        self.output_file: str = output_file

    def read_input(self) -> list[str]:
        contents: list[str] = []
        with open(self.input_file, 'r') as file:
           for line in file:
                contents.append(line.strip())
        return contents

    def write_output(self, data: list[str]):
        with open(self.output_file, 'w') as file:
            for line in data:
                file.write(line + '\n')