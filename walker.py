import abc
import logging
import utils

log = logging.getLogger(__name__)
log.setLevel('DEBUG')


class Walker(abc.ABC):
    def __init__(self, root):
        """
        Args:
            root (Container): The root container
        """
        self.list = [root]


    @abc.abstractmethod
    def add(self, element):
        """Adds an element to the data structure.

        Args:
            element (object): Element to add to the walker
        """
        raise NotImplementedError

    @abc.abstractmethod
    def next(self):
        """Returns the next element from the walker.

        Returns:
            Container|FileEntry
        """
        raise NotImplementedError

    def get_children(self, element):
        """Returns children of the element.

        Args:
            element (Container)

        Returns:
            list: the children of the element
        """
        children = []
        container_type = element.container_type

        if container_type == 'file':
            return children

        children += element.files

        if container_type != 'analysis':
            # children += element.analyses
            if container_type == 'project':
                children += element.subjects()
            elif container_type == 'subject':
                children += element.sessions()
            elif container_type == 'session':
                children += element.acquisitions()

        log.debug('Children of element %s are:\n%s', element.id, children)
        return children

    def is_empty(self):
        """Returns True if the walker is empty.

        Returns:
            bool
        """
        return len(self.list) == 0

    def walk(self):
        """Walks the hierarchy from a root container.

        Yields:
            Container|FileEntry
        """

        while not self.is_empty():
            yield self.next()


class DepthFirstWalker(Walker):
    def add(self, element):
        """Adds an element to the data structure.

        Args:
            element (object): Element to add to the walker
        """
        self.list.append(element)

    def next(self):
        """Returns the next element from the walker and adds its children.

        Returns:
            Container|FileEntry
        """
        next_element = self.list.pop()
        log.debug('Element returned is %s', type(next_element))
        for child in self.get_children(next_element):
            self.add(child)
        return next_element


class BreadthFirstWalker(Walker):
    def add(self, element):
        """Adds an element to the data structure.

        Args:
            element (object): Element to add to the walker
        """
        self.list.append(element)

    def next(self):
        """Returns the next element from the walker and adds its children.

        Returns:
            Container|FileEntry
        """
        next_element = self.list.pop(0)
        for child in self.get_children(next_element):
            self.add(child)
        return next_element

