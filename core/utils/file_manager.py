from typing import Optional, Tuple, Union, List


def file_to_list(
    filename: str, lines: Union[None, int, Tuple[int, int], List[int]] = None
) -> List[str]:
    """
    Reads a file and returns the specified lines as a list.
    Line numbers start from 1.

    :param filename: The name of the file to read from.
    :param lines: The lines to return, which can be:
                  - None (returns all lines),
                  - int (returns a specific line),
                  - tuple of two ints (returns a range of lines),
                  - list of ints (returns specific lines).
    :return: A list of the content of the specified lines.
    :raises ValueError: If any line number is out of range.
    """
    with open(filename, "r+") as f:
        lines_list = list(filter(bool, f.read().splitlines()))

    def get_line(line_number: int) -> str:
        if line_number < 1 or line_number > len(lines_list):
            raise ValueError("Line number is out of range")
        return lines_list[line_number - 1]

    if lines is None:
        return lines_list
    elif isinstance(lines, int):
        return [get_line(lines)]
    elif isinstance(lines, tuple) and len(lines) == 2:
        start, end = lines
        if start < 1 or end > len(lines_list) or start > end:
            raise ValueError("Line range is out of range or invalid")
        return lines_list[start - 1 : end]
    elif isinstance(lines, list):
        return [get_line(line) for line in lines]
    else:
        raise ValueError("Invalid input for lines parameter")


def str_to_file(file_name: str, msg: str, mode: Optional[str] = "a"):
    with open(
            file_name,
            mode
    ) as text_file:
        text_file.write(f"{msg}\n")


def shift_file(file):
    with open(file, 'r+') as f:  # open file in read / write mode
        first_line = f.readline()  # read the first line and throw it out
        data = f.read()  # read the rest
        f.seek(0)  # set the cursor to the top of the file
        f.write(data)  # write the data back
        f.truncate()  # set the file size to the current size
        return first_line.strip()
