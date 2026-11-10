# Technical brief on etoc tagging (WIP)

We will try to keep these items in sync with the actual code, but they may be lagging behind.

The PDF and LaTeX views of what a TOC is are simply too archaic and restrictive to etoc, which flies high above such cages.

## Dev notes and perspectives at [1.2f]

The tagging support of 1.2f has been checked only with pdfLaTeX and the LaTeX release of 2026-11-01.  The sections after this one describe the state at 2025-09-20 and at 2024-01-16.

Work done in November 2026:
- around the TOC, the paragraph state is handled with the sockets `para/end`, `para/restore` and `para/begin`, according to whether the TOC starts in vertical or horizontal mode,
- the structure names are obtained via `\UseStructureName` from the kernel symbolic names `toc/item/text`, `toc/item/label` and `para/textblock`,
- a line is a `TOCI` (opened by the socket) containing a `Reference` structure; the prefix and contents are in an artifact marked content; `\etocname`, `\etocnumber` and `\etocpage` end it, insert their data as `Reference` marked content (the number as `Lbl` marked content in an `Lbl` structure which is a child of the `Reference`), then restart an artifact explicitly: `\tag_mc_end_push:` and `\tag_mc_begin_pop:n` can not be used, as the pop restarts a tagged marked content,
- with hyperref, `\etoclink` tags its argument as `Reference` marked content, as the `Link` structure needs real content; without hyperref its argument remains an artifact,
- no `TOCI` for a line whose prefix and contents are both empty,
- boxes typeset only to be measured, then discarded, are built with tagging suspended, else their marked content is referenced in the structure tree although it never reaches the PDF,
- the fall-back line styles produce a correct structure (leaders and punctuation as artifacts, number as `Lbl`, order name, number, page),
- during the TOC contents the sockets `parbox/before`, `parbox/after`, `minipage/before`, `minipage/after` and `para/restore` are set to `noop`: with the LaTeX release of 2026-11-01, `\parbox` and `minipage` use `para/restore` inside their box, which re-activated paragraph tagging inside a `Reference`; at the end of the TOC `etoc` assigns the `default` plug of `para/restore` again before using it,
- the `lof` and `lot` package options write the destination of the copied figure and table entries also without hyperref (jfbu/etoc#8),
- each test file is compiled 7 times, tagpdf warnings being turned into errors for the last 2 only, then `tocchecks.py` checks the structure of the PDF.

Correction to the 2024 notes below: since the fix of jfbu/etoc#22 (2024-01-14), `etoc` defines `\toclevel@<levelname>` from its own level if it is undefined, as latex-lab needs it.

Unsolved:
- material typeset by the `{<start>}` and `{<finish>}` parts of a line style is not tagged at all, neither as content nor as artifact, and a structure created there (for example by `\emph`) becomes a child of the `TOC` (jfbu/etoc#25),
- displays built from structural environments, such as a `tabular` (jfbu/etoc#24) or lists, whose structures interleave with `TOC` and `TOCI`,
- the two-stage constructions (TOC as a molecule, delayed inline TOC) raise tagging errors again,
- a TOC inside a `figure` or `table` (jfbu/etoc#18, upstream),
- `etoc` can not recover the plug of `para/restore` assigned by the document before the TOC, and assumes it was `default`,
- the test `\ifhmode` deciding the paragraph handling at the start of the TOC is probably not the right one (for example in a TikZ picture),
- `etoc`'s level system versus the kernel's `\toclevel@<levelname>`.

## Dev notes up to [2025-09-20]

- the `@cfgpoint@` macros (`\@starttoc@cfgpoint@before`, `\@starttoc@cfgpoint@after`, `\@contentsline@cfgpoint@before`, `\@contentsline@cfgpoint@after`) and the internal tagpdf commands `\__tag_toc_contentsline_begin:nnn` and `\__tag_toc_contentsline_end:n` used earlier no longer exist; `etoc` uses via `\UseTaggingSocket` the tagging sockets `toc/starttoc/before` and `toc/starttoc/after` around the TOC contents (argument `toc`, or `localtoc` for local lists of figures and tables), and `toc/contentsline/before` and `toc/contentsline/after` with arguments `{#1}{#2}{#3}{#4}` in `\Etoc@etoccontentsline@` (in compatibility mode the kernel `\contentsline` does it); the second argument is no longer replaced by `\etocthename`,
- the test files are compiled several times, tagpdf warnings being turned into errors only at the last compilations, as some warnings disappear only after several passes; they have their `\DocumentMetadata` in an external file and can be compiled with tagging off.

## Perspectives at [2024-01-16]

At this stage, success has been obtained even with rather fancy TOCs, as for example:
- the TOC is rendered as a TikZ tree: [a](https://github.com/jfbu/etoc/blob/7bbd267821b00d5f5e88b06e64dde2c11a363ebf/test_issues/test_tagging_toc_as_molecule.tex), [b](https://github.com/jfbu/etoc/blob/7bbd267821b00d5f5e88b06e64dde2c11a363ebf/test_issues/test_tagging_toc_as_molecule_b.tex).
- [the one](https://github.com/jfbu/etoc/blob/badf89455e7e04061e9cdbba71a480a118f765a5/test_snippets/etocsnippet-12.txt) from jfbu/etoc#19 which stores subsections and subsubsections into an `lrbox` environment and displays them as footnotes via un `\unhbox`,
- a [TOC of all TOCs](https://github.com/jfbu/etoc/blob/6dfe94e6423a7fbe8728231415edc616554b7fdb/test_snippets/etocsnippet-14.txt) which gives (inline in a paragraph) a linked list of all eTOCs encountered in the document,
- a [very complex one](https://github.com/jfbu/etoc/blob/624241c90090c44facaa14f28aadf32c7afddfa0/test_snippets/etocsnippet-25.txt) where sections redefine dynamically the style of subsections, for example counting them rather than displaying them, and moreover this being done only by specific sections chosen as per their number in the current chapter... moreover in some cases the section style will use `\l@section` so that then etoc-tagging has to be locally turned off as it will come from the upstream additions to `\l@section` or `\@dottedtocline`...

But ultimately the following can not be avoided:
- `etoc` empowers the user to employ *arbitrary* LaTeX code in the custom line styles,
- that means not only the `{<prefix>}{<contents>}` part which actually gives the typesetting of a line style at a given level can use *arbitrary* LaTeX code,
- but also the `{<start>}` and `{<finish>}` parts can be used to inject *arbitrary* code and (at this time of the author pondering) it wouldn't be right to consider them as belonging to the `TOCI` structural level.
- It is also possible to render TOCs as tables, so that one line style may start typesetting in a cell then inject a few `&` and continue typesetting there.  When tagging is not involved the simplest way to make this work is for user to execute `\etocglobaldefs` so that the `\etocname` etc... as defined while in the first cell have global scope and are usable in the next cell.
- Fancy TOCs using a two stage process need to provide the user suitable mark-up interface, as the parsing stage is the one using `etoc` and must be done with tagging being turned off, and the accumulated data (in a macro or a toks) will have to be prepared with suitable tagging macros for its rendering in the second, non-`etoc` stage.


The problems related to arbitrariness of user code  manifest themselves in particular in issues jfbu/etoc#24 and jfbu/etoc#25.

I was initially not quite aware that the more user employs official LaTeX code and not core TeX level primitives, the more danger there will be that tagging will complain about an un-allowed Parent-Child relation, but it is obvious a posteriori.

I am reaching end of time which I can devote to this for now, and my free time was devoted to test `etoc` not yet to become familiar with the PDF tagging references, nor with the [latex-lab](latex3/latex2) code, but my conclusion at this stage is that the only way to make this work for (almost-all) eTOCs is for `etoc` to typeset them with:
- **all** upstream tagging support being turned off, **except** for the sole one devoted to TOC,
- i.e. the `\@starttoc` and `\contentsline` tagging hooks, which put into place the `TOC` and `TOCI` struct's.
- As alternative to re-using the tagging hooks or socket plugs will be  to have our own custom copy, but it *has* to be closely modeled on upstream, as it *will have to update upstream related structures*.

It is not clear at this stage if the last point is possible in tabular context for example.  There are other more minor problems here that the `\@starttoc` tagsupport code is not compatible (at last time of testing) with being executed from inside a `figure` or `table` environment, see jfbu/etoc#18.

## Dev notes up to [2024-01-16]

- special uses of `etoc` may execute `\(local)tableofcontents` not to typeset, but to build some structures; for such cases in particular `\etoctaggingoff` and `\etoctaggingon` are provided, to control whether `etoc` adds automatically tagging,
- user level interface macros are provided (see the [Change log](/ChangeLog.md)) to insert tagging manually, this is useful for sophisticated TOCs from the previous item, where `\tableofcontents` typesets nothing but only prepares some tokens which are used later, for example in a TikZ picture, see the [toc as a molecule demo](/test_issues/test_tagging_toc_as_molecule.tex) example,
- `etoc` uses the kernel `\@starttoc@cfgpoint@before{toc}` and `\@starttoc@cfgpoint@after{toc}` before and after the `.toc` file contents, (*this has to be kept in sync with upstream evolving interface*),
- for local TOCs (inclusive of local lists of figures or tables) it uses as argument to kernel configuration points `{localtoc}` in place of `{toc}`,
- `etoc` if left in compatibility mode simply executes the contents of the `.toc` file (with its `\contentsline` entries which have been updated by kernel to do tagging) so it has nothing more to do,
- else it uses `\@contentsline@cfgpoint@before{#1}{#2}{#3}{#4}` and `\@contentsline@cfgpoint@after{#1}{#2}{#3}{#4}` in `\Etoc@etoccontentsline@`, (*this has to be kept in sync with upstream evolving interface*),
- actually the `#2` is now replaced by `\etocthename` (which will then be expanded immediately by kernel code);
- from this point on the tagging is done using the [tagpdf](https://github.com/latex3/tagpdf) mark-up API,
- [WIP] (some further thoughts are needed on this overall design) the `<prefix>` and `<contents>` of the line style are inside a `tag=Reference` struct; but at the start of their expansion they are in an mc chunk tagged as `artifact`, using `\tagmcbegin{artifact=layout}`,
- [WIP] `\etocname`, `\etocnumber`, `\etoclink` each stop the `artifact` and produce their own `tag=Reference` chunk.  The `\etocnumber` inserts a sub-struct with `tag=Lbl`, (TODO: decide if really this must be nested, pdf 1.7 reference seems to say `Lbl` can be direct child of `TOCI`, but I imitated `latex-lab`)
- during this construction the hyperlinks get handled and `\etocthelinkedname`, `\etocthelinkednumber` and `\etocthelinkedpage` are defined in addition to `\etocthetaggedname`, `\etocthetaggednumber` and `\etocthetaggedpage` which contain no hyperlinks, (those latter macros may be dropped or renamed and kept non-user level),
- (independent of tagging) the `\etocthelinkedname` et al. use now a `\protected` wrapper of `hyperlink` which facilitates their use in an `\edef` for advanced usage of `etoc`, see the [toc as a molecule demo](/test_issues/test_tagging_toc_as_molecule.tex), 
- depending on the `\Hy@linktoc` numerical value, the robust macros `\etocname` etc..., are then configured to expand to the linked or the non linked (but still tagged) variants,
- one reason for declaring everything as  `artifact` *except* for name, number, page is that some LaTeX mark-up tagging behavior (currently only `\emph` but perhaps others) was determined to be incompatible with being a direct child of `TOCI` (see jfbu/etoc#6); in expectations that other mark-up would prove problematic the only reasonable way seems to be to have everything apart from `name`, `number` and `page` be artifacts.  Indeed these extras do not seem to define structure, but only a priori will add decorations, *testing is needed here*,
- it was found out necessary to disable the `minipage` kernel tagging sockets, not only for the usage of `minipage` in the `\etocframedstyle` (which is a framing around contents, thus this happens external to the toc contents tagging, and the problem was not related to the TOC related kernel tagging hooks but those in `minipage`) but also as `minipage` can be used in the user toc line specifications and was found incompatible with the above described approach (see jfbu/etoc#4, jfbu/etoc#5), or rather with an earlier one, but it was checked to still be incompatible with the current one,
- both `\etocframedstyle` and `\etocruledstyle` box their title, and a `\parbox` can not be inserted inside a primitive TeX box unless its tagging hooks have been de-activated (jfbu/etoc#15, jfbu/etoc#17).

`etoc` is aware of, and maintains virtually a hierarchical tree of the `.toc` file (or relevant portion to local toc), which seems to be like a potential mirror of  some core low-level actions done by [tagpdf](https://github.com/latex3/tagpdf).  But `etoc` user can arbitrarily reassign levels for doing some rather devious tasks using only the `.toc` file.  As a kind of example, see `etoc`'s own `\locallistoffigures` and `\locallistoftables`.  Some thinking and testing will be needed to see how arbitrary level assignments by user may affect the kernel tagging code which expects a fixed hierarchy.  At least, `etoc` does not define `\toclevel@<levelname` macros for reasons pre-existing tagging, see code comments.  This removes surely potential problems.  Untested, but for example a TOC of all subsections ignoring chapters and sections, as is possible with `etoc` should be tagged fine.  And preliminary testing of `etoc`'s `\locallistoffigures` and `\locallistoftables` seems to be positive.


[1.2f]: https://github.com/jfbu/etoc/releases/tag/1.2f
[2025-09-20]: https://github.com/jfbu/etoc/releases/tag/2025-09-20
[2024-01-16]: https://github.com/jfbu/etoc/releases/tag/2024-01-16
