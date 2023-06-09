import math

from node.utils import calculate_hash


class Node:
    def __init__(self, value:int, left_child=None, right_child=None):
        self.value = value
        self.left_child = left_child
        self.right_child = right_child


def is_pow_2(num_of_leaves:int) -> bool:
    result = math.log2(num_of_leaves).is_integer()
    return result

def compute_tree_depth(number_of_leaves:int) -> int:
    result = math.ceil(math.log2(number_of_leaves))
    return result

def build_merkle_tree(node_data: list[str]) -> Node:
    old_set_of_nodes = [Node(calculate_hash(data)) for data in node_data]
    tree_depth = compute_tree_depth(len(old_set_of_nodes))

    for i in range(0, tree_depth):
        num_nodes = 2**(tree_depth - 1)
        new_set_of_nodes = []
        for j in range(0, num_nodes, 2):
            child_node_0 = old_set_of_nodes[i]
            child_node_1 = old_set_of_nodes[j + 1]
            new_node = Node(value=calculate_hash(f'{child_node_0.value}{child_node_1.value}'),
                            left_child=child_node_0,
                            right_child=child_node_1)
            new_set_of_nodes.append(new_node)
        old_set_of_nodes = new_set_of_nodes
    return new_set_of_nodes[0]


def fill_set(list_of_nodes):
    current_number_of_leaves = len(list_of_nodes)
    if is_pow_2(current_number_of_leaves):
        return list_of_nodes
    total_num_leaves = 2**(compute_tree_depth(current_number_of_leaves))
    if current_number_of_leaves % 2 == 0:
        for i in range(current_number_of_leaves, total_num_leaves, 2):
            list_of_nodes = list_of_nodes + [list_of_nodes[-2], list_of_nodes[-1]]
    else:
        for i in range(current_number_of_leaves, total_num_leaves, 2):
            list_of_nodes.append(list_of_nodes[-1])
    return list_of_nodes