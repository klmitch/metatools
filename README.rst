===================================
Python Metaclass Construction Tools
===================================

This package contains the ``metatools`` module, which provides a
utility class (``MetaClass``) which metaclasses can extend.  It
provides three static methods (available only on classes inheriting
from ``MetaClass``; they will not clutter up your actual classes)
which can be used to enhance inheritance.

The most important of these static methods is the ``iter_bases()``
method.  When passed a list of base classes, such as those passed to
the ``__new__()`` method, it generates a list of the superclasses in
proper Python Method Resolution Order.  This can be used with the
``inherit_dict()`` and ``inherit_set()`` static methods.

Both ``inherit_dict()`` and ``inherit_set()`` have similar interfaces.
When passed a base class, the dictionary for the class being
constructed, and the name of an attribute containing the dictionary or
set which should have inheritance rules applied, they look up the
attribute in both the base class and in the namespace dictionary, then
walk through all entries in the base class's version; if the entry
does not currently exist in the namespace's version of that dictionary
or set, then it is automatically added.  Both routines return a list
of items added, if the metaclass needs to perform any additional
post-processing on the entries.  The items may also be filtered by
passing a callable returning ``True`` or ``False`` as the ``inherit``
parameter to the routines.  Additionally, if ``inherit`` is ``False``
or ``None`` (or any other value that tests as ``False``), then the
items are not automatically added to the dictionary or set, but are
still provided in the list of returned items.
