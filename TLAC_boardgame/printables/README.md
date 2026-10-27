# TLAC printables and ebooks

- `ThinkLikeAComputer-English-All-Steps.epub`: all five tutorial collections from the portal in English, including all seven games' instruction cards, complete static walkthroughs of the tutorial examples, and reproducible sample sessions of every game.
- `ThinkLikeAComputer-Japanese-All-Steps.epub`: Japanese edition of the same complete book.
- `ThinkLikeAComputer-Spanish-All-Steps.epub`: Spanish edition of the same complete book.
- `ThinkLikeAComputer-English.epub`: an identical copy at the previous download path.
- `all_boards.pdf`: labelled boards at the intended print size.
- `all_objects.pdf`: printable game pieces.

The EPUB works offline in an EPUB reader. It has a table of contents, an index linking directly to each program's first step, board illustrations, and expanded practice answers. Complete walkthroughs appear directly after their lesson examples. Each begins with a result preview and repeats the complete board, watched variables, and accumulated text output at every step, including unchanged states. Nothing is collapsed. The introductory assignment, condition, movement, and conceptual morning-routine cards also have explicit walkthroughs.

Game samples run the unmodified Python sources with fixed input sequences and random seed 7. Every executed source step, including initialization loops, is included. The book states the inputs and stopping point for each sample; these represent one session each, not all possible playthroughs. `epub_game_runs.py` records them without live keyboard input or sleeps.

Instruction charts retain the HTML tutorials’ original markup, colors, number badges, indentation images, and nested blocks. Their text remains selectable. The builder copies each page’s chart styles and restores the charts after Pandoc conversion so their layout is preserved in the EPUB.

To regenerate the EPUB after rebuilding the tutorial HTML files:

```sh
python3 TLAC_boardgame/printables/build_english_epub.py
python3 TLAC_boardgame/printables/build_english_epub.py --language ja
python3 TLAC_boardgame/printables/build_english_epub.py --language es
```

The builder uses Pandoc, Beautiful Soup 4, and Pillow. It reads the existing HTML and embedded execution data, records the bounded game samples, and works without network access. It validates the EPUB archive, edition language metadata, XML, internal links, and bundled images, and compares every packaged step's full output and watched values against its source snapshot.

Japanese and Spanish editions use the existing translations of the lessons, instruction cards, and execution labels. Book navigation, walkthrough captions, and game-session notes are localized by `epub_translations.py`. Source code, variable names and values, original game output, and the GPL license remain verbatim; the introduction explains this in each language. Each language builds to its own EPUB without replacing the other editions.
