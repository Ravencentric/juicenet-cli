from colorama import Fore

from .compat import StrEnum

GREEN = Fore.GREEN
RESET = Fore.RESET


# fmt: off
class BarTitle(StrEnum):
    PARPAR = f"{GREEN}Processing Files{RESET}    | PARPAR   |"
    NYUU =   f"{GREEN}Uploading Files{RESET}     | NYUU     |"
    RAW =    f"{GREEN}Reposting Articles{RESET}  | NYUU     |"


class CurrentFile(StrEnum):
    PARPAR = f"{GREEN}Current File{RESET}        | PARPAR   |"
    NYUU =   f"{GREEN}Current File{RESET}        | NYUU     |"
    RAW =    f"{GREEN}Current Article{RESET}     | NYUU     |"
