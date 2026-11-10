# Change log

Description of the changes to `etoc.sty` since its initial commit in this repo at version `1.2d 2023/10/29`.

[This diff](https://github.com/jfbu/etoc/compare/1.2e...HEAD) compares current HEAD with release `1.2e 2026/05/04`, which did not include the tagging work.

These headings map to the diffs between successive tags.

## [dev HEAD]

## [1.2f]

Tagging support, for pdfLaTeX and the LaTeX release of 2026-11-01 only.

- use the upstream paragraph tagging sockets (`para/restore`, `para/begin`, `para/end`) via `\UseTaggingSocket`, in place of `\tagpdfparaOn` and of manual structure and marked-content handling.
- obtain the structure names from the kernel symbolic names (`toc/item/text`, `toc/item/label`, `para/textblock`) via `\UseStructureName`, so that a document assigning them another role is obeyed.
- fix jfbu/etoc#8: the `lof` and `lot` package options write the destination of the figure and table entries also without hyperref when tagging is active.
- the fall-back line styles (`\etocfallbacklines`) produce a correct structure: leaders and punctuation are artifacts, the part (and book) number is an `Lbl`, the structure order is name, number, page, and no marked content is referenced twice.
- no `TOCI` for a line whose style displays nothing.
- fix jfbu/etoc#5, jfbu/etoc#10, jfbu/etoc#29: a `minipage` or a `\parbox` in a line style does not open a paragraph structure inside the `Reference` anymore (the `para/restore` socket is set to `noop` for the TOC contents).
- `\etoctaggingon` in the preamble of a document without tagging does not cause errors anymore.
- `\etocsetlocaltop.toc` accepts a level number such as `-2` or `0`, not only a level name: numbers did not survive the round trip of the `.toc` data through the `.aux` file and caused errors.
- Testing: each test file is compiled 7 times, tagpdf warnings being turned into errors for the last 2 compilations only, as the structure becomes stable only after about 6 passes; then `tocchecks.py` checks the structure of the PDF (requires [pikepdf](https://pypi.org/project/pikepdf/)); `structtree.py` prints the structure tree.  The test infrastructure is shared by `test_issues` and `test_snippets`, with scripts at top level.
- Testing: the test files use PDF 2.0 and PDF/UA-2 metadata (`documentmetadata_pdf20_ua2.txt`).  New test `gh30_tagging_project_test_598.tex`, from latex3/tagging-project#598 (jfbu/etoc#30).  With PDF 2.0 a float is tagged `Aside`, so a TOC inside a `figure` passes (jfbu/etoc#18, which remains with PDF 1.7).
- Current [test_issues errorsummary](https://github.com/jfbu/etoc/blob/e4f97fed7b737269265c6d12c4ad45e6df2fc7f2/test_issues/errorsummary): FAIL=5, TOTAL=27
  * fail: gh24_simplest_tabular.tex (a `tabular` for the display)
  * fail: gh25_start_finish.tex (material from the start and finish parts of a line style)
  * fail: test_tagging_inline_delayed.tex, test_tagging_toc_as_molecule.tex, test_tagging_toc_as_molecule_b.tex (two-stage constructions)
- Current [test_snippets errorsummary](https://github.com/jfbu/etoc/blob/e4f97fed7b737269265c6d12c4ad45e6df2fc7f2/test_snippets/errorsummary): FAIL=3, TOTAL=18
  * fail: testsnippet-01.tex (lists for the display)
  * fail: testsnippet-19.tex, testsnippet-20.tex (a `tabular` for the display)

## [1.2e]

Released on 2026/05/04 from the `master` branch, which had been trimmed on 2024/06/18 from the tagging work: hence its diff starts from `1.2d`, not from `2025-09-20`.

- hotfix for jfbu/etoc#28 (compatibility of the `lof` option with hyperref v7.01q): our redefinition of `\addcontentsline` keeps its original signature (same fix as jfbu/etoc#7 in the tagging work).  Thanks to @pkl97 for report.
- `\etocsetlinestyle` and `\etocfallbacklines` as respective aliases to `\etocsetstyle` and `\etocdefaultlines`.
- add `\etochyperlink` as `\protected` wrapper of `\hyperlink` and use it in `\etocthelinkedname` et al.
- refactor core `\Etoc@lxyz`.
- none of the dev tagging code is included.

## [2025-09-20]

- use the upstream tagging sockets `toc/starttoc/before`, `toc/starttoc/after`, `toc/contentsline/before` and `toc/contentsline/after` via `\UseTaggingSocket`, in place of the `@cfgpoint@` macros and of the internal tagpdf commands `\__tag_toc_contentsline_begin:nnn` and `\__tag_toc_contentsline_end:n`, which no longer exist.
- Testing: each test file is compiled 5 times, tagpdf warnings being turned into errors at the 4th and 5th compilations only; the test files have their `\DocumentMetadata` in an external file and can be compiled with tagging off (`./dotests.sh no`); the `test_issues` files are renamed `gh0N_*.tex`.
- Testing: snippet 11 has again its `figure` environment, to test jfbu/etoc#18.

## [2024-01-16]

- Current [errorsummary](https://github.com/jfbu/etoc/blob/7bbd267821b00d5f5e88b06e64dde2c11a363ebf/test_snippets/errorsummary): FAIL=3, PASS=15, TOTAL=18
  * fail: testsnippet-01.tex (jfbu/etoc#14, related to and possible duplicate of jfbu/etoc#25)
  * fail: testsnippet-19.tex (jfbu/etoc#20, related to and possible duplicate ot jfbu/etoc#24)
  * fail: testsnippet-20.tex (jfbu/etoc#21, related to and possible duplicate of jfbu/etoc#24)
- 2 snippets were merged so that they are at this time [18 test snippets](https://github.com/jfbu/etoc/tree/7bbd267821b00d5f5e88b06e64dde2c11a363ebf/test_snippets).
- 4 additional snippets were made to fit with template, of which 2 fail and 2 pass.
- add to repo the 26 snippets from `etoc.pdf` of which 15 can be used almost directly for testing (eleven of them not being usable directly with our test template, due to various reasons such as using commands from KOMA document class).  Eight out of the fifteen raise tagging-related warnings which will for most get converted into issues here.

## [2024-01-12]

- fix jfbu/etoc#10, via applying to `\parbox` the same treatment as for `minipage` (jfbu/etoc#5).
- fix jfbu/etoc#9, jfbu/etoc#12, jfbu/etoc#13 which all had to do with the fact that the borrowed `\@starttoc` tagging hooks turn para-tagging off, but do not reenact it in the "after" part.
- fix jfbu/etoc#11, thanks to [help from @u-fischer](https://github.com/jfbu/etoc/issues/11#issuecomment-1888089994).
- add user interface for achieving tagging in sophisticated 2-steps TOCs, where the first step done under `\etoctaggingoff` regime will construct some token list which is then used in the second, non-etoc, step, and thus the prepared tokens need to contain explicit manual tagging:
  - `\etoctagstartTOCcontents`
  - `\etocthetocitembegintag`, to be expanded (once or `\edef`) inside a user etoc line style, only makes sense there
  - `\etoctagReference` is designed to be used in-between the `tocitem{begin,end}tag`'s
  - `\etoctagLbl` is designed to be used in-between the `tocitem{begin,end}tag`'s
  - `\etocthetocitemendtag`, to be expanded (once or `\edef`) inside a user etoc line style, only makes sense there
  - `\etoctagfinishTOCcontents`

  Those macros will work independently of the `\etoctaggingon/\etoctaggingoff` flag when they get expanded, because the latter only say whether the `\tableofcontents`, `\localtableofcontents` should automatically insert tagging, and the above macros will do their real job only later, outside of `etoc` TOCs.  The first step which uses an etoc TOC typesets nothing and *must* be done with `\etoctaggingoff`.  See the [TOC as a molecule](/test_issues/test_tagging_toc_as_molecule.tex) demo file.
- add `\etochyperlink` as `\protected` wrapper of `\hyperlink` and use it in `\etocthelinkedname` et al., which facilitates their use in `\edef` for sophisticated 2-steps TOCs such as those using TikZ trees in the user manual.
- fix jfbu/etoc#8.  `\locallistoffigures` and `\locallistoftables` raised lots of warnings but this is only because the fix to jfbu/etoc#2 forgot to handle them at the same time.  Only remain now warnings due to upstrem latex3/tagging-project#55.
- fix jfbu/etoc#7.  Our redefinition of `\addcontentsline` must keep its original signature so that the [hyperref](https://github.com/latex3/hyperref) "before" hook can be inserted, when as currently via [tagpdf](https://github.com/latex3/tagpdf) this is done by kernel via a generic cmd hook.
- Testing: add a bash script for automated testing using existing test files; the latter got modified so that all [tagpdf](https://github.com/latex3/tagpdf) warnings are made into errors aborting the job, and the bash script can be made if `LATEX` environment variable is suitably set to use `latexmk -pdf` for example, so that one checks no warnings are issued on first as well as next compilations.  Using the script with any argument tells it to clean all auxiliary files first.
- strip from code all `\Etoc@tagrule` and `\Etoc@tagleaders` which had been tentatively added, then made no-op's.
- refactor core `\Etoc@lxyz` in part to avoid sub-optimal `\etocthelinkednumber` containing (begin|end) or (end|begin) with nothing in-between; also for more straightforward coding logic and improved readability of the nested conditionals.
- fix jfbu/etoc#6.  Everything in the line style apart from name, number, page is automatically tagged as an artifact.  Which may be a bad idea but it solves the `'TOCI/' --> 'Em/pdf2'` forbidden Parent-Child relation.

## [2024-01-05]

- fix jfbu/etoc#5 via a general deactivation of the minipage tagging sockets for the duration of the TOC contents.
- fix jfbu/etoc#4 thanks to @u-fischer's advice at latex3/tagging-project#54.  No more warnings at this stage!
- use `\Etoc@tagleaders` to mark as artifacts the dots in fall-back TOC line styles, in imitation of upstream `\@dottedtocline`.
- tentative `\Etoc@tagrule` added in various places (yet to be tested).
- rework indentation which had been catastrophic for ages in `\etocframedstyle` source code.

## [2024-01-03]

- refactor tagging support, fix jfbu/etoc#1, jfbu/etoc#2, jfbu/etoc#3.
- `\etocsetlinestyle` and `\etocfallbacklines` as respective aliases to `\etocsetstyle` and `\etocdefaultlines`.

## [2024-01-02]

- initial tagging support.


[dev HEAD]: https://github.com/jfbu/etoc/compare/1.2f...HEAD
[1.2f]: https://github.com/jfbu/etoc/compare/2025-09-20...1.2f
[1.2e]: https://github.com/jfbu/etoc/compare/1.2d...1.2e
[2025-09-20]: https://github.com/jfbu/etoc/compare/2024-01-16...2025-09-20
[2024-01-16]: https://github.com/jfbu/etoc/compare/2024-01-12...2024-01-16
[2024-01-12]: https://github.com/jfbu/etoc/compare/2024-01-05...2024-01-12
[2024-01-05]: https://github.com/jfbu/etoc/compare/2024-01-03...2024-01-05
[2024-01-03]: https://github.com/jfbu/etoc/compare/2024-01-02...2024-01-03
[2024-01-02]: https://github.com/jfbu/etoc/compare/1.2d-2023-10-29...2024-01-02
