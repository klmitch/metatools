import inspect


__all__ = ['MetaClass']


class MetaMeta(type):
    @staticmethod
    def iter_bases(bases):
        """
        Performs MRO linearization of a set of base classes.  Yields
        each base class in turn.
        """

        sequences = ([list(inspect.getmro(base)) for base in bases] +
                     [list(bases)])

        # Loop over sequences
        while True:
            sequences = [seq for seq in sequences if seq]
            if not sequences:
                return

            # Select a good head
            for seq in sequences:
                head = seq[0]

                tails = [seq for seq in sequences if head in seq[1:]]
                if not tails:
                    break
            else:
                raise TypeError('Cannot create a consistent method '
                                'resolution order (MRO) for bases %s' %
                                ', '.join([base.__name__ for base in bases]))

            # Yield this base class
            yield head

            # Remove base class from all the other sequences
            for seq in sequences:
                if seq[0] == head:
                    del seq[0]

    @staticmethod
    def inherit_dict(base, namespace, attr_name,
                     inherit=lambda k, v: True):
        """
        Perform inheritance of dictionaries.  Returns a list of key
        and value pairs for values that were inherited, for
        post-processing.

        :param base: The base class being considered; see
                     iter_bases().
        :param namespace: The dictionary of the new class being built.
        :param attr_name: The name of the attribute containing the
                          dictionary to be inherited.
        :param inherit: Filtering function to determine if a given key
                        should be inherited.  If None, key will not be
                        added, but will be included in the returned
                        items.  If a function, key will be added and
                        included in the items list only if the
                        function returns True.  By default, all keys
                        are added and included in the items list.
        """

        items = []

        # Get the dicts to compare
        base_dict = getattr(base, attr_name, {})
        new_dict = namespace.setdefault(attr_name, {})
        for key, value in base_dict.items():
            # Skip keys that have been overridden or that we shouldn't
            # inherit
            if key in new_dict or (inherit and not inherit(key, value)):
                continue

            # Inherit the key
            if inherit:
                new_dict[key] = value

            # Save the item for post-processing
            items.append((key, value))

        return items

    @staticmethod
    def inherit_set(base, namespace, attr_name,
                    inherit=lambda i: True):
        """
        Perform inheritance of sets.  Returns a list of items that
        were inherited, for post-processing.

        :param base: The base class being considered; see
                     iter_bases().
        :param namespace: The dictionary of the new class being built.
        :param attr_name: The name of the attribute containing the set
                          to be inherited.
        :param inherit: Filtering function to determine if a given
                        item should be inherited.  If None, item will
                        not be added, but will be included in the
                        returned items.  If a function, item will be
                        added and included in the items list only if
                        the function returns True.  By default, all
                        items are added and included in the items
                        list.
        """

        items = []

        # Get the sets to compare
        base_set = getattr(base, attr_name, set())
        new_set = namespace.setdefault(attr_name, set())
        for item in base_set:
            # Skip items that have been overridden or that we
            # shouldn't inherit
            if item in new_set or (inherit and not inherit(item)):
                continue

            # Inherit the item
            if inherit:
                new_set.add(item)

            items.append(item)

        return items


class MetaClass(type):
    """
    Helper class for building metaclasses.  Provides static methods
    iter_bases(), inherit_dict(), and inherit_set(), without polluting
    the namespace of the class this is a metaclass for.
    """

    __metaclass__ = MetaMeta
