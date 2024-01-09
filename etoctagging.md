# technical brief on etoc tagging (WIP)

We will try to keep these items in sync with the actual code, but they may be lagging behind.

- `etoc` uses `\@starttoc@cfgpoint@before{toc}` and `\@starttoc@cfgpoint@after{toc}`, (*this has to be kept in sync with upstream evolving interface*)
- `etoc` if left in compatibility mode simply executes the contents of the `.toc` file (with its `\contentsline` entries which have been updated by kernel to do tagging) so it has nothing more to do,
- else it uses `\@contentsline@cfgpoint@before{#1}{#2}{#3}{#4}` and `\@contentsline@cfgpoint@after{#1}{#2}{#3}{#4}` in `\Etoc@etoccontentsline@`, (*this has to be kept in sync with upstream evolving interface*)
- from this point on the tagging is done via the [tagpdf](https://github.com/latex3/tagpdf) mark-up API,
- user level interface macros are provided (see the [Change log](/ChangeLog.md)) to insert tagging manually, this is useful for sophisticated TOCs where `\tableofcontents` typesets nothing but only prepares some tokens which are used later, for example in a TikZ picture,
- the `<prefix>` and `<contents>` of the line style are inside a `tag=Reference` struct; but at the start of their expansion they are in an mc chunk tagged as `artifact`, using `\tagmcbegin{artifact=layout}`,
- `\etocname`, `\etocnumber`, `\etoclink` each stop the `artifact` and produce their own `tag=Reference` chunk.  The `\etocnumber` inserts a sub-struct with `tag=Lbl`, (TODO: decide if really this must be nested, pdf 1.7 reference seems to say `Lbl` can be direct child of `TOCI`, but I imitated `latex-lab`)
- another layer adds the hyperlinks, `\etocthelinkedname`, `\etocthelinkednumber` and `\etocthelinkedpage` are defined in addition to `\etocthetaggedname`, `\etocthetaggednumber` and `\etocthetaggedpage` which contain no hyperlinks,
- (independent of tagging) the `\etocthelinkedname` et al. use now a `\protected` wrapper of `hyperlink` which facilitates their use in an `\edef` for advanced usage of `etoc`, see the [toc as a molecule demo](/issuetesting/test_tagging_toc_as_molecule.tex), 
- depending on the `\Hy@linktoc` numerical value, the `\etocname` etc..., are then using either the linked or non-linked variants,
- it was found out necessary to disable the `minipage` kernel tagging sockets, not only for the usage of `minipage` in the `\etocframedstyle` (which is a framing around contents) but also as `minipage` can be used in the user toc line specifications and was found incompatible with the above described approach (see jfbu/etoc#4, jfbu/etoc#5), or rather with an earlier one, but it was checked to still be incompatible with the current one,
- one reason for declaring everything as  `artifact` *except* for name, number, page is that some LaTeX mark-up tagging behavior (currently only `\emph` but perhaps others) was determined to be incompatible with being a direct child of `TOCI` (see jfbu/etoc#6); in expectations that other mark-up would prove problematic the only reasonable way seems to be to have everything apart from `name`, `number` and `page` be artifacts.  Indeed these extras do not seem to define structure, but only a priori will add decorations.

`etoc` is aware of, and maintains virtually a hierarchical tree of the `.toc` file (or relevant portion to local toc), which seems to be like a potential mirror of  some core low-level actions done by [tagpdf](https://github.com/latex3/tagpdf).  But `etoc` user can arbitrarily reassign levels for doing some rather devious tasks using only the `.toc` file.  As a kind of example, see `etoc`'s own `\locallistoffigures` and `\locallistoftables`.  Thinking this through will not be for the immediate future.

At any rate, already `\etoctagging{on,off}` are provided and are indispensable for some advanced usages of `\localtableofcontents` as per the user documentation, see the [toc as a molecule demo](/issuetesting/test_tagging_toc_as_molecule.tex).

The [etoctagging.tex](/etoctagging.tex) file is a user level companion to the more technical explications which have been given here.
