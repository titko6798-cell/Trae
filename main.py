import sys
import urllib.request
import urllib.error
from html.parser import HTMLParser

class LinkHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.title = []
        self._in_title = False
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for k, v in attrs:
                if k == 'href' and v:
                    self.links.append(v)
        if tag == 'title':
            self._in_title = True
    def handle_endtag(self, tag):
        if tag == 'title':
            self._in_title = False
    def handle_data(self, data):
        if self._in_title:
            self.title.append(data)
    def get_title(self):
        return ''.join(self.title).strip() or None

def crawl(url: str, timeout: float = 10.0, max_bytes: int = 1048576):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 TraeCrawler'})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            content_type = resp.headers.get('Content-Type', '')
            charset = resp.headers.get_content_charset() or 'utf-8'
            raw = resp.read(max_bytes)
            html = raw.decode(charset, errors='replace')
    except urllib.error.HTTPError as e:
        return {'url': url, 'status': e.code, 'content_type': None, 'title': None, 'links': []}
    except Exception:
        return {'url': url, 'status': None, 'content_type': None, 'title': None, 'links': []}
    parser = LinkHTMLParser()
    parser.feed(html)
    return {'url': url, 'status': 200, 'content_type': content_type, 'title': parser.get_title(), 'links': parser.links}

if __name__ == '__main__':
    target = sys.argv[1] if len(sys.argv) > 1 else 'https://example.com'
    result = crawl(target)
    print(result['title'] if result['title'] else '')
    print(len(result['links']))
    if result['links']:
        for l in result['links'][:10]:
            print(l)
