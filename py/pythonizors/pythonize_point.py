def pythonize_gbl_point(klass, name):
    if name == 'Point':

        def __iter__(self):
            yield self.x
            yield self.y
        
        klass.__iter__ = __iter__
        klass.__repr__ = lambda self: repr(tuple(self))
