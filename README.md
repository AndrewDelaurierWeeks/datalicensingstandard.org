# datalicensingstandard.org

The record site of The Data Licensing Standard for AI (TDLS-AI) v0.1, at https://datalicensingstandard.org.

The sealed files are published at https://github.com/AndrewDelaurierWeeks/data-licensing-standard. This repository serves the same files byte for byte from the folder `docs/`, with a page and a Markdown copy for each Part, Requirement and Annex, and the vendor declaration schema at the address in its `$id`.

## Build

From a checkout of the venue at commit de671fb:

```
python3 build/build.py --venue PATH_TO_VENUE --out docs
```

The build stops if a sealed file differs from its SHA-256, if the Markdown copies do not give back the sealed source, or if the words of a page's sealed block differ from its section. It needs Python 3.9 or later, pandoc 3, and pdftotext (poppler) to check the cover's words on the home page against the sealed PDF.

The home page sets the cover of the sealed PDF as a page. Its engraved device moves by `build/assets/hero.js`, the one script on the site, which loads only from this site; the device's image in `build/assets/device/` is cut from that cover, and its point files are drawn from it. Without the script the page shows the engraving still.

## License

The sealed files, and the text of the document in `docs/`, are under the license stated in Part 7 of the document; the few sentences the site adds to its pages are under the same Creative Commons Attribution 4.0 International license. The build script, the stylesheet and `hero.js` are under the MIT License (`build/LICENSE`). The files in `build/assets/device/` come from the cover engraving, which Part 7 places under the same Creative Commons Attribution 4.0 International license as the text. The fonts in `build/assets/fonts/` are under the SIL Open Font License 1.1; each family's copyright line is in its OFL file.
