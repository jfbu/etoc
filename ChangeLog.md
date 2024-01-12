# Change log

Description of the changes to `etoc.sty` since its initial commit in this repo at version `1.2d 2023/10/29`.

[This diff](https://github.com/jfbu/etoc/compare/1.2d-2023-10-29...HEAD) compares current HEAD with latest CTAN release (which currently is the `1.2d 2023/10/29` one).

These headings map to the diffs between successive tags.

## [dev HEAD]

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

  Those macros will work independently of the `\etoctaggingon/\etoctaggingoff` flag when they get expanded, because the latter only say whether the `\tableofcontents`, `\localtableofcontents` should automatically insert tagging, and the above macros will do their real job only later, outside of `etoc` TOCs.  The first step which uses an etoc TOC typesets nothing and *must* be done with `\etoctaggingoff`.  See the [TOC as a molecule](/issuetesting/test_tagging_toc_as_molecule.tex) demo file.
- add `\etochyperlink` as `\protected` wrapper of `\hyperlink` and use it in `\etocthelinkedname` et al., which facilitates their use in `\edef` for sophisticated 2-steps TOCs such as those using TikZ trees in the user manual.
- fix jfbu/etoc#8.  `\locallistoffigures` and `\locallistoftables` raised lots of warnings but this is only because the fix to jfbu/etoc#2 forgot to handle them at the same time.  Only remain now warnings due to upstrem latex3/tagging-project#55.
- fix jfbu/etoc#7.  Our redefinition of `\addcontentsline` must keep its original signature so that the [hyperref](https://github.com/latex3/hyperref) "before" hook can be inserted, when as currently via [tagpdf](https://github.com/latex3/tagpdf) this is done by kernel via a generic cmd hook.
- [testing] add a bash script for automated testing using existing test files; the latter got modified so that all [tagpdf](https://github.com/latex3/tagpdf) warnings are made into errors aborting the job, and the bash script can be made if `LATEX` environment variable is suitably set to use `latexmk -pdf` for example, so that one checks no warnings are issued on first as well as next compilations.  Using the script with any argument tells it to clean all auxiliary files first.
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


[dev HEAD]: https://github.com/jfbu/etoc/compare/2024-01-12...HEAD
[2024-01-12]: https://github.com/jfbu/etoc/compare/2024-01-05...2024-01-12
[2024-01-05]: https://github.com/jfbu/etoc/compare/2024-01-03...2024-01-05
[2024-01-03]: https://github.com/jfbu/etoc/compare/2024-01-02...2024-01-03
[2024-01-02]: https://github.com/jfbu/etoc/compare/1.2d-2023-10-29...2024-01-02
