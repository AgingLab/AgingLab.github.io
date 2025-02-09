from scholarly import scholarly
from bs4 import BeautifulSoup

# Your Google Scholar ID
SCHOLAR_ID = "tQY3ijcAAAAJ"

def fetch_publications(scholar_id):
    """Fetches publications from Google Scholar."""
    author = scholarly.search_author_id(scholar_id)  # Fetch author profile (returns a dictionary)
    scholarly.fill(author, sections=["publications"])  # Get full details
    
    publications = []
    for pub in author.get("publications", []):
        pub_details = scholarly.fill(pub)  # Fetch full details of each publication
        
        title = pub_details["bib"].get("title", "Unknown Title")
        authors = pub_details["bib"].get("author", "Unknown Authors")
        year = pub_details["bib"].get("pub_year", "Unknown Year")
        journal = pub_details["bib"].get("venue", "Unknown Journal")
        link = pub_details.get("pub_url", "")

        link_html = f'<a href="{link}" target="_blank">{link}</a>' if link else "N/A"

        publications.append({
            "title": title,
            "authors": authors,
            "year": year,
            "journal": journal,
            "link": link_html
        })
    
    return publications

def generate_html(publications):
    """Generates an HTML file listing all publications in APA style."""
    html = BeautifulSoup(features="html.parser")

    # Create HTML structure
    html.append(html.new_tag("html"))
    head = html.new_tag("head")
    html.html.append(head)
    title = html.new_tag("title")
    title.string = "Publications - Yashar Zeighami"
    head.append(title)
    
    body = html.new_tag("body")
    html.html.append(body)
    
    h1 = html.new_tag("h1")
    h1.string = "Publications"
    body.append(h1)

    ol = html.new_tag("ol")
    body.append(ol)

    for pub in publications:
        li = html.new_tag("li")
        li.string = f"{pub['authors']} ({pub['year']}). {pub['title']}. {pub['journal']}. {pub['link']}"
        ol.append(li)

    return html.prettify()

if __name__ == "__main__":
    publications = fetch_publications(SCHOLAR_ID)
    html_content = generate_html(publications)

    # Save to an HTML file
    with open("publications.html", "w", encoding="utf-8") as f:
        f.write(html_content)

    print("HTML file generated: publications_raw.html")
