from __future__ import annotations


class Colors:
    RESET = "\033[0m"
    CYAN = "\033[36m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    RED = "\033[31m"
    MAGENTA = "\033[35m"
    BLUE = "\033[34m"
    WHITE = "\033[37m"
    BOLD = "\033[1m"


STATE_COLOR = {
    "THINKING": Colors.CYAN,
    "HUNGRY": Colors.YELLOW,
    "WAITING": Colors.MAGENTA,
    "EATING": Colors.GREEN,
    "RELEASING": Colors.BLUE,
}
