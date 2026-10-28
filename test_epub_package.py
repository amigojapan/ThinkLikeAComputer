import tempfile
import unittest
from pathlib import Path
from zipfile import ZipFile
import xml.etree.ElementTree as ET

from bs4 import BeautifulSoup
from TLAC_boardgame.printables.epub_package import package_epub, XHTML, OPF
from TLAC_boardgame.printables.build_english_epub import validate


class EpubPackageTests(unittest.TestCase):
    def test_chapters_links_images_and_original_content(self):
        image = Path(__file__).parent / 'TLAC_boardgame/img/egg.png'
        with tempfile.TemporaryDirectory() as folder:
            work = Path(folder)
            destination = work / 'book.epub'
            document = BeautifulSoup(f'''<html><body>
<h1 id="intro">日本語の本</h1><p><a href="#final">次へ</a></p>
<div class="epub-html-chart" style="color: red"><p>命令 &amp; 値</p></div>
<img src="{image}" alt="卵"/>
<h2 id="final">最後</h2><pre>if x &lt; 3:\n    print("a &amp; b")</pre>
<img src="{image}" alt="卵"/><a href="#intro">戻る</a>
</body></html>''', 'html.parser')
            package_epub(destination, document, 'p { color: red; }', 'ja', '日本語の本', '目次', work)
            validate(destination, 'ja')
            with ZipFile(destination) as archive:
                docs = [ET.fromstring(archive.read(name)) for name in archive.namelist()
                        if name.startswith('EPUB/text/')]
                self.assertEqual(len(docs), 2)
                self.assertEqual(sum(1 for name in archive.namelist() if name.startswith('EPUB/media/')), 1)
                code = [node.text for doc in docs for node in doc.iter(f'{{{XHTML}}}pre')]
                self.assertEqual(code, ['if x < 3:\n    print("a & b")'])
                chart = next(node for doc in docs for node in doc.iter() if node.get('class') == 'epub-html-chart')
                self.assertEqual(chart.get('style'), 'color: red')
                package = ET.fromstring(archive.read('EPUB/content.opf'))
                spine = package.find(f'{{{OPF}}}spine')
                self.assertEqual(len(spine), len(docs))
                nav = ET.fromstring(archive.read('EPUB/nav.xhtml'))
                self.assertEqual(len(list(nav.iter(f'{{{XHTML}}}a'))), len(docs))

    def test_rejects_missing_anchor(self):
        with tempfile.TemporaryDirectory() as folder:
            work = Path(folder)
            document = BeautifulSoup('<html><body><h1>Book</h1><a href="#missing">Link</a></body></html>', 'html.parser')
            with self.assertRaisesRegex(ValueError, 'Unresolved EPUB anchor'):
                package_epub(work / 'book.epub', document, '', 'en', 'Book', 'Contents', work)
            self.assertFalse((work / 'book.epub').exists())


if __name__ == '__main__':
    unittest.main()
