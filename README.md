# pyJsonEdit

[![PyPi version](https://pypip.in/v/jsoneditor/badge.png)](https://crate.io/packages/jsoneditor/)
[![license](https://img.shields.io/github/license/Naereen/StrapDown.js.svg)]()
[![tests](https://github.com/UrbanskiDawid/pyJsonEditor/actions/workflows/tests.yaml/badge.svg)](https://github.com/UrbanskiDawid/pyJsonEditor/actions/workflows/tests.yaml)

[![](https://forthebadge.com/images/badges/made-with-python.svg)]()
[![](https://forthebadge.com/images/badges/powered-by-coffee.svg)]()
[![](https://forthebadge.com/images/badges/uses-badges.svg)]()
[![](https://forthebadge.com/images/badges/works-on-my-machine.svg)]()




Edit parts of inconsistently formatted json.

It's just a bit slower that doint this by hand!


## how to install

> pip install --upgrade pyjsonedit


# json in python

**Pure pyhon** implementation of json encoder/decoder.

Its slow and unnecessary!
# matcher

Now you can select **nodes** in json tree

syntax!

  *  | select all children in current node
-----|-----
 [n] | select n-th item of curent node
 {n} | select n-th item of curent node
 key | select node chilld by name 
"key"| select node chilld by name
 \>  | go to next node

## example: mask multiple nodes
> $ ./pyjsonedit/print_color **"quiz > * > q1 >*"** DOC/example.json

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

```bash
$ import pyjsonedit
$ pyjsonedit.string_match_mark("{'pass':123}","pass")
{'pass':XXX}
```
![](DOC/mask_pass.gif)[]()


