#!/bin/bash
printf "Total lines of insertion and deletion\n"
printf "add\tdelete\tsum\tauthor\n"
git log --pretty="%aN" | sort -u | while read author; do git log --author="$author" --pretty=tformat: --numstat -- $(git ls-files | grep -v "^.*data/.*") | awk '{ add += $1 ; subs += $2 ; loc += $1 + $2 } END { printf "%s\t%s\t%s\t",add,subs,loc }';printf "%s\n" "$author"; done
printf "Total lines of survival\n"
git ls-files | grep -v "^.*data/.*" | while read f; do git blame -w -M -C -C --line-porcelain "$f" | grep '^author '; done | sort -f | uniq -ic | sort -n
git fame -swCM --excl="^data"
printf 'weight=$(((commits * 5) + (files_changed * 10) + (lines_added * 5) - (lines_removed * 2) + (surviving_lines * 3)))\n'
