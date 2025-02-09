from scholarly import scholarly
from bs4 import BeautifulSoup

# Your Google Scholar ID
SCHOLAR_ID = "tQY3ijcAAAAJ"

def format_authors(author_str):
    """Formats author names in APA style (Last, F. M.)."""
    authors = author_str.split(", ")
    formatted_authors = []
    
    for author in authors:
        parts = author.split()
        if len(parts) > 1:
            last_name = parts[-1]
            initials = " ".join([f"{name[0]}." for name in parts[:-1]])
            formatted_authors.append(f"{last_name}, {initials}")
        else:
            formatted_authors.append(author)  # Handle unexpected format

    return ", ".join(formatted_authors)

def fetch_publications(scholar_id):
    """Fetches and sorts publications from Google Scholar by year (descending)."""
    author = scholarly.search_author_id(scholar_id)
    scholarly.fill(author, sections=["publications"])  
    
    publications = []
    for pub in author.get("publications", []):
        pub_details = scholarly.fill(pub)  
        
        title = pub_details["bib"].get("title", "Unknown Title")
        authors = pub_details["bib"].get("author", "Unknown Authors")
        formatted_authors = format_authors(authors)
        year = str(pub_details["bib"].get("pub_year", "0000"))  # Ensure it's a string
        journal = pub_details["bib"].get("venue", "Unknown Journal")
        link = pub_details.get("pub_url", "")

        link_html = f'<a href="{link}" target="_blank">{link}</a>' if link else "N/A"

        publications.append({
            "title": title,
            "authors": formatted_authors,
            "year": int(year) if year.isdigit() else 0,  # Convert to int only if valid
            "journal": journal,
            "link": link_html
        })
    
    # Sort by year in descending order (most recent first)
    publications.sort(key=lambda x: x["year"], reverse=True)

    return publications

def generate_html(publications):
    """Generates an HTML file listing all publications in APA style, sorted by year."""
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
    h1.string = "Publications (Sorted by Year)"
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

    print("HTML file generated: publications.html (Sorted by Year)")
