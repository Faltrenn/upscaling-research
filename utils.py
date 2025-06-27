from typing import Callable


class MissingNecessaryflags(Exception):
    def __init__(self, flags: list[str]) -> None:
        self.flags = flags
        super().__init__(f"Missing some necessary flags: {flags}")


def get_and_check_flags(argv: list[str], necessary_flags: tuple[str, ...], error_function: Callable) -> dict[str, list[str]]:
    flags: dict[str, list[str]] = {}

    flag = ""
    for arg in argv:
        if len(arg) > 1 and arg.startswith("-"):
            flag = arg
            flags[flag] = []
            continue

        if flag:
            flags[flag].append(arg)

    keys = flags.keys()

    flags_missing = [flag for flag in necessary_flags if flag in keys]

    if not flags_missing:
        error_function()
        raise MissingNecessaryflags(flags_missing)

    return flags
