# etoc

etoc.sty development repo and issue tracker

This repository:
- serves as an issue tracker for the current release of the [etoc](https://ctan.org/pkg/etoc) LaTeX package on [CTAN](https://ctan.org),
- provides snapshots of the current dev version of the package, allowing interested people to test it and report bugs or feature requests.

Please insert `@jfbu` inside your bug report else I may not be pinged.

The repository provides only `etoc.sty`, not the full `etoc.dtx` whose latest official release is only on CTAN.  But this version ot `etoc.sty` may contain deliberately comments which ultimately will be moved to the released `dtx` file.

[This diff](https://github.com/jfbu/etoc/compare/1.2d-2023-10-29...HEAD) compares current HEAD with latest CTAN release.

## PDF Tagging

For background information on the current status of the upstream LaTeX project, refer to this PDF document (by Frank Mittelbach and Chris Rowley): [*LaTeX Tagged PDF—A blueprint for a large project*](https://www.latex-project.org/publications/2020-FMi-TUB-tb129mitt-tagpdf.pdf) for background information, and to the [latex3/tagging-project](https://github.com/latex3/tagging-project) and [latex3/tagpdf](https://github.com/latex3/tagpdf) repositories.

For a description extracted from dev `etoc.dtx` of what is hoped for at this stage regarding this topic, see [etoctagging.tex](/etoctagging.tex).  You can compile it to pdf using `pdflatex`.

Here we give a more technical brief description, feedback welcome! We will try to keep this in sync with the actual code.

- `etoc` uses `\@starttoc@cfgpoint@before{toc}` and `\@starttoc@cfgpoint@after{toc}`, (*this has to be kept in sync with upstream evolving interface*)
- for local tables of contents this is a bit subtle because the local TOC triggers from *inside* the `.toc` data (which has been saved in a `\toks`), hence the above hooks are used only at a strategic location (see jfbu/etoc#2),
- `etoc` if left in compatibility mode simply executes the contents of the `.toc` file (thus the standard `\contentsline`) so it has nothing more to do, the tagging will be by the kernel (or class),
- else it uses `\@contentsline@cfgpoint@before{#1}{#2}{#3}{#4}` and `\@contentsline@cfgpoint@after{#1}{#2}{#3}{#4}` in `\Etoc@etoccontentsline@`, (*this has to be kept in sync with upstream evolving interface*)
- from this point on the tagging is done via the [tagpdf](https://github.com/latex3/tagpdf) mark-up API,
- specifically both the `<prefix>` and `<contents>` of the line style are inside a `tag=Reference` struct; but immediately a marked content chunk is started but tagged as `artifact`,
- then `\etocname`, `\etocnumber`, `\etoclink` each stop the `artifact` and produce a `tag=Reference` chunk.  The number inserts a sub-struct with `tag=Lbl`,
- there is another layer to add the hyperlinks, `\etocthelinkedname`, `\etocthelinkednumber` and `\etocthelinkedpage` are defined in addition to `\etocthetaggedname`, `\etocthetaggednumber` and `\etocthetaggedpage` which contain no hyperlinks; depending on `\Hy@linktoc` numerical value, the former or the latter are mapped to (the fragile versions of the robust) `\etocname` etc...
- it was found out necessary to disable the `minipage` kernel tagging sockets, not only for the usage of `minipage` in the `\etocframedstyle` (which is a framing around contents) but also as `minipage` can be used in the user toc line specifications and was found incompatible with the above described approach (see jfbu/etoc#4, jfbu/etoc#5), or rather with an earlier one, but it was checked to still be incompatible with the current one,
- one reason for the choice that everything is declared `artifact` *except* for name, number, page is that some LaTeX mark-up tagging behavior (currently only `\emph` but perhaps others) was determined to be incompatible with being a direct child of `TOCI` (see jfbu/etoc#6).

A final comment is that `etoc` is aware of, and maintains virtually a hierarchical tree of the `.toc` file (or relevant portion to local toc), which seems to be like a potential mirror of  some core low-level actions done by [tagpdf](https://github.com/latex3/tagpdf).  But `etoc` user can arbitrarily reassign levels for doing some rather devious tasks using only the `.toc` file.  As a kind of example, see `etoc`'s own `\locallistoffigures` and `\locallistoftables`.  Thinking this through will not be for the immediate future.

At any rate, already `\etoctagging{on,off}` are provided and are indispensable for some advanced usages of `\localtableofcontents` as per the user documentation.  For this and other things see the [etoctagging.tex](/etoctagging.tex) file which is the user level companion to the more technical explications which have been given here.

## License

<pre>
%     This Work may be distributed and/or modified under the
%     conditions of the LaTeX Project Public License, in its
%     version 1.3c. This version of this license is in
%          http://www.latex-project.org/lppl/lppl-1-3c.txt
%     and the latest version of this license is in
%          http://www.latex-project.org/lppl.txt
%     and version 1.3 or later is part of all distributions of
%     LaTeX version 2005/12/01 or later.
</pre>
