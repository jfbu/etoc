#!/bin/bash

# export LATEX="latexmk -pdf" for using latexmk
latex="${LATEX:-pdflatex} -halt-on-error --interaction=batchmode "

shopt -s nullglob

starline="******************************************************************************"

status=0
errorfiles=""
nboffiles=0
nbofgoodfiles=0
nbofbadfiles=0

# pass any argument to let the script remove auxiliary files
# for example ./dotests.sh clean
# pass "no" as first argument to do not activate tagging,
# then pdflatex is used (latexmk requires -usepretex options...)
# for example ./dotests.sh no clean
if [ $# -eq 0 ]
then
    :
else
    if [ "$1" = "no" ]
    then
        echo -e "\033[1;31m"
        echo "$starline"
        echo "**** NOT DOING ANY TAGGING! AND IGNORING LATEXMK ENV VARIABLE!"
        echo -e "$starline\033[0m"
        latex="pdflatex -halt-on-error --interaction=batchmode \\def\\NOTAGGING{}\\input "
	shift
    fi
fi

if [ $# -gt 0 ]
then
    rm -f *.{aux,toc,log,div,lof,lot,out,ps,fls,fdb_latexmk}
fi

# execute tex only on committed files, allowing new ones to
# reside in directory while they are being manually tested
for file in $(git ls-files | grep tex)
do
    ((nboffiles+=1))
    $latex $file
    if [ $? -eq 0 ]
    then
        ((nbofgoodfiles+=1))
        echo -e "\033[32m"
        echo -e "ok pour $file\033[0m"
    else
        ((nbofbadfiles+=1))
        echo -e "\033[1;31m"
        echo "$starline"
        echo "**** PROBLÈME AVEC $file"
        echo -e "$starline\033[0m"
        status=1
        errorfiles="$errorfiles $file"
    fi
    echo ""
done

if [ $# -eq 0 ]
then
    :
else
    echo "N.B.: auxiliary files have all been removed before compilation"
fi

if [ $status -eq 0 ]
then
    echo -e "\033[32m==== Aucune erreur lors des compilations TeX.     ====\033[0m"
    echo -e "\033[32mFAIL=$nbofbadfiles, PASS=$nbofgoodfiles, TOTAL=$nboffiles\033[0m"
else
    echo -e "\033[1;31m!!!! PROBLÈMES AVEC $nbofbadfiles/$nboffiles TESTS:\033[0m"
    for file in $errorfiles
    do
        echo -e "\033[1;31m$file\033[0m"
        tail -n 20 $(basename $file .tex).log | head -n 10
    done
    echo -e "\033[1;31mFAIL=$nbofbadfiles, PASS=$nbofgoodfiles, TOTAL=$nboffiles\033[0m"
fi

exit $status

