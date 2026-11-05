import argparse
import asyncio

from . import run


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("query")
    parser.add_argument("--max-results", type=int, default=15)
    args = parser.parse_args()

    for hit in asyncio.run(run(args.query, args.max_results)):
        print(f"{hit['title']}\n{hit['url']}\n{hit['snippet'] or ''}\n")


if __name__ == "__main__":
    main()
