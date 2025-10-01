class TreeNode:
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent
        self.children = []
        self.id = self._generate_id()
        
        if parent:
            parent.children.append(self)
    
    def _generate_id(self):
        if self.parent is None:
            # Root node starts at 1.1
            return "1.1"
        
        parent_id = self.parent.id
        siblings = self.parent.children
        sibling_index = len(siblings)  # Current position among siblings
        
        # Determine the level (odd or even)
        # Count periods and letters to determine depth
        level = parent_id.count('.') + sum(c.isalpha() for c in parent_id)
        
        if level % 2 == 1:  # Odd level (ends with number) -> children get letters
            letter = chr(ord('a') + sibling_index)
            return f"{parent_id}{letter}"
        else:  # Even level (ends with letter) -> children get numbers
            return f"{parent_id}.{sibling_index + 1}"
    
    def add_child(self, name):
        return TreeNode(name, parent=self)
    
    def display(self, indent=0):
        print("  " * indent + f"{self.id}: {self.name}")
        for child in self.children:
            child.display(indent + 1)
    
    def __repr__(self):
        return f"TreeNode(id={self.id}, name={self.name})"


# Example usage
if __name__ == "__main__":
    # Create root
    root = TreeNode("Root")
    
    # Add siblings to root (1.2, 1.3)
    node_1_2 = TreeNode("Node 1.2", parent=root.parent if root.parent else None)
    node_1_3 = TreeNode("Node 1.3", parent=root.parent if root.parent else None)
    
    # Better approach: Create a tree with proper hierarchy
    print("Example Tree Structure:")
    print("=" * 50)
    
    # Level 0 (root): 1.1
    tree_root = TreeNode("Root")
    
    # Level 1 (children of 1.1): 1.1a, 1.1b, 1.1c
    child_a = tree_root.add_child("Child A")
    child_b = tree_root.add_child("Child B")
    child_c = tree_root.add_child("Child C")
    
    # Level 2 (children of 1.1a): 1.1a.1, 1.1a.2
    grandchild_1 = child_a.add_child("Grandchild 1")
    grandchild_2 = child_a.add_child("Grandchild 2")
    
    # Level 3 (children of 1.1a.1): 1.1a.1a, 1.1a.1b
    great_grandchild_a = grandchild_1.add_child("Great-Grandchild A")
    great_grandchild_b = grandchild_1.add_child("Great-Grandchild B")
    
    # Level 2 (more children of 1.1b): 1.1b.1
    grandchild_3 = child_b.add_child("Grandchild 3")
    
    # Level 3 (children of 1.1b.1): 1.1b.1a, 1.1b.1b, 1.1b.1c
    great_grandchild_c = grandchild_3.add_child("Great-Grandchild C")
    great_grandchild_d = grandchild_3.add_child("Great-Grandchild D")
    great_grandchild_e = grandchild_3.add_child("Great-Grandchild E")
    
    # Display the tree
    tree_root.display()
    
    print("\n" + "=" * 50)
    print("ID Pattern Explanation:")
    print("Level 0 (root): 1.1")
    print("Level 1: Letters appended (1.1a, 1.1b, 1.1c)")
    print("Level 2: Period + number (1.1a.1, 1.1a.2)")
    print("Level 3: Letters appended (1.1a.1a, 1.1a.1b)")
    print("Pattern continues alternating...")