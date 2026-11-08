from src.tools.tools import scrape_url, web_search, scrape_url

# output= web_search.invoke("recent advancements in AI")
# print(output)


url = "https://www.linkedin.com/top-content/innovation/ai-trends-and-innovations/recent-breakthroughs-in-ai-technology"

output= scrape_url.invoke(url)
print(output)