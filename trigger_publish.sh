#!/bin/sh
current=`grep version pyproject.toml | cut -d' ' -f3`

echo $current
python3 -c "v=$current.split('.'); print(v)"

new=`python3 -c "v=$current.split('.'); v[2]=str(1+int(v[2])); print('.'.join(v))"`
echo "$current -> $new"
sed -i "s/^version.=.*/version = '$new'/" pyproject.toml
git diff pyproject.toml
#exit 1
git add pyproject.toml
git commit -m "net tag $new"
git tag -a $new -m "new tag $new"
git push --tag origin master
