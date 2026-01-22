import asyncio
import json
import logging
from urllib.parse import urljoin, urlparse

import httpx
from bs4 import BeautifulSoup

# Configuration
BASE_URL = "https://cs50.harvard.edu/"
COURSE_SLUGS = ["x", "ai", "python", "r", "sql", "web"]
CONCURRENCY_LIMIT = 5
MAX_RETRIES = 3

# Setup Logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


class CS50Scraper:
    def __init__(self):
        self.semaphore = asyncio.Semaphore(CONCURRENCY_LIMIT)
        self.client = httpx.AsyncClient(follow_redirects=True, timeout=20.0)
        self.results = []

    async def fetch_with_retry(self, url):
        """Fetches a URL with a 3-retry logic for failures."""
        for attempt in range(MAX_RETRIES + 1):
            try:
                async with self.semaphore:
                    response = await self.client.get(url)

                if response.status_code == 404:
                    return None  # Signal resource not found

                response.raise_for_status()
                return response
            except (httpx.HTTPError, httpx.ConnectError) as e:
                if attempt == MAX_RETRIES:
                    logger.error(
                        f"Failed to fetch {url} after {MAX_RETRIES} retries: {e}"
                    )
                    return None
                await asyncio.sleep(1 * (attempt + 1))  # Exponential backoff

    def is_valid_sublink(self, href):
        """Phase 5: Filter criteria for problem sub-links."""
        if not href or href.startswith(("#", ".", "..")):
            return False
        # Check if it's an absolute external URL
        parsed = urlparse(href)
        if parsed.scheme or parsed.netloc:
            return False
        return True

    def extract_commands(self, html_content):
        """Phase 6: Command extraction logic with H2 and Code block constraints."""
        soup = BeautifulSoup(html_content, "html.parser")
        commands = []

        # Target headers
        target_headers = ["How to Begin", "Distribution Code", "Getting Started"]

        # Find all h2 tags
        headers = soup.find_all("h2")
        for i, h2 in enumerate(headers):
            if any(target in h2.get_text() for target in target_headers):
                # Look at elements between this H2 and the next H2
                current_node = h2.next_sibling
                while current_node and current_node.name != "h2":
                    if current_node.name == "code":
                        # Condition: No class, no '$'
                        if (
                            not current_node.has_attr("class")
                            and "$" not in current_node.get_text()
                        ):
                            cmd = current_node.get_text(strip=True)
                            if cmd:
                                commands.append(cmd)
                    # Also look for code blocks inside other elements (like <p> or <li>)
                    elif hasattr(current_node, "find_all"):
                        for code in current_node.find_all("code", recursive=True):
                            if (
                                not code.has_attr("class")
                                and "$" not in code.get_text()
                            ):
                                cmd = code.get_text(strip=True)
                                if cmd:
                                    commands.append(cmd)
                    current_node = current_node.next_sibling
        return commands

    async def process_subproblem(self, url, relative_path):
        """Phase 6 & 7: Extract data from individual problem pages."""
        response = await self.fetch_with_retry(url)
        if not response:
            return

        cmds = self.extract_commands(response.text)
        cmds = clean_commands(cmds)

        if cmds:
            self.results.append({"id": relative_path, "commands": cmds})

    async def process_problem_set(self, slug, year, fmt, index):
        """Phase 5: Enumerate sub-problems within a pset/project index."""
        base_pset_url = f"{BASE_URL}{slug}/{year}/{fmt}/{index}/"
        response = await self.fetch_with_retry(base_pset_url)

        if not response:
            return False  # Stop signal for Phase 4 enumeration

        soup = BeautifulSoup(response.text, "html.parser")
        anchors = soup.find_all("a", href=True)

        tasks = []
        for a in anchors:
            href = a["href"]
            if self.is_valid_sublink(href):
                sub_url = urljoin(base_pset_url, href)
                rel_path = f"{slug}/{year}/{fmt}/{index}/{href}"
                tasks.append(self.process_subproblem(sub_url, rel_path))

        if tasks:
            await asyncio.gather(*tasks)
        return True

    async def run(self):
        for slug in COURSE_SLUGS:
            logger.info(f"Processing course: {slug}")

            # Phase 1 & 2: Course and Year Discovery
            for year in range(2026, 2006, -1):
                year_url = f"{BASE_URL}{slug}/{year}/"
                year_resp = await self.fetch_with_retry(year_url)

                if not year_resp:
                    continue

                logger.info(f"  Found year: {year}")

                # Phase 3: Pset vs Project Detection
                format_found = None
                for fmt in ["psets", "projects"]:
                    fmt_url = f"{BASE_URL}{slug}/{year}/{fmt}/"
                    fmt_resp = await self.fetch_with_retry(fmt_url)
                    if fmt_resp:
                        format_found = fmt
                        break

                if not format_found:
                    continue

                # Phase 4: Enumeration
                idx = 0
                while True:
                    success = await self.process_problem_set(
                        slug, year, format_found, idx
                    )
                    if not success:
                        break
                    idx += 1

                # Phase 8.6: Persist after each course-year combination
                self.save_data()

    def save_data(self):
        with open("after.json", "w") as f:
            json.dump(self.results, f, indent=2)
        logger.info(f"Data persisted to data.json ({len(self.results)} entries)")


async def main():
    scraper = CS50Scraper()
    try:
        await scraper.run()
    finally:
        await scraper.client.aclose()


def clean_commands(commands: list[str]) -> list[str]:
    """
    Filter commands to only keep the actual setup sequence.
    Stops at the first command that isn't part of the standard workflow.
    """
    if not commands:
        return []

    # Valid command prefixes for setup
    valid_prefixes = ("wget ", "unzip ", "rm ", "cd ", "ls", "mkdir ", "code ")

    cleaned = []

    for cmd in commands:
        # Stop if we hit a command that's not part of setup
        if not cmd.startswith(valid_prefixes):
            break

        # Keep valid commands
        cleaned.append(cmd)

        # If we hit 'ls', stop (next items are file listings)
        if cmd.strip() == "ls":
            break

    return cleaned


if __name__ == "__main__":
    asyncio.run(main())
