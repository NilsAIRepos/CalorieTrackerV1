"""Search engine wrapper for online nutritional lookups."""

from duckduckgo_search import DDGS

def search_nutrition(query: str, max_results: int = 3) -> list[str]:
    """
    Search DuckDuckGo for nutritional information.

    Args:
        query: The food item to search for (e.g., "nutrition facts fried egg").
        max_results: Number of results to return.

    Returns:
        A list of string snippets from the search results.
    """
    # Add keywords to ensure we get nutritional info
    if "nutrition" not in query.lower():
        search_query = f"{query} nutrition facts"
    else:
        search_query = query

    try:
        results = DDGS().text(search_query, max_results=max_results)
        snippets = []
        if results:
            for r in results:
                title = r.get('title', '')
                body = r.get('body', '')
                snippets.append(f"Title: {title}\nSnippet: {body}")
        return snippets
    except Exception as e:
        print(f"Search error: {e}")
        return []

if __name__ == "__main__":
    # Simple test
    print("Searching for 'boiled egg'...")
    res = search_nutrition("boiled egg")
    for s in res:
        print("-" * 20)
        print(s)
