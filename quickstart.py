class MyClass:
    is_true = True

    def __init__(self, **kwargs):
        self.__dict__.update(**kwargs)

foo = MyClass(version="1.0", is_true=False)
print(foo.version)
print(foo.is_true)
print(MyClass.is_true)
