# Copyright (C) 2012 by Kevin L. Mitchell <klmitch@mit.edu>
#
# This program is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see
# <http://www.gnu.org/licenses/>.

import inspect

import unittest2

import metatools


class IterBasesTest(unittest2.TestCase):
    # The examples here are drawn from the post available at
    # http://www.python.org/download/releases/2.3/mro/ which documents
    # the Python method resolution order (MRO).

    def test_cross_inheritance(self):
        # Example "zero", which I dub "cross-inheritance"; A and B
        # both inherit from X and Y, but in opposite orders.  Python
        # would raise TypeError when constructing a class C from bases
        # A and B in either order.

        class X(object):
            pass

        class Y(object):
            pass

        class A(X, Y):
            pass

        class B(Y, X):
            pass

        with self.assertRaises(TypeError):
            result = list(metatools.MetaMeta.iter_bases([A, B]))

        with self.assertRaises(TypeError):
            result = list(metatools.MetaMeta.iter_bases([B, A]))

    def test_example1(self):
        # Example one, given at the link above.

        class F(object):
            pass

        class E(object):
            pass

        class D(object):
            pass

        class C(D, F):
            pass

        class B(D, E):
            pass

        self.assertEqual(list(metatools.MetaMeta.iter_bases([object])),
                         [object])
        self.assertEqual(list(metatools.MetaMeta.iter_bases([D, E])),
                         [D, E, object])
        self.assertEqual(list(metatools.MetaMeta.iter_bases([D, F])),
                         [D, F, object])
        self.assertEqual(list(metatools.MetaMeta.iter_bases([B, C])),
                         [B, C, D, E, F, object])

    def test_example2(self):
        # Example two, given at the link above.

        class F(object):
            pass

        class E(object):
            pass

        class D(object):
            pass

        class C(D, F):
            pass

        class B(E, D):
            pass

        class A(B, C):
            pass

        self.assertEqual(list(metatools.MetaMeta.iter_bases([object])),
                         [object])
        self.assertEqual(list(metatools.MetaMeta.iter_bases([D, F])),
                         [D, F, object])
        self.assertEqual(list(metatools.MetaMeta.iter_bases([E, D])),
                         [E, D, object])
        self.assertEqual(list(metatools.MetaMeta.iter_bases([B, C])),
                         [B, E, C, D, F, object])


class InheritanceTest(unittest2.TestCase):
    def test_inherit_dict_delayed(self):
        class Base(object):
            the_dict = dict(a=1, b=2, c=3)

        namespace = dict(the_dict=dict(b=4, d=5))

        result = metatools.MetaMeta.inherit_dict(Base, namespace, 'the_dict',
                                                 None)

        self.assertEqual(dict(result), dict(a=1, c=3))
        self.assertEqual(namespace, dict(the_dict=dict(b=4, d=5)))

    def test_inherit_dict_simple(self):
        class Base(object):
            the_dict = dict(a=1, b=2, c=3)

        namespace = dict(the_dict=dict(b=4, d=5))

        result = metatools.MetaMeta.inherit_dict(Base, namespace, 'the_dict')

        self.assertEqual(dict(result), dict(a=1, c=3))
        self.assertEqual(namespace, dict(the_dict=dict(a=1, b=4, c=3, d=5)))

    def test_inherit_dict_nonexistant(self):
        class Base(object):
            the_dict = dict(a=1, b=2, c=3)

        namespace = {}

        result = metatools.MetaMeta.inherit_dict(Base, namespace, 'the_dict')

        self.assertEqual(dict(result), dict(a=1, b=2, c=3))
        self.assertEqual(namespace, dict(the_dict=dict(a=1, b=2, c=3)))

    def test_inherit_dict_filter(self):
        class Base(object):
            the_dict = dict(a=1, b=2, c=3)

        namespace = dict(the_dict=dict(b=4, d=5))

        inherit = lambda k, v: k not in set(['c'])
        result = metatools.MetaMeta.inherit_dict(Base, namespace, 'the_dict',
                                                 inherit)

        self.assertEqual(dict(result), dict(a=1))
        self.assertEqual(namespace, dict(the_dict=dict(a=1, b=4, d=5)))

    def test_inherit_set_delayed(self):
        class Base(object):
            the_set = set(['a', 'b', 'c'])

        namespace = dict(the_set=set(['b', 'd']))

        result = metatools.MetaMeta.inherit_set(Base, namespace, 'the_set',
                                                None)

        self.assertEqual(set(result), set(['a', 'c']))
        self.assertEqual(namespace, dict(the_set=set(['b', 'd'])))

    def test_inherit_set_simple(self):
        class Base(object):
            the_set = set(['a', 'b', 'c'])

        namespace = dict(the_set=set(['b', 'd']))

        result = metatools.MetaMeta.inherit_set(Base, namespace, 'the_set')

        self.assertEqual(set(result), set(['a', 'c']))
        self.assertEqual(namespace, dict(the_set=set(['a', 'b', 'c', 'd'])))

    def test_inherit_set_nonexistant(self):
        class Base(object):
            the_set = set(['a', 'b', 'c'])

        namespace = {}

        result = metatools.MetaMeta.inherit_set(Base, namespace, 'the_set')

        self.assertEqual(set(result), set(['a', 'b', 'c']))
        self.assertEqual(namespace, dict(the_set=set(['a', 'b', 'c'])))

    def test_inherit_set_filter(self):
        class Base(object):
            the_set = set(['a', 'b', 'c'])

        namespace = dict(the_set=set(['b', 'd']))

        inherit = lambda i: i not in set(['c'])
        result = metatools.MetaMeta.inherit_set(Base, namespace, 'the_set',
                                                inherit)

        self.assertEqual(set(result), set(['a']))
        self.assertEqual(namespace, dict(the_set=set(['a', 'b', 'd'])))
