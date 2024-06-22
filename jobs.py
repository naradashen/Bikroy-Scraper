import httpx
from bs4 import BeautifulSoup

async def fetch_html(url):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            response.raise_for_status()  # Raise exception for 4xx/5xx errors
            return response.content
        except httpx.HTTPStatusError as e:
            print(f"HTTP error occurred: {e}")
        except Exception as e:
            print(f"Error fetching URL: {e}")

async def scrape_bikroy_page(url):
    html_content = await fetch_html(url)
    if not html_content:
        return []

    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all listings on the page
    listings = soup.find_all('div', class_='content--3JNQz')

    results = []

    for listing in listings:
        title_elem = listing.find('h2', class_='heading--2eONR heading-2--1OnX8 title--3yncE block--3v-Ow')
        location_elem = listing.find('div', class_='description--2-ez3')
        price_elem = listing.find('div', class_='price--3SnqI color--t0tGX')
        updated_time_elem = listing.find('div', class_='updated-time--1DbCk')

        if title_elem and location_elem and price_elem and updated_time_elem:
            title = title_elem.text.strip()
            location = location_elem.text.strip()
            price = price_elem.span.text.strip()
            updated_time = updated_time_elem.text.strip()

            item = {
                'title': title,
                'location': location,
                'price': price,
                'updated_time': updated_time
            }
            results.append(item)

    return results

async def main():
    base_url = 'https://bikroy.com/en/ads/bangladesh/jobs?sort=date&order=desc&buy_now=0&urgent=0&page='

    total_items = 0

    for page in range(1, 41):  # Pages 1 to 40
        url = f"{base_url}{page}"
        print(f"\n........................................ Scraping page {page} .....................................................\n")
        items = await scrape_bikroy_page(url)
        total_items += len(items)
        
        for idx, item in enumerate(items, start=1):
            print(f"Item {idx} | {item['title']} | {item['location']} | {item['price']} | {item['updated_time']}")

    print(f"Total scraped data: {total_items} items")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
