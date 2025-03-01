import singletons
import test_module


class A(singletons.SimpleSingleton):
    pass


class B(metaclass=singletons.MetaSingleton):
    pass


class C(metaclass=singletons.MetaSingleton):
    pass


a_obj = A()
same_a_obj = A()


b_obj = B()
same_b_obj = B()


c_obj = C()
same_c_obj = C()


if __name__ == "__main__":
    assert singletons.instance is test_module.instance
    assert len(singletons.MetaSingleton._instances) == 2
    assert a_obj is same_a_obj
    assert b_obj is same_b_obj
    assert c_obj is same_c_obj
