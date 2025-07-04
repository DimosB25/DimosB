import sys
import argparse
import random

class TreapStorage:
    def __init__(self, capacity):
        self.capacity = capacity
        self.nodes = [{'key': -1, 'prio': -1, 'left': i - 1, 'right': -1} for i in range(capacity)]
        self.available = capacity - 1
        self.root_idx = -1

    def allocate_node(self, key, prio):
        if self.available == -1:
            raise MemoryError("Treap storage exhausted")

        node_idx = self.available
        self.available = self.nodes[node_idx]['left']

        self.nodes[node_idx] = {
            'key': key,
            'prio': prio,
            'left': -1,
            'right': -1
        }

        return node_idx

    def add(self, current_idx, key, prio):
        if current_idx == -1:
            return self.allocate_node(key, prio)

        current = self.nodes[current_idx]

        if key < current['key']:
            current['left'] = self.add(current['left'], key, prio)

            if self.nodes[current['left']]['prio'] > current['prio']:
                current_idx = self.rotate_right(current_idx)
        else:
            current['right'] = self.add(current['right'], key, prio)

            if self.nodes[current['right']]['prio'] > current['prio']:
                current_idx = self.rotate_left(current_idx)

        return current_idx

    def rotate_left(self, idx):
        right_child = self.nodes[idx]['right']
        self.nodes[idx]['right'] = self.nodes[right_child]['left']
        self.nodes[right_child]['left'] = idx
        return right_child

    def rotate_right(self, idx):
        left_child = self.nodes[idx]['left']
        self.nodes[idx]['left'] = self.nodes[left_child]['right']
        self.nodes[left_child]['right'] = idx
        return left_child

    def display(self, idx=None, level=0):
        if idx is None:
            idx = self.root_idx
        if idx == -1:
            return

        node = self.nodes[idx]
        pad = "  " * level
        print(f"{pad}- [{idx}] key={node['key']}, prio={node['prio']}, L={node['left']}, R={node['right']}")

        if node['left'] != -1:
            self.display(node['left'], level + 1)
        if node['right'] != -1:
            self.display(node['right'], level + 1)


if __name__ == "__main__":
    treap = TreapStorage(capacity=10)

    sample_data = [
        (40, 100),
        (30, 90),
        (60, 70),
        (50, 60),
        (70, 50),
        (90, 40),
        (80, 80),
        (100, 30)
    ]

    for key, prio in sample_data:
        treap.root_idx = treap.add(treap.root_idx, key, prio)

    print("\nTreap structure after insertions:")
    treap.display()