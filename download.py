import requests
import os
import time

# Search terms to look for in the page content
search_terms = ['Brazil', 'Brasil', 'Brazilian', 'Brasilian', 'Brasilia']

# Output folder
output_folder = 'brazil_wikipedia_articles'
os.makedirs(output_folder, exist_ok=True)

# Base URL for the MediaWiki API
API_URL = "https://en.wikipedia.org/w/api.php"

headers = {
    'User-Agent': 'BrazilWikipediaDownloader/1.0)'
}

def search_pages(term, limit=50):
    """Search Wikipedia pages by content mentioning a term."""
    pages = []
    params = {
        "action": "query",
        "format": "json",
        "list": "search",
        "srsearch": term,
        "srlimit": limit
    }

    while True:
        try:
            response = requests.get(API_URL, params=params, headers=headers)
            response.raise_for_status()  # Raise an exception for HTTP errors
            data = response.json()

            # Check if 'query' key is in the response
            if 'query' not in data:
                print(f"Error: No 'query' in response for term '{term}'. Response: {data}")
                break

            z = 0
            for item in data['query']['search']:
                if item['title'] in pages: continue
                z = 1
                pages.append(item['title'])
            if z == 0: return
            print("\t", len(pages))

            # Check for continuation
            if 'continue' in data:
                params.update(data['continue'])
            else:
                break
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            break
        except requests.exceptions.JSONDecodeError:
            print(f"Failed to decode JSON response from Wikipedia. Response text: {response.text}")
            break
        except:
            break

    print("Number of pages:", len(pages))
    return pages

def download_page(title):
    """Download the full content of a Wikipedia page."""
    params = {
        "action": "query",
        "prop": "extracts",
        "explaintext": True,
        "titles": title,
        "format": "json"
    }
    filename = f"{title.replace(' ', '_').replace('/', '_')}.txt"
    filepath = os.path.join(output_folder, filename)

    if os.path.isfile(filepath): return 0

    response = requests.get(API_URL, params=params, headers=headers)
    data = response.json()
    page = next(iter(data['query']['pages'].values()))

    if "missing" in page:
        print(f"Page '{title}' not found.")
        return 1

    content = page.get("extract", "")\

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Saved: {filename}")
    return 1

def main():
    downloaded = set()
    all_titles = set()
    for term in search_terms:
        print(f"Searching for pages mentioning: {term}")
        titles = search_pages(term)
        for title in titles:
            all_titles.add(title)
    print("All titles:", len(all_titles))
    for title in all_titles:
        if title not in downloaded:  # Avoid duplicates
            download = download_page(title)
            downloaded.add(title)
            if download: time.sleep(0.5)  # Be polite to Wikipedia API

if __name__ == "__main__":
    main()