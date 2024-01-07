# technical brief on etoc tagging (WIP)

We will try to keep these items in sync with the actual code, but they may be lagging behind.

- `etoc` uses `\@starttoc@cfgpoint@before{toc}` and `\@starttoc@cfgpoint@after{toc}`, (*this has to be kept in sync with upstream evolving interface*)
- for local tables of contents the local TOC triggers from *inside* the `.toc` data (which has been saved in a `\toks`), so the above hooks are not used unconditionally, but strategically located (see jfbu/etoc#2),
- `etoc` if left in compatibility mode simply executes the contents of the `.toc` file (with its `\contentsline` entries which have been updated by kernel to do tagging) so it has nothing more to do,
- else it uses `\@contentsline@cfgpoint@before{#1}{#2}{#3}{#4}` and `\@contentsline@cfgpoint@after{#1}{#2}{#3}{#4}` in `\Etoc@etoccontentsline@`, (*this has to be kept in sync with upstream evolving interface*)
- from this point on the tagging is done via the [tagpdf](https://github.com/latex3/tagpdf) mark-up API,
- the `<prefix>` and `<contents>` of the line style are inside a `tag=Reference` struct; but at the start of their expansion they are in an mc chunk tagged as `artifact`,
- `\etocname`, `\etocnumber`, `\etoclink` each stop the `artifact` and produce their own `tag=Reference` chunk.  The `\etocnumber` inserts a sub-struct with `tag=Lbl`,
- another layer adds the hyperlinks, `\etocthelinkedname`, `\etocthelinkednumber` and `\etocthelinkedpage` are defined in addition to `\etocthetaggedname`, `\etocthetaggednumber` and `\etocthetaggedpage` which contain no hyperlinks,
- then depending on the `\Hy@linktoc` numerical value, the former or the latter are mapped to (the fragile versions of the robust) `\etocname` etc...,
- it was found out necessary to disable the `minipage` kernel tagging sockets, not only for the usage of `minipage` in the `\etocframedstyle` (which is a framing around contents) but also as `minipage` can be used in the user toc line specifications and was found incompatible with the above described approach (see jfbu/etoc#4, jfbu/etoc#5), or rather with an earlier one, but it was checked to still be incompatible with the current one,
- one reason for declaring everything as  `artifact` *except* for name, number, page is that some LaTeX mark-up tagging behavior (currently only `\emph` but perhaps others) was determined to be incompatible with being a direct child of `TOCI` (see jfbu/etoc#6); in expectations that other mark-up would prove problematic the only reasonable way seems to be to have everything apart from `name`, `number` and `page` be artifacts.  Indeed these extras do not seem to define structure, but only a priori will add decorations.

`etoc` is aware of, and maintains virtually a hierarchical tree of the `.toc` file (or relevant portion to local toc), which seems to be like a potential mirror of  some core low-level actions done by [tagpdf](https://github.com/latex3/tagpdf).  But `etoc` user can arbitrarily reassign levels for doing some rather devious tasks using only the `.toc` file.  As a kind of example, see `etoc`'s own `\locallistoffigures` and `\locallistoftables`.  Thinking this through will not be for the immediate future.

At any rate, already `\etoctagging{on,off}` are provided and are indispensable for some advanced usages of `\localtableofcontents` as per the user documentation.  For this and other things see the [etoctagging.tex](/etoctagging.tex) file which is the user level companion to the more technical explications which have been given here.
