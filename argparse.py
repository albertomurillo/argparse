import os
import sys


class ArgumentParser:
    """A minimal implementation of argparse.ArgumentParser for Python <= 2.2"""

    def __init__(self):
        self._namespace = Namespace()
        self._args = {}
        self._padding = 20
        self.add_argument("--help", help="show this help message and exit")

    def add_argument(self, arg, choices=None, default=None, required=False, help=""):
        self._args[arg] = {
            "name": self._argument_name(arg),
            "choices": choices or [],
            "required": required,
            "val": default,
            "help": help,
        }
        padding = len(arg)
        if choices:
            padding += len(str(choices)) + 4
        self._padding = max(self._padding, padding)

    def parse_args(self):
        self._parse_args()
        self._validate_args()
        for arg in self._args.values():
            setattr(self._namespace, arg["name"], arg["val"])
        return self._namespace

    def _parse_args(self):
        if len(sys.argv) == 1:
            return

        for i in range(1, len(sys.argv), 2):
            arg = sys.argv[i]
            if arg not in self._args:
                self.print_help()

            if arg == "--help":
                self.print_help()

            if i + 1 >= len(sys.argv):
                self.print_help()

            val = sys.argv[i + 1]
            self._args[arg]["val"] = val

    def _validate_args(self):
        for arg in self._args.values():
            val = arg["val"]
            choices = arg["choices"]
            required = arg["required"]

            if required and val is None:
                self.print_help()

            if val and choices and val not in choices:
                self.print_help()

    def _argument_name(self, arg):
        if arg[:2] != "--":
            raise NameError("argument name must start with --")
        if len(arg) <= 3:
            raise NameError("argument name cannot be empty")
        return arg[2:].replace("-", "_")

    def print_help(self):
        prog = os.path.basename(sys.argv[0])
        print("Usage: " + prog + " [OPTIONS]")
        print("")
        print("Options:")
        for k, v in self._args.items():
            s = []
            arg = k
            choices = v["choices"] or ""
            name = v["name"]
            help = v["help"]

            if choices:
                s.append(" ".join((arg, str(choices))).ljust(self._padding))
            elif arg == "--help":
                s.append(arg.ljust(self._padding))
            else:
                s.append(" ".join((arg, name.upper())).ljust(self._padding))
            if help:
                s.append(help)
            print(" ".join(s))
        sys.exit(1)


class Namespace:
    """A minimal implementation of argparse.Namespace for Python <= 2.2"""
