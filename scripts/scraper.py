import asyncio
import json

import httpx
from bs4 import BeautifulSoup

# Configuration
BASE_URL = "https://cs50.harvard.edu"
COURSE_SLUGS = ["x", "ai", "python", "r", "sql", "web"]
CONCURRENCY_LIMIT = 5
MAX_RETRIES = 3
YEARS = list(range(2026, 2006, -1))

semaphore = asyncio.Semaphore(CONCURRENCY_LIMIT)


async def fetch(client, url, follow_redirects=True):
    """Fetch URL with retry logic and concurrency control."""
    for attempt in range(MAX_RETRIES):
        try:
            async with semaphore:
                response = await client.get(url, follow_redirects=follow_redirects)
                if response.status_code == 404:
                    return None
                response.raise_for_status()
                return response
        except (httpx.HTTPStatusError, httpx.RequestError):
            if attempt == MAX_RETRIES - 1:
                return None
            await asyncio.sleep(1)
    return None


def parse_code_snippets(soup):
    """Filters code blocks based on Phase 6 criteria."""
    snippets = []
    valid_starts = ("wget ", "unzip ", "rm ", "cd ", "ls", "mkdir ", "code ")

    for code in soup.find_all("code"):
        text = code.get_text().strip()
        # Filter: No '$', must start with valid commands
        if "$" not in text and text.startswith(valid_starts):
            snippets.append(text)
    return snippets


async def scrape_problem(client, course, year, type_slug, index, problem_slug):
    """Phase 6: Scrape code examples from a specific problem page."""
    url = f"{BASE_URL}/{course}/{year}/{type_slug}/{index}/{problem_slug}/"
    resp = await fetch(client, url)
    if not resp:
        return None

    soup = BeautifulSoup(resp.text, "html.parser")
    snippets = parse_code_snippets(soup)

    if not snippets:
        return None

    # Logic for storage: String if wget, else List
    commands = snippets[0] if snippets[0].startswith("wget") else snippets

    return {
        "name": problem_slug,
        "data": {
            "c": commands,
            "e": f"{course}/{year}/{type_slug}/{index}/{problem_slug}",
        },
    }


async def process_course_year(client, course, year, results):
    """Phases 3-5: Identify type, enumerate indices, and find problems."""
    # Phase 3: Identify Type
    type_slug = None
    for t in ["psets", "projects"]:
        if await fetch(client, f"{BASE_URL}/{course}/{year}/{t}/"):
            type_slug = t
            break

    if not type_slug:
        return

    # Phase 4 & 5: Index Loop and Problem Discovery
    index = 0
    while True:
        index_url = f"{BASE_URL}/{course}/{year}/{type_slug}/{index}/"
        resp = await fetch(client, index_url)
        if not resp:
            break

        soup = BeautifulSoup(resp.text, "html.parser")
        problem_links = []

        # Filter Criteria Phase 5.3
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if (
                not any(href.startswith(x) for x in ["/", "http", "https", "#", "."])
                and "#" not in href
            ):
                problem_links.append(href.strip("/"))

        # Phase 6: Scrape each problem found
        tasks = [
            scrape_problem(client, course, year, type_slug, index, p)
            for p in problem_links
        ]
        problem_results = await asyncio.gather(*tasks)

        for res in problem_results:
            if res:
                name = res["name"]
                if name not in results:
                    results[name] = {"d": str(year)}
                results[name][str(year)] = res["data"]
                # Update default year to the most recent found
                if int(year) > int(results[name]["d"]):
                    results[name]["d"] = str(year)

        index += 1


async def main():
    results = {}
    async with httpx.AsyncClient(timeout=10.0) as client:
        # Phase 1: Filter valid course base URLs
        valid_courses = []
        for slug in COURSE_SLUGS:
            if await fetch(client, f"{BASE_URL}/{slug}/"):
                valid_courses.append(slug)

        # Phase 2: Year Discovery and processing
        for course in valid_courses:
            print(f"Scraping Course: {course}")
            for year in YEARS:
                # Check if year exists for course
                if await fetch(client, f"{BASE_URL}/{course}/{year}/"):
                    await process_course_year(client, course, year, results)

    # Output to JSON
    with open("scraped_data.json", "w") as f:
        json.dump(results, f, indent=2)
    print("Scraping complete. Data saved to scraped_data.json")


if __name__ == "__main__":
    asyncio.run(main())
