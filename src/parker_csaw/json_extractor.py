"""Tools for parsing JSON strings from blobs of text."""

from typing import Any
from collections.abc import Iterator
from dataclasses import dataclass

import orjson


@dataclass(kw_only=True)
class ParsedJson:
    """A parsed JSON object."""

    data: dict[str, Any] | list[Any]
    start_idx: int
    end_idx: int
    original_str: str


def extract_json_blobs(content: str) -> Iterator[ParsedJson]:
    """Extract JSON values from a string."""
    # Source: https://stackoverflow.com/a/64920157
    start_idx = 0
    while start_idx < len(content):
        if content[start_idx] == "{":
            for end_idx in range(len(content) - 1, start_idx, -1):
                if content[end_idx] == "}":
                    try:
                        data = orjson.loads(content[start_idx : end_idx + 1])
                        yield ParsedJson(
                            data=data,
                            start_idx=start_idx,
                            end_idx=end_idx + 1,
                            original_str=content[start_idx : end_idx + 1],
                        )
                        start_idx = end_idx
                        break
                    except orjson.JSONDecodeError:
                        pass
        start_idx += 1
