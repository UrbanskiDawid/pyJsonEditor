#!/bin/bash


WD=`git rev-parse --show-toplevel`/scripts/git_hooks
TARGET_DIR=`git rev-parse --show-toplevel`/.git/hooks

FN=(`find $WD -type f -not -name 'install.sh'`)

for f in $FN
do
  echo "installing $f"
  cp -v $f $TARGET_DIR
done
