from io import StringIO
from parse import parse
from tokenize import tokenize
from pprint import pprint


json_raw="""{
    "test1":  true  ,
    "arr":[1,2],
    "test2": { "name":1 }
}"""


if __name__ == '__main__':
    f = StringIO(json_raw)

    a = [i for i in tokenize(f)]
    ret = parse(a)
    pprint(ret)



def test_pass():
    assert True