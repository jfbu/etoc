# etoc

etoc.sty development repo and issue tracker

This repository:

- serves as an issue tracker for the current release of the [etoc](https://ctan.org/pkg/etoc) LaTeX package on [CTAN](https://ctan.org),
- provides snapshots of the current dev version of the package, allowing interested people to test it and report bugs or feature requests.

Please insert `@jfbu` inside your bug report else I may not be pinged.

The repository provides only `etoc.sty`, not the full `etoc.dtx` whose latest official release is only on CTAN.  But this version ot `etoc.sty` may contain deliberately comments which ultimately will be moved to the released `dtx` file.

[This diff](https://github.com/jfbu/etoc/compare/1.2d-2023-10-29...HEAD) compares current HEAD with latest CTAN release.

See the [Change log](/ChangeLog.md) for more fine-grained tag-to-tag diffs.

## PDF Tagging

`etoc` development is currently mostly about adding tentative experimental support for tagging, using the related upstream kernel code in [`latex-lab`](https://github.com/latex3/latex2e/tree/develop/required/latex-lab) as model and starting point.

- [etoctagging.tex](/etoctagging.tex): this file contains the user level description extracted from dev `etoc.dtx`.  You can compile it to pdf using `pdflatex`.
- [etoctagging.md](/etoctagging.md): this file contains more technical notes, they are complementary to the user manual.

For background information on the upstream LaTeX project, refer to this PDF document (by Frank Mittelbach and Chris Rowley): [*LaTeX Tagged PDF—A blueprint for a large project*](https://www.latex-project.org/publications/2020-FMi-TUB-tb129mitt-tagpdf.pdf), and to the [latex3/tagging-project](https://github.com/latex3/tagging-project) and [latex3/tagpdf](https://github.com/latex3/tagpdf) repositories.

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
