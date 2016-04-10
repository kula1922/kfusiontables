from collections import Iterable


def flatten(elements):
    new_elements = []
    for element in elements:
        if isinstance(element, Iterable) and not isinstance(element, str):
            new_elements += flatten(element)
        else:
            new_elements.append(element)
    return new_elements
