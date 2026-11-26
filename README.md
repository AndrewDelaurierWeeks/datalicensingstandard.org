# datalicensingstandard.org

The record site of The Data Licensing Standard for AI (TDLS-AI) v0.1, at https://datalicensingstandard.org.

The sealed files are published at https://github.com/AndrewDelaurierWeeks/data-licensing-standard. This repository serves the same files byte for byte from the folder `docs/`, with a page and a Markdown copy for each Part, Requirement and Annex, and the vendor declaration schema at the address in its `$id`.

## Build

From a checkout of the venue at commit de671fb:

```
python3 build/build.py --venue PATH_TO_VENUE --out docs
```

The build stops if a sealed file differs from its SHA-256, if the Markdown copies do not give back the sealed source, or if the words of a page's sealed block differ from its section. It needs Python 3.9 or later, pandoc 3, and pdftotext (poppler) to check the cover's words on the home page and the colophon's words against the sealed PDF.

The home page sets the cover of the sealed PDF as a page. Its engraved device moves by `build/assets/hero.js`, the one script on the site (served under a name that carries its hash), which loads only from this site; the device's image in `build/assets/device/` is cut from that cover, and its point files are drawn from it. Without the script the page shows the engraving still. After 5 seconds without pointer movement the device holds still and the script stops running until the next movement, a touch on the device or a press.

Every page carries its own security policy in a meta tag: scripts, styles, images, fonts and data from this site alone, nothing inline except the structured data, which is not run, no forms, no embedded frames, no base address. The stylesheet and the script carry integrity hashes, and their names carry their hashes, so a cached old file never meets a new page. The site sets no cookies and stores nothing in the browser. `/.well-known/security.txt` (RFC 9116) says where to report a security problem with the site: the repository's private vulnerability reporting. Its Expires date is 2027-11-25.

For search and AI tools: each section page has a description drawn from its own sealed words, every page has structured data in the schema.org vocabulary (the standard, its sections, the author, the glossary of Annex C as defined terms), with the license given as Part 7 states it, and a preview image; each section page links its Markdown copy. `llms.txt` is a guide for language models and `llms-full.txt` is the sealed source, byte for byte. The keywords are the sealed text's own words; the build checks each one against the source. The colophon at `/colophon/` is page 3 of the sealed PDF, word for word, and the build checks it against that page. The page `/security-elements/` is page 4 of the sealed PDF, word for word, with the page's own figures taken from it by `build/tools/make-security.py`; the build checks its words against that page. The site's icon is the face of the cover's engraved device, cut from the sealed PDF by `build/tools/make-icons.py`.

## License

The sealed files, and the text of the document in `docs/`, are under the license stated in Part 7 of the document; the few sentences the site adds to its pages are under the same Creative Commons Attribution 4.0 International license. The build script, the stylesheet and `hero.js` are under the MIT License (`build/LICENSE`). The files in `build/assets/device/` and `build/assets/icons/`, `build/assets/apple-touch-icon.png`, and `device.webp` and `face.webp` in `build/assets/security/`, come from the cover engraving, which Part 7 places under the same Creative Commons Attribution 4.0 International license as the text. The fonts in `build/assets/fonts/` are under the SIL Open Font License 1.1; each family's copyright line is in its OFL file.
