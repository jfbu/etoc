# etoc

etoc.sty development repo and issue tracker

This repository:
- serves as an issue tracker for the current release of the [etoc](https://ctan.org/pkg/etoc) LaTeX package on [CTAN](https://ctan.org),
- provides snapshots of the current dev version of the package, allowing interested people to test it and report bugs or feature requests.

Please insert `@jfbu` inside your bug report else I may not be pinged.

The repository provides only `etoc.sty`, not the full `etoc.dtx` whose latest official release is only on CTAN.  But this version ot `etoc.sty` may contain deliberately comments which ultimately will be moved to the released `dtx` file.

[This diff](https://github.com/jfbu/etoc/compare/1.2d-2023-10-29...HEAD) compares current HEAD with latest CTAN release.

## Relative diffs

These diffs are with respect to the latest previous tag in this repo:

### [dev HEAD]

### [2024-01-05]

- fix jfbu/etoc#5 via a general deactivation of the minipage tagging sockets for the duration of the TOC contents.

- fix jfbu/etoc#4 thanks to @u-fischer's advice at latex3/tagging-project#54.  No more warnings at this stage!

- use `\Etoc@tagleaders` to mark as artifacts the dots in fall-back TOC line styles, in imitation of upstream `\@dottedtocline`.

- tentative `\Etoc@tagrule` added in various places (yet to be tested).

- rework indentation which had been catastrophic for ages in `\etocframedstyle` source code.

### [2024-01-03]

- refactor tagging support, fix jfbu/etoc#1, jfbu/etoc#2, jfbu/etoc#3.

- `\etocsetlinestyle` and `\etocfallbacklines` as respective aliases to `\etocsetstyle` and `\etocdefaultlines`.

### [2024-01-02]

- initial tagging support.


## PDF Tagging

Refer to the this PDF document (by Frank Mittelbach and Chris Rowley): [*LaTeX Tagged PDF—A blueprint for a large project*](https://www.latex-project.org/publications/2020-FMi-TUB-tb129mitt-tagpdf.pdf) for background information, and to the [latex3/tagging-project](https://github.com/latex3/tagging-project) and [latex3/tagpdf](https://github.com/latex3/tagpdf) repositories for current status of this upstream LaTeX project.

Here is a description from dev `etoc.dtx` of what is hoped for at this stage regarding this topic (this will be kept updated with `etoc.sty` pushes to this repo):

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

\begingroup\colorlet{shadecolor}{red!10}
\begin{shaded}
The author has neither the time nor the resources nor the appropriate tools to
do any kind of testing beyond the most basic by himself.

Besides he is mostly ignorant attow about tagging related matters.
\end{shaded}
\endgroup

Current status (as of 2024-01-05 1.2e dev):
\begin{itemize}
\item A document using only \toc and \localtoc, with \etoc left in
  compatibility mode for line styles should be tagged as can be hoped
  for documents not using \etoc facilities.  Indeed
  \etoc then does not at all interfere with the rendering of the
  \texttt{.toc} file data, apart from implementing the ``local toc''
  mechanism.  Potential problems:
  \begin{itemize}
  \item the tagging code from the kernel \csa{@starttoc} has been copied
    over manually by the author into \etoc source code, as it does not
    execute \csa{@starttoc}.  When upstream \LaTeX{} changes, \etoc has
    to be updated.
  \item if \csb{etocsettocstyle}, or higher level interface such as
    \csb{etocframedstyle}, has made \etoc leave the compatibility mode for the
    ``global display TOC style'', it may be that the user will have to add
    directly extra tagging code regarding the way for exemple the
    ``title'' of the TOC is rendered.
  \end{itemize}
\item The \etoc ``fallback'' line styles (see \csb{etocfallbacklines}) have
  been updated where needed and do not cause \ctanpkg{tagpdf} warnings in our
  brief testing; it remains to be seen if the tagging is actually correct.
\item A document using \csb{etocsetlinestyle} to define custom line
  styles using \csb{etocname}, \csb{etocnumber} and \csb{etocpage}
  should behave about correctly (as the latter have been extended to
  insert the suitable tagging code), but additional user mark-up may be
  needed to properly handle extra material such as dots or whatever,
  which perhaps should be marked as artifacts.  For this user has to use
  the \ctanpkg{tagpdf} internals.
\end{itemize}

\begingroup\colorlet{shadecolor}{red!10}
\begin{shaded}
  All user interface is to be considered currently unstable and may change at
any time.
\end{shaded}
\endgroup

\begin{description}
\item[\csb{etoctaggingon}] activates the tagging-related code from \etoc
  (this is done at begin document if document has activated tagging).  This is
  a no-op if document has not activated tagging.

  \csb{etocname}, \csb{etocnumber} and \csb{etocpage} will now accomplish
  tagging tasks, as will \csb{etoclink} and the non-robust \csb{etocthelink}.
  But \csb{etocthename}, \csb{etocthenumber}, and \csb{etocthepage} are kept
  as is, with no tagging.  This is especially important for \csb{etocthenumber}
  for backwards compatibility as it may be needed in some line styles as a
  numerical quantity.

\item[\csb{etoctaggingoff}] turns off (almost) all \etoc tagging-related
  code.

  As advanced \etoc users will be aware, it is possible with it to use
  the \toc and \localtoc commands to do things only remotely related to
  tables of contents per se, for example one can use it to count how
  many sections are contained in a chapter so the only result of
  execution of these commands is to update some counter or other
  user-defined macro to hold the result.  Use \csb{etoctaggingoff}
  before the \toc or \localtoc command then.

  Attow, this does \emph{not} deactivate turning off the \emph{minipage}
  tagging sockets, which currently seems required to fix
  \href{https://github.com/jfbu/etoc/issues/4}{etoc\#5}.  But in the use
  case from previous paragraph, this is irrelevant.

\item[\csb{etoctagginginlineoff}] is in case user employs
  \csb{etocsetlinestyle} to re-employ kernel macros such as
  |\@dottedtocline| or |\l@section|, see \autoref{sec:anothercompat}: it
  tells \etoc to free \csb{etocname}, \csb{etocnumber} and
  \csb{etocpage} from contributing any tagging data by themselves, as
  this will be inserted already by the used \LaTeX{} kernel macros where
  \csb{etocname} et al. have been reinserted.  It also turns off \etoc
  added hyperlinking because the kernel |\@dottedtocline| or
  |\l@section| will originate it by themselves if tagging has been
  activated in the document.

  This command (as \csb{etoctaggingoff}) is supposed to be used right
  before \toc or \localtoc.  It may (untested) also be used from inside
  the \marg{start} part of \csb{etocsetlinestyle} for
  a given sectioning name, it this is the only level using the \LaTeX{}
  kernel macros as per \autoref{sec:anothercompat}.  Then the
  \marg{finish} part may use \csb{etoctaggingon}.

  There is no \csa{etoctagginginlineon}, use \csb{etoctaggingon}.

\item[\csb{etoctagthis}] tags its argument  with label |tag=Reference|.
\end{description}


WARNING: \emph{the next paragraph may now be partially obsolete due to non
  documented yet \csa{etocthetaggedname} etc..., but an interface is at
  nay rate currently lacking to allow user
  to re-insert TOC and TOCI tags.}

Advanced usages of \etoc, such as those in this documentation which use \toc
or \localtoc to extract data from the \texttt{.toc} file, using
\csb{etocthename}, \csb{etocthenumber}, \csb{etocthepage}, which are then
rendered in a second stage, once the whole TOC has been parsed, via TikZ for
example, will need to use \csb{etoctaggingoff} locally and users are currently
on their own to add tagging manually to the TikZ (or whatever) rendering.
Attow \csb{etoctagthis} can only be used from inside the \marg{prefix} and
\marg{contents} arguments of \csb{etocsetstyle}.
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

[dev HEAD]: https://github.com/jfbu/etoc/compare/2024-01-05...HEAD
[2024-01-05]: https://github.com/jfbu/etoc/compare/2024-01-03...2024-01-05
[2024-01-03]: https://github.com/jfbu/etoc/compare/2024-01-02...2024-01-03
[2024-01-02]: https://github.com/jfbu/etoc/compare/1.2d-2023-10-29...2024-01-02
