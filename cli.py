"""Small CLI to run queries from the command line (prototype)."""

import argparse
from dygral import TemporalGraph, TemporalQueries
import examples.basic_example as ex


def main():
    parser = argparse.ArgumentParser(description="DyGraL CLI (prototype)")
    parser.add_argument("--example", action="store_true", help="Run built-in example")
    args = parser.parse_args()

    if args.example:
        ex.run_example()


if __name__ == '__main__':
    main()
