"""Package prepared lesson HTML as EPUB without a whole-book converter AST."""
from datetime import datetime, timezone
from hashlib import sha256
from html import escape
import mimetypes
from pathlib import Path
from urllib.parse import unquote, urlsplit
from uuid import NAMESPACE_URL, uuid5
from zipfile import ZipFile, ZIP_DEFLATED, ZIP_STORED
import xml.etree.ElementTree as ET

XHTML = 'http://www.w3.org/1999/xhtml'
OPF = 'http://www.idpf.org/2007/opf'
DC = 'http://purl.org/dc/elements/1.1/'
EPUB = 'http://www.idpf.org/2007/ops'


def xml_bytes(tree):
    return ET.tostring(tree, encoding='utf-8', xml_declaration=True)


def package_epub(destination, document, css, language, title, toc_title, work):
    """Split at exposed headings, resolve anchors, and bundle local assets.

    Only one chapter is parsed as XML at a time. Chapter files on disk allow a
    second pass to resolve forward links without retaining a second book tree.
    """
    ET.register_namespace('', XHTML)
    ET.register_namespace('epub', EPUB)
    chapters, anchors, images, image_sources = [], {}, {}, {}
    nodes, heading = [], title

    def flush():
        nonlocal nodes
        if not nodes:
            return
        name = f'ch{len(chapters) + 1:04d}.xhtml'
        text = ''.join(str(node) for node in nodes)
        if not text.strip():
            nodes = []
            return
        tree = ET.fromstring(
            f'<html xmlns="{XHTML}" lang="{language}" xml:lang="{language}">'
            f'<head><title>{escape(heading)}</title>'
            '<link rel="stylesheet" type="text/css" href="../styles/book.css"/>'
            '<meta charset="utf-8"/></head><body>' + text + '</body></html>')
        for node in tree.iter():
            identifier = node.get('id')
            if identifier:
                if identifier in anchors:
                    raise ValueError('Duplicate EPUB anchor: ' + identifier)
                anchors[identifier] = name
            if node.tag == f'{{{XHTML}}}img':
                source = Path(node.attrib['src']).resolve()
                if source not in image_sources:
                    data = source.read_bytes()
                    target = 'image-' + sha256(data).hexdigest()[:20] + source.suffix.lower()
                    image_sources[source] = target
                    images.setdefault(target, source)
                node.set('src', '../media/' + image_sources[source])
        (work / name).write_bytes(xml_bytes(tree))
        chapters.append((name, heading))
        nodes = []

    for node in document.body.contents:
        if getattr(node, 'name', None) in ('h1', 'h2'):
            flush()
            heading = node.get_text(' ', strip=True)
        nodes.append(node)
    flush()
    if not chapters:
        raise ValueError('Cannot package an empty EPUB')

    nav = ET.Element(f'{{{XHTML}}}html', {'lang': language, '{http://www.w3.org/XML/1998/namespace}lang': language})
    head = ET.SubElement(nav, f'{{{XHTML}}}head')
    ET.SubElement(head, f'{{{XHTML}}}title').text = toc_title
    body = ET.SubElement(nav, f'{{{XHTML}}}body')
    toc = ET.SubElement(body, f'{{{XHTML}}}nav', {f'{{{EPUB}}}type': 'toc', 'id': 'toc'})
    ET.SubElement(toc, f'{{{XHTML}}}h1').text = toc_title
    listing = ET.SubElement(toc, f'{{{XHTML}}}ol')
    for name, chapter_title in chapters:
        item = ET.SubElement(listing, f'{{{XHTML}}}li')
        ET.SubElement(item, f'{{{XHTML}}}a', {'href': 'text/' + name}).text = chapter_title

    package = ET.Element(f'{{{OPF}}}package', {'version': '3.0', 'unique-identifier': 'book-id', '{http://www.w3.org/XML/1998/namespace}lang': language})
    metadata = ET.SubElement(package, f'{{{OPF}}}metadata')
    ET.SubElement(metadata, f'{{{DC}}}identifier', {'id': 'book-id'}).text = 'urn:uuid:' + str(uuid5(NAMESPACE_URL, title + ':' + language))
    ET.SubElement(metadata, f'{{{DC}}}title').text = title
    ET.SubElement(metadata, f'{{{DC}}}language').text = language
    ET.SubElement(metadata, f'{{{OPF}}}meta', {'property': 'dcterms:modified'}).text = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    manifest = ET.SubElement(package, f'{{{OPF}}}manifest')
    spine = ET.SubElement(package, f'{{{OPF}}}spine')
    ET.SubElement(manifest, f'{{{OPF}}}item', {'id': 'nav', 'href': 'nav.xhtml', 'media-type': 'application/xhtml+xml', 'properties': 'nav'})
    ET.SubElement(manifest, f'{{{OPF}}}item', {'id': 'style', 'href': 'styles/book.css', 'media-type': 'text/css'})
    for index, (name, _) in enumerate(chapters, 1):
        identifier = f'chapter-{index}'
        ET.SubElement(manifest, f'{{{OPF}}}item', {'id': identifier, 'href': 'text/' + name, 'media-type': 'application/xhtml+xml'})
        ET.SubElement(spine, f'{{{OPF}}}itemref', {'idref': identifier})
    for index, name in enumerate(images, 1):
        ET.SubElement(manifest, f'{{{OPF}}}item', {'id': f'image-{index}', 'href': 'media/' + name, 'media-type': mimetypes.guess_type(name)[0] or 'application/octet-stream'})

    temporary = destination.with_suffix('.tmp.epub')
    with ZipFile(temporary, 'w', compression=ZIP_DEFLATED) as archive:
        archive.writestr('mimetype', 'application/epub+zip', compress_type=ZIP_STORED)
        archive.writestr('META-INF/container.xml', '<?xml version="1.0" encoding="UTF-8"?>'
                        '<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">'
                        '<rootfiles><rootfile full-path="EPUB/content.opf" media-type="application/oebps-package+xml"/></rootfiles></container>')
        archive.writestr('EPUB/styles/book.css', css)
        archive.writestr('EPUB/nav.xhtml', xml_bytes(nav))
        for name, _ in chapters:
            tree = ET.parse(work / name).getroot()
            for node in tree.iter():
                href = node.get('href')
                if not href or not href.startswith('#'):
                    continue
                identifier = unquote(urlsplit(href).fragment)
                if identifier not in anchors:
                    raise ValueError('Unresolved EPUB anchor: ' + href)
                node.set('href', anchors[identifier] + href)
            archive.writestr('EPUB/text/' + name, xml_bytes(tree))
        for name, source in images.items():
            archive.write(source, 'EPUB/media/' + name)
        ET.register_namespace('', OPF)
        ET.register_namespace('dc', DC)
        archive.writestr('EPUB/content.opf', xml_bytes(package))
    temporary.replace(destination)
    print(f'Packaged {len(chapters)} chapters and {len(images)} image assets.', flush=True)
