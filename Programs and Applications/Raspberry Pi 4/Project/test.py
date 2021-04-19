def test(*args, **kwargs):
    print("args: ", args)
    print("kwargs: ", kwargs)
    print(kwargs["test"])


test(test1="test")
