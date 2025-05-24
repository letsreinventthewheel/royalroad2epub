# 📚 RoyalRoad to EPUB Converter

A Python-based tool that scrapes RoyalRoad stories and converts them into `.epub` files – perfect for offline reading on your e-reader.

![YouTube Video](https://img.shields.io/badge/Watch%20on-YouTube-red?logo=youtube)

> 🔗 [Watch the full walkthrough on YouTube](https://www.youtube.com/watch?v=nm1U4KzlfOY)

---

## ✨ What It Does

This script takes the URL of a RoyalRoad story and downloads all of its chapters into a clean, well-formatted EPUB file. It’s fast, customizable, and lightweight — ideal for turning your favorite serialized web fiction into a portable reading experience.

---

## 📦 Features

- Scrapes story title, author, and metadata
- Fetches all chapter content automatically
- Generates `.epub` files compatible with most e-readers
- Minimal dependencies, easy to extend

---

## 🧰 Technologies Used

- `requests` – to fetch RoyalRoad pages
- `BeautifulSoup` – for HTML parsing and data extraction
- `EbookLib` – to create the final EPUB file

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/letsreinventthewheel/royalroad2epub.git
cd royalroad2epub
```

### 2. Install Dependencies

Use `pip` to install the required Python libraries:

```bash
pip install -r requirements.txt
```

_Or manually:_

```bash
pip install requests beautifulsoup4 ebooklib
```

### 3. Run the Script

```bash
python royalroad2epub.py "https://www.royalroad.com/fiction/21220/mother-of-learning"
```

Replace the URL with the RoyalRoad story you want to convert.

---

## 📝 Example Output

Once complete, you’ll get a file like:

```
📘 Mother_of_Learning.epub
```

Ready to be sideloaded into your Kindle, Kobo, or other reader apps.

---

## 📺 Full Video Tutorial

Want a step-by-step guide? Check out the [YouTube video](https://www.youtube.com/watch?v=nm1U4KzlfOY) where we build this project from scratch and explain every step.

---

## 🛠️ Extend It

Some ideas for extending the script:

- Add argument (flag) to clean up Chapter name (remove numbering if present)
- Add argument (flag) to drop first paragraph of each chapter (applicable to some stories)
- Convert to PDF or MOBI
- Replace custom made download progress indicator with `tqdm`

---

## 💡 Who Is This For?

This project is aimed at beginner-to-intermediate Python developers who want to learn practical web scraping and content generation. It's a great way to build a useful tool while learning how to handle real-world HTML.

---

## 🙌 Acknowledgments

Inspired by the amazing stories on [RoyalRoad](https://www.royalroad.com/).
