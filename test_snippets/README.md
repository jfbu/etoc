# Snippets

[etoc.pdf](https://ctan.org/pkg/etoc) comes (at release 1.2d 2023/10/29) with 26 code snippets illustrating various usages of  etoc.

We have copied them here with a shared preamble to set up tests.  At time of writing 11 of the 26 had to be excluded because they may use another document class, or define commands which have to be used rather than `\tableofcontents`, in which case we can probably later add them to the files included in the actual testing.  All sources have suffix `.txt` and the tested files are those for which a `.tex` symlink has been defined and added to the version control.

Use

- ``./dotests.sh`` to execute the test,
- ``./dotests.sh clean`` to have it remove aux files first,
- ``./dotests.sh no`` to not activate tagging.

In the latter case the env variable ``LATEX`` is ignored, else you can set it to e.g ``latexmk -pdf --silent`` to be (about) sure that enough compilations are made to catch warnings.
