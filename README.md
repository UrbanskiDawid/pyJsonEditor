# pyJsonEdit

[![PyPi version](https://badge.fury.io/py/pyjsonedit.svg)](https://pypi.org/project/pyjsonedit/)
[![license](https://img.shields.io/github/license/Naereen/StrapDown.js.svg)]()
[![tests](https://github.com/UrbanskiDawid/pyJsonEditor/actions/workflows/tests.yaml/badge.svg)](https://github.com/UrbanskiDawid/pyJsonEditor/actions/workflows/tests.yaml)

[![](https://forthebadge.com/images/badges/made-with-python.svg)]()
[![](https://forthebadge.com/images/badges/powered-by-coffee.svg)]()
[![](https://forthebadge.com/images/badges/uses-badges.svg)]()


Edit parts of inconsistently formatted json.

It's just a bit slower that doing this by hand!

# matcher

Now you can easly select **nodes** in json tree

syntax:

selector | action | node type
---------|--------|-------
  *| select **all** items in current node| -
 [n] | select **n-th** item of curent node| array
 {n} | select **n-th** item of curent node| object
 key | select node chilld **by name**| object
"key"| select node chilld **by name**| object
 \>  | mark current node as seleced |-
 a=b | check if current node has child 'a' with value 'b' |object


example 1: 

```
key > [0]
```

this pattern will match one element by:

1. selecting "key" element in root node (assuring that is an object)
2. select first element in it (assumintg its an array) 

example 2: 

```
name > *
```

this pattern will match multiple elements by:

1. selecting "name" element in root node (assuring that is an object)
2. select all element in it 

## how to install

```bash
pip install --upgrade pyjsonedit
```

## python module

```python
import pyjsonedit
```
## comand line - mark

```sh
$ pyjsonedit-mask --help
```

```
Usage: pyjsonedit-mask [OPTIONS] PATTERN [JSONS]...

  Select and mask parts of json

Options:
  --symbol TEXT
  -i, --insert   save changes to file
  --help         Show this message and exit.
```

example:
```
pyjsonedit-mask "pass" "{'pass':123}"
{'pass':XXX}
```
## comand line - modify

```sh
$ pyjsonedit-modify --help
```
```
Usage: pyjsonedit-modify [OPTIONS] PATTERN TEMPLATE [JSONS]...

  select and modify parts of json

Options:
  -i, --insert  save changes to file
  --help        Show this message and exit.
```

example 1: simple string
```
pyjsonedit-modify "pass" 'P@$W&$d' "{'pass':123}"
{'pass':P@$W&$d}
```

example 2: python code:

file **/home/dave/somefile.py**
```python
#!/usr/bin/python3
def modify(node,ctx):
   return "'<"+str(1)+">'"
```
node - matched node

ctx - context in witch node was matched: file_name & match_nr

```bash
pyjsonedit-modify "*" /home/dave/somefile.py "{'a':1}"
{'a':'<1>'}
```

## example: mask multiple nodes
```
$ pyjsonedit-mask **"quiz > * > q1 >*"** DOC/example.json
```

```
{
    "quiz": {
        "sport": {
            "q1": {
                "question": XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX,
                "options": XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX,
                "answer": XXXXXXXXXXXXXXX
            }
        },
        "maths": {
            "q1": {
                "question": XXXXXXXXXXX,
                "options": XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX,
                "answer": XXXX
            },
            "q2": {
                "question": "12 - 8 = ?",
                "options": [
                    "1",
                    "2",
                    "3",
                    "4"
                ],
                "answer": "4"
            }
        }
    }
}
```

## example: mask selected nodes

```python
$ import pyjsonedit
$ pyjsonedit.string_match_mark("{'pass':123}","pass")
{'pass':XXX}
```

[![string_match_mark](https://github.com/UrbanskiDawid/pyJsonEditor/raw/master/DOC/mask_pass.gif)]()


## project stats

[![string_match_mark](https://github.com/UrbanskiDawid/pyJsonEditor/raw/master/DOC/stats_boilerplate.png)]()