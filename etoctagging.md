# Technical brief on etoc tagging (WIP)

We will try to keep these items in sync with the actual code, but they may be lagging behind.

[etoctagging.tex](/etoctagging.tex) is a user level companion of the more technical explications which are given here.  It may lag behind even more.

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
- i.e. the `\@starttoc` and `\@contentsline` tagging hooks, which put into place the `TOC` and `TOCI` struct's.
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


[2024-01-16]: https://github.com/jfbu/etoc/releases/tag/2024-01-16
