#!/usr/bin/env python3
import sys


class Node_Tree_Element(object):
    """individual element of the node tree
    These objects contain node information such as left child, right child,
    level on the tree and node integer value
    """
    def __init__(self, node_value):
        assert isinstance(node_value, int)
        self.__node_level = None
        self.__node_value = node_value
        self.__best_path_down = None
        self.__left_child = None
        self.__right_child = None

    def get_nl(self):
        return self.__node_level

    def set_nl(self, node_level):
        assert isinstance(node_level, int)
        assert node_level > -1
        self.__node_level = node_level

    def del_nl(self):
        pass

    node_level = property(get_nl, set_nl, del_nl)

    def get_nv(self):
        return self.__node_value

    def set_nv(self, node_value):
        assert isinstance(node_value, int)
        assert node_value > -1
        self.__node_value = node_value

    def del_nv(self):
        pass

    node_value = property(get_nv, set_nv, del_nv)

    def get_bpd(self):
        return self.__best_path_down

    def set_bpd(self, best_path_down):
        assert isinstance(best_path_down, str)
        self.__best_path_down = best_path_down

    def del_bpd(self):
        pass

    best_path_down = property(get_bpd, set_bpd, del_bpd)

    def get_lc(self):
        return self.__left_child

    def set_lc(self, left_child):
        assert isinstance(left_child, int)
        assert left_child > 0
        self.__left_child = left_child

    def del_lc(self):
        pass

    left_child = property(get_lc, set_lc, del_lc)

    def get_rc(self):
        return self.__right_child

    def set_rc(self, right_child):
        assert isinstance(right_child, int)
        assert right_child > 0
        self.__right_child = right_child

    def del_rc(self):
        pass

    right_child = property(get_rc, set_rc, del_rc)


class Node_Tree(list):
    """this class is an extension of the list class
    set to only allow Node_Tree_Elements in it
    """

    def append(self, *args, **kwargs):
        assert isinstance(args[0], Node_Tree_Element)
        return list.append(self, *args, **kwargs)

    def insert(self, *args, **kwargs):
        assert isinstance(args[0], Node_Tree_Element)
        return list.insert(self, *args, **kwargs)


def main(argv=None):

    file_name = argv
    number_of_levels = 0
    number_of_elements = 0
    nt = Node_Tree()

    # load text files into the tree by creating elements based on input
    # file contains lines with numbers, each line new level
    # file must contain only valid integers with separating space
    with open(file_name, encoding='utf-8') as file_in:
        for line_in in file_in:
            # remove trailing newline, etc.
            line_in = line_in.rstrip()
            split_line = line_in.split(" ")
            for value_in in split_line:
                nte = Node_Tree_Element(int(value_in))
                nte.node_level = number_of_levels
                number_of_elements += 1
                nt.append(nte)
            number_of_levels += 1

    # now that all of the values are in the tree the left and right children
    # locations need to be set so the tree can be traversed
    # the last level - leaf nodes will be left null
    this_element = 0
    this_level = 0
    add_child_pointers_below_these_levels = number_of_levels - 1

    # only up to last level
    while this_level < add_child_pointers_below_these_levels:
        # left and right children are determined by a calculation to determine
        # position in the tree based on input file
        lc_position = this_element + this_level + 1
        rc_position = lc_position + 1
        nt[this_element].left_child = lc_position
        nt[this_element].right_child = rc_position
        this_element += 1
        this_level = nt[this_element].node_level

    # start at last node and roll up the best path for each node based on
    # the either the left or right child
    # use number of elements for relative subscript so decrease by 1
    max_nodes = number_of_elements - 1
    for i in range(max_nodes, -1, -1):
        lc = nt[i].left_child
        rc = nt[i].right_child
        new_node_value = 0
        if ((lc == None) or (rc == None)):
            # the bottom nodes have no children
            new_node_value = nt[i].node_value
            new_best_path_down = "\n" \
                + str(nt[i].node_value) \
                + " at node " \
                + str(i) \
                + " on level " \
                + str(nt[i].node_level)
        else:
            if (nt[lc].node_value > nt[rc].node_value):
                new_node_value = nt[i].node_value + nt[lc].node_value
                new_best_path_down = "\n" \
                    + str(nt[i].node_value) \
                    + " at node " \
                    + str(i) \
                    + " on level " \
                    + str(nt[lc].node_level) \
                    + str(nt[lc].best_path_down)
            else:
                new_node_value = nt[i].node_value + nt[rc].node_value
                new_best_path_down = "\n" \
                    + str(nt[i].node_value) \
                    + " at node " \
                    + str(i) \
                    + " on level " \
                    + str(nt[rc].node_level) \
                    + str(nt[rc].best_path_down)
        nt[i].node_value = new_node_value
        nt[i].best_path_down = new_best_path_down

    with open("solution.txt", "w") as solution_file:
        solution_file.write("Max Value is " + str(nt[0].node_value) + "\n")
        solution_file.write("The Best Path chosen was: " \
                            + str(nt[0].best_path_down))

    return 0


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.stderr.write("no file name provided")
    else:
        main(sys.argv[1])
    sys.exit()
