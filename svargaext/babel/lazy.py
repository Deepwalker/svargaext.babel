# -*- coding: utf-8 -*-


class LazyString(object):
    __slots__ = ['_func', '_args', '_kwargs', '_value', '_lazy_hyper']

    def __init__(self, func, *args, **kwargs):
        # Avoid triggering our own __setattr__ implementation
        object.__setattr__(self, '_func', func)
        object.__setattr__(self, '_args', args)
        object.__setattr__(self, '_kwargs', kwargs)
        object.__setattr__(self, '_lazy_hyper', kwargs.get('hyper_lazy', True))
        if 'hyper_lazy' in kwargs:
            del kwargs['hyper_lazy']
        object.__setattr__(self, '_value', None)

    def value(self):
        if self._value:
            return self._value
        else:
            value = self._func(*self._args, **self._kwargs)
            if not self._lazy_hyper:
                object.__setattr__(self, '_value', value)
            return value

    value = property(value)

    def __contains__(self, key):
        return key in self.value

    def __nonzero__(self):
        return bool(self.value)

    def __dir__(self):
        return dir(self.value)

    def __iter__(self):
        return iter(self.value)

    def __len__(self):
        return len(self.value)

    def __str__(self):
        return str(self.value)

    def __unicode__(self):
        return unicode(self.value)

    def __add__(self, other):
        return self.value + other

    def __radd__(self, other):
        return other + self.value

    def __mod__(self, other):
        return self.value % other

    def __rmod__(self, other):
        return other % self.value

    def __mul__(self, other):
        return self.value * other

    def __rmul__(self, other):
        return other * self.value

    def __call__(self, *args, **kwargs):
        return self.value(*args, **kwargs)

    def __lt__(self, other):
        return self.value < other

    def __le__(self, other):
        return self.value <= other

    def __eq__(self, other):
        return self.value == other

    def __ne__(self, other):
        return self.value != other

    def __gt__(self, other):
        return self.value > other

    def __ge__(self, other):
        return self.value >= other

    def __delattr__(self, name):
        delattr(self.value, name)

#    def __getattr__(self, name):
#        return getattr(self.value, name)

    def __setattr__(self, name, value):
        setattr(self.value, name, value)

    def __delitem__(self, key):
        del self.value[key]

    def __getitem__(self, key):
        return self.value[key]

    def __setitem__(self, key, value):
        self.value[key] = value
