import argparse
import requests
import sys
from bs4 import BeautifulSoup
from typing import Optional, cast
from dataclasses import dataclass
from ebooklib import epub

@dataclass
class StoryMetadata:
    title: str
    author: str
    cover_url: Optional[str]

@dataclass
class Chapter:
    title: str
    content: str

def fetch_html(url: str) -> Optional[str]:
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        sys.stderr.write(f"Failed to fetch HTML content of {url}: {e}\n")
        return None

def fetch_cover_image(url: str) -> Optional[bytes]:
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.content
    except requests.exceptions.RequestException as e:
        sys.stderr.write(f"Failed to fetch story cover image from {url}: {e}\n")
        return None

def extract_story_metadata(soup: BeautifulSoup) -> Optional[StoryMetadata]:
    title = soup.select_one("div.fic-header > div.fic-title h1")
    if not title:
        sys.stderr.write(f"Failed to find story Title\n")
        return None
    title = title.text

    author = soup.select_one("div.fic-header > div.fic-title h4 a")
    if not author:
        sys.stderr.write(f"Failed to find story Author\n")
        return None
    author = author.text

    cover_url = soup.select_one("div.fic-header > div.cover-col > div.cover-art-container img")
    cover_url = cast(str, cover_url['src']) if cover_url else None

    return StoryMetadata(title=title, author=author, cover_url=cover_url)

def extract_chapter_links(soup: BeautifulSoup) -> list[str]:
    chapter_links: list[str] = []

    for chapter_link in soup.select("table#chapters tr.chapter-row > td:first-child a"):
        chapter_link = cast(str, chapter_link['href'])
        chapter_links.append(chapter_link)

    return chapter_links

def fetch_chapters(chapter_links: list[str]) -> Optional[list[Chapter]]:
    chapters: list[Chapter] = []
    chapter_count = len(chapter_links)

    for index, chapter_link in enumerate(chapter_links):
        print(f"Downloading chapter {index+1}/{chapter_count}", end='\r', flush=True)
        chapter_url = f"https://www.royalroad.com{chapter_link}"
        chapter_html = fetch_html(chapter_url)
        if not chapter_html:
            sys.stderr.write("Failed to fetch chapter HTML")
            return None

        soup = BeautifulSoup(chapter_html, 'html.parser')

        title = soup.select_one("div.fic-header h1")
        if not title:
            sys.stderr.write(f"Failed to find chapter Title\n")
            return None
        title = title.text

        content = soup.select_one("div.chapter-content")
        if not content:
            sys.stderr.write(f"Failed to find chapter Content\n")
            return None
        content = content.text

        chapters.append(Chapter(title=title, content=content))

    print(f"Downloaded {chapter_count} chapters".ljust(50))

    return chapters

def build_epub(metadata: StoryMetadata, chapters: list[Chapter]) -> str:
    book = epub.EpubBook()

    book.set_title(metadata.title)
    book.set_language('en')
    book.add_author(metadata.author)

    if metadata.cover_url:
        cover_image = fetch_cover_image(metadata.cover_url)
        if cover_image:
            book.set_cover('cover.jpg', cover_image)

    toc: list[epub.EpubHtml] = []
    spine: list[str | epub.EpubHtml] = ['nav']

    for index, chapter in enumerate(chapters):
        c = epub.EpubHtml(title=chapter.title, file_name=f'{index+1}{chapter.title.replace(" ","_")}.xhtml', lang='en')
        c.set_content(f"<h1>{chapter.title}</h1>{chapter.content}")
        book.add_item(c)
        toc.append(c)
        spine.append(c)

    book.toc = toc
    book.spine = spine

    style = 'body { font-family: Times, Times New Roman, serif; }'
    nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style.encode())
    book.add_item(nav_css)

    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    file_name = f"{metadata.title.replace(" ", "_")}.epub"
    epub.write_epub(file_name, book)
    return file_name

def main():
    parser = argparse.ArgumentParser(prog='royalroad2epub', description='Scrape RoyalRoad story and produce EPUB')
    parser.add_argument('url', help='RoyalRoady story URL')
    args = parser.parse_args()

    story_url = args.url

    print(f"Fetch HTML of {story_url}")
    story_html = fetch_html(story_url)
    if not story_html:
        print("Failed to fetch story HTML")
        return

    print("Extracting metadata")
    soup = BeautifulSoup(story_html, 'html.parser')
    story_metadata = extract_story_metadata(soup)
    if not story_metadata:
        print("Failed to extract story metadata")
        return

    print("Extracting chapter links")
    chapter_links = extract_chapter_links(soup)
    if len(chapter_links) == 0:
        print("Failed to extract chapter links")
        return
    print(f"Found {len(chapter_links)} chapter links")

    chapters = fetch_chapters(chapter_links)
    if not chapters:
        print("Failed to fetch chapters")
        return

    file_name = build_epub(story_metadata, chapters)
    print(f"Saved story as {file_name}")

if __name__ == "__main__":
    main()
