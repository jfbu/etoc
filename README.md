# etoc
etoc.sty development repo and issue tracker

This repository will provide development snapshots from the [etoc](https://ctan.org/pkg/etoc) LaTeX package by the author.

Comments via the issue tracker are welcome: please add `@jfbu` inside your bug report, my past experience of GitHub is that I would not be pinged otherwise.

It provides only etoc.sty, not the full etoc.dtx whose latest official release is only on CTAN.

But we have deliberately left inside the etoc.sty file code comments relative to current not yet released to CTAN work.

# 1.2d 2023/10/29

The first commit in this repo with etoc.sty contains its latest official release attow, i.e. 1.2d of 2023/10/29.

# 1.2e-dev 2024/01/02

This tag (sic) corresponds to a development version of etoc aimed at supporting at least partially tagged PDF output.

You will find test files there which you can run via `latexmk -pdf test_tagging*tex` and check the log output for [tagpdf](https://ctan.org/pkg/tagpdf) warnings (none normally!) and if you have appropriate tools you can check if the tagging looks reasonable for the main TOC and the local TOCs.

Update: due to [#1](https://github.com/jfbu/etoc/issues/1), usage of `latexmk -pdf` has to be modified into `latexmk -f -pdf` and one has to hit RETURN each time TeX pauses to report the tagpdf error message, or `latexmk -f -interaction=nonstopmode -pdf` to avoid that.

Here is a description of what is hoped for at this stage:

```latex
\section{Tagging}
\label{etoctaggingon}
\label{etoctaggingoff}
\label{etocthetaggednumber}

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

Current status (as of 1.2e-dev 2024/01/02):
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

Current bug (2024/01/02): the first compilation will cause \ctanpkg{tagpdf} to
raise an error.  Next compilations are fine.  This will be fixed in due time,
and is at this stage only an inconvenience.

One can turn tagging on or off via \csb{etoctaggingon} and
\csb{etoctaggingoff}.  Of course the former will have any effect only if the
document has activated tagging (currently via \csa{DocumentMetadata}, see above
documentation).

The macros \csb{etocname} and \csb{etocpage} keep the same meaning whether
tagging is on or off.  The \csb{etocthenumber} also, because it may be used
in numerical contexts in some user line styles (although in general it may only
holds a textual representation of some numeric data).  So one should use the
new \csb{etocthetaggednumber}, if for some reason \csb{etocnumber} is not
usable.  The latter contains the specific tagging instructions too.

Currently the reason \csb{etocname} and \csb{etocpage} by themselves hold no
tagging instruction is because the whole \marg{prefix} and \marg{contents}
part of \csb{etocsetstyle} configuration have been prefixed and postfixed
by tagging commands.  Whether this gives correct results is to be seen.

The author has neither the time nor the resources nor the appropriate tools to
do any kind of testing beyond the most basic by himself.

Examples such as those in this documentation which construct first some data
via specific line styles using \csb{etocthename}, \csb{etocthenumber},
\csb{etocthepage}, which are then rendered in a second stage, once the whole
TOC has been parsed, via TikZ for example, will need to use
\csb{etoctaggingoff} locally and users are currently on their own to add
tagging manually to the TikZ (or whatever) rendering.
```

# License

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
