# etoc
etoc.sty development repo and issue tracker

This repository will provide development snapshots from the [etoc](https://ctan.org/pkg/etoc) LaTeX package by the author.

Comments via the issue tracker are welcome: please add `@jfbu` inside your bug report, my past experience of GitHub is that I would not be pinged otherwise.

It provides only `etoc.sty`, not the full `etoc.dtx` whose latest official release is only on CTAN.

But we have deliberately left inside the etoc.sty file code comments relative to current not yet released to CTAN work.

### 1.2d 2023/10/29

The first commit in this repo with etoc.sty contains its latest official release attow, i.e. 1.2d of 2023/10/29.

### 1.2e-dev 2024/01/03

Development version of etoc aimed at supporting at least partially tagged PDF output.

Please refer to the [latex3/tagging-project](https://github.com/latex3/tagging-project) for background information.

You will find here test files which you can run via `latexmk -pdf test_tagging*tex` and check the log output for [tagpdf](https://ctan.org/pkg/tagpdf) warnings (none normally!) and if you have appropriate tools you can check if the tagging looks reasonable for the main TOC and the local TOCs.

Here is a description of what is hoped for at this stage:

```latex
\section{Tagging}
\label{etoctaggingon}
\label{etoctaggingoff}
\label{etoctagginginlineoff}
\label{etoctagthis}

For some years upstream \LaTeX{} maintainers have been engaged into a
``\LaTeX{} Tagged PDF'' project to enable automatic tagging of PDF
documents produced via \LaTeX, see the relevant entries in
\centeredline{\url{https://latex-project.org/news/latex2e-news/ltnews.pdf}}
and a general overview in this 2020 paper
\centeredline{\url{https://www.latex-project.org/publications/2020-FMi-TUB-tb129mitt-tagpdf.pdf}}
See also further relevant articles in \href{https://tug.org/tugboat}{TUGboat}.

This means that there are ongoing kernel (and \ctanpkg{hyperref}) changes
which have to be taken into account by \etoc to not be broken, or cause a
broken PDF structure, once the user activates the feature, currently via usage of
suitable \cs{DocumentMetadata} keys, cf.\@ above documentation.

As advanced \etoc users will be aware, it is possible with it to use the \toc
and \localtoc commands to do things only remotely related to tables of
contents per se, for example one can use it to count how many sections are
contained in a chapter so the only result of execution of these commands is to
update some counter or other user-defined macro to hold the result.

Current status (as of 1.2e-dev 2024/01/03):
\begin{itemize}
\item a document loading \etoc and leaving it in compatibility mode, using
  only \toc and \localtoc should produce tagged TOCs as done by kernel code,
\item a document loading \etoc and using its default (better called
  ``fallback'') line styles should not raise \ctanpkg{tagpdf} warnings (after
  final compilation) and the TOCs will have some tagging.  But the dotted
  lines are not marked yet as artefacts.
\item hopefully, a document using \csb{etocsetstyle} to define custom line
  styles and using \csb{etocname}, \csb{etocnumber} and \csb{etocpage} should
  behave about correctly, this has not been really tested, it was tested only
  via looking what happens with the package fallback line styles.  Thus the
  same remark applies about all material in the line styles which should be
  especially marked will not be so. 
\end{itemize}

One can turn tagging on or off via \csb{etoctaggingon} and
\csb{etoctaggingoff}.  Of course the former will have any effect only if the
document has activated tagging (currently via \csa{DocumentMetadata}, see
above documentation).  There is also a special purpose
\csb{etoctagginginlineoff} for those rather special uses of \csb{etocsetstyle}
which re-employ the kernel macros such as |\@dottedtocline| or |\l@section|,
see \autoref{sec:anothercompat}.  This tells \etoc to free \csb{etocname},
\csb{etocnumber} and \csb{etocpage} from contributing any tagging data by
themselves, as it will be inserted by the \LaTeX{} kernel macros and nested
marked chunks must be avoided (it also turns off \etoc added hyperlinking
because the kernel |\@dottedtocline| or |\l@section| will originate it by
themselves if tagging has been activated in the document).

These commands can not be used from inside the \marg{prefix} and \marg{contents}
arguments of \csb{etocsetstyle}.

Commands \csb{etocname}, \csb{etocnumber} and \csb{etocpage} will now
accomplish tagging tasks, as will \csb{etoclink} and the non-robust
\csb{etocthelink}.  But \csb{etocthename}, \csb{etocthenumber}, and
\csb{etocthepage} are kept as with no tagging.  This is especially important
for \csb{etocthenumber} for backwards compatibility as it may be needed in
some line styles as a numerical quantity (which it is not always, that depends
on the various \csa{thesection} etc.... macros).  A (fragile attow) command
\csb{etoctagthis} is a no-op if tagging is not activated, else it tags its
argument with label |tag=Reference|.

The author has neither the time nor the resources nor the appropriate tools to
do any kind of testing beyond the most basic by himself.

Examples such as those in this documentation which construct first some data
via specific line styles using \csb{etocthename}, \csb{etocthenumber},
\csb{etocthepage}, which are then rendered in a second stage, once the whole
TOC has been parsed, via TikZ for example, will need to use
\csb{etoctaggingoff} locally and users are currently on their own to add
tagging manually to the TikZ (or whatever) rendering.  Attow \csb{etoctagthis}
can only be used from inside the \marg{prefix} and \marg{contents}
arguments of \csb{etocsetstyle}.
```

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
