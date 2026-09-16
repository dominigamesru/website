"""Show changes in VISIBLE TEXT of the site's pages, ignoring markup/CSS.

Usage (from repo root):
    python .claude/skills/updating-site-content/text_diff.py [REV]

REV defaults to HEAD. Compares every tracked *.html page at REV with the
working tree. A pure layout change must print "no text changes".
Anything listed under "-" is text that was removed or altered.
"""
import difflib
import re
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path

BLOCK_TAGS = {
    "p", "div", "li", "ul", "ol", "tr", "td", "th", "table", "h1", "h2", "h3",
    "h4", "h5", "h6", "section", "header", "footer", "main", "br", "title",
    "blockquote", "dd", "dt", "article", "nav",
}
SKIP_TAGS = {"style", "script", "head"}
TEXT_ATTRS = ("alt", "title", "content")  # meta description, img alt


class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.lines, self.buf, self.skip = [], [], 0

    def flush(self):
        text = re.sub(r"\s+", " ", "".join(self.buf)).strip()
        if text:
            self.lines.append(text)
        self.buf = []

    def handle_starttag(self, tag, attrs):
        if tag in SKIP_TAGS:
            self.skip += 1
        if tag in BLOCK_TAGS:
            self.flush()
        for name, value in attrs:
            # meta description and alt texts are content too
            if value and name in TEXT_ATTRS and (tag != "meta" or ("name", "description") in attrs):
                self.lines.append(f"[{tag} {name}] {value.strip()}")

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)

    def handle_endtag(self, tag):
        if tag in SKIP_TAGS:
            self.skip = max(0, self.skip - 1)
        if tag in BLOCK_TAGS:
            self.flush()

    def handle_data(self, data):
        if not self.skip:
            self.buf.append(data)


def extract(html):
    p = TextExtractor()
    p.feed(html)
    p.flush()
    return p.lines


def git(*args):
    return subprocess.run(["git", *args], capture_output=True, check=False).stdout.decode("utf-8")


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    rev = sys.argv[1] if len(sys.argv) > 1 else "HEAD"
    pages = sorted(set(git("ls-files", "*.html").split()) | set(git("ls-files", "--others", "--exclude-standard", "*.html").split()))
    changed = False
    for page in pages:
        old = extract(git("show", f"{rev}:{page}"))
        new = extract(Path(page).read_text(encoding="utf-8")) if Path(page).exists() else []
        diff = list(difflib.unified_diff(old, new, f"{rev}:{page}", page, n=1, lineterm=""))
        if diff:
            changed = True
            print("\n".join(diff), end="\n\n")
    if not changed:
        print("no text changes")


if __name__ == "__main__":
    main()
