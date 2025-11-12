import argparse
import asyncio
import json
from pathlib import Path


async def main(start: int, end: int, output_path: Path):
    results = {
        "start": start,
        "end": end,
    }
    with open(output_path / f"{start}_{end}.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", type=int, required=True)
    parser.add_argument("--end", type=int, required=True)
    args = parser.parse_args()

    asyncio.run(main(args.start, args.end, Path(".") / "data"))
