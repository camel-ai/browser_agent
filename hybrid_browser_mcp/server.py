#!/usr/bin/env python3

import logging
from hybrid_browser_mcp.router import mcp

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def main():
    mcp.run("stdio")
    return 0


if __name__ == "__main__":
    main()