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


class TreeBuilder:
    """Build a tree from various input formats"""
    
    @staticmethod
    def from_dict(data):
        """
        Build tree from nested dictionary structure.
        Format: {"name": "Node Name", "children": [...]}
        """
        def build_node(node_data, parent=None):
            node = TreeNode(node_data["name"], parent=parent)
            
            if "children" in node_data:
                for child_data in node_data["children"]:
                    build_node(child_data, parent=node)
            
            return node
        
        return build_node(data)
    
    @staticmethod
    def from_nested_dict(data):
        """
        Build tree from simple nested dictionary.
        Format: {"Parent": {"Child1": {}, "Child2": {"Grandchild": {}}}}
        """
        def build_node(name, children_dict, parent=None):
            node = TreeNode(name, parent=parent)
            
            for child_name, grandchildren in children_dict.items():
                build_node(child_name, grandchildren, parent=node)
            
            return node
        
        # Get root name and children
        root_name = list(data.keys())[0]
        root_children = data[root_name]
        
        return build_node(root_name, root_children)
    
    @staticmethod
    def from_indented_text(text):
        """
        Build tree from indented text structure.
        Each line represents a node, indentation shows hierarchy.
        Example:
            Root
              Child A
                Grandchild 1
              Child B
        """
        lines = [line.rstrip() for line in text.strip().split('\n') if line.strip()]
        
        def get_indent_level(line):
            return len(line) - len(line.lstrip())
        
        if not lines:
            return None
        
        # Create root
        root = TreeNode(lines[0].strip())
        stack = [(get_indent_level(lines[0]), root)]
        
        for line in lines[1:]:
            indent = get_indent_level(line)
            name = line.strip()
            
            # Find parent by popping stack until we find correct indent level
            while stack and stack[-1][0] >= indent:
                stack.pop()
            
            if stack:
                parent = stack[-1][1]
                node = TreeNode(name, parent=parent)
                stack.append((indent, node))
        
        return root
    
    @staticmethod
    def from_paths(paths):
        """
        Build tree from list of paths.
        Example: ["Root/Child A/Grandchild 1", "Root/Child A/Grandchild 2", "Root/Child B"]
        """
        if not paths:
            return None
        
        # Find or create node by path
        nodes = {}
        root = None
        
        for path in paths:
            parts = [p.strip() for p in path.split('/')]
            
            for i, part in enumerate(parts):
                current_path = '/'.join(parts[:i+1])
                
                if current_path not in nodes:
                    if i == 0:
                        # Root node
                        node = TreeNode(part)
                        nodes[current_path] = node
                        if root is None:
                            root = node
                    else:
                        # Child node
                        parent_path = '/'.join(parts[:i])
                        parent = nodes[parent_path]
                        node = TreeNode(part, parent=parent)
                        nodes[current_path] = node
        
        return root


# Example usage
if __name__ == "__main__":
    print("=" * 60)
    print("METHOD 1: Building from nested dictionary with 'children' key")
    print("=" * 60)
    
    tree_data = {
        "name": "Root",
        "children": [
            {
                "name": "Child A",
                "children": [
                    {
                        "name": "Grandchild 1",
                        "children": [
                            {"name": "Great-Grandchild A"},
                            {"name": "Great-Grandchild B"}
                        ]
                    },
                    {"name": "Grandchild 2"}
                ]
            },
            {
                "name": "Child B",
                "children": [
                    {
                        "name": "Grandchild 3",
                        "children": [
                            {"name": "Great-Grandchild C"},
                            {"name": "Great-Grandchild D"}
                        ]
                    }
                ]
            },
            {"name": "Child C"}
        ]
    }
    
    tree1 = TreeBuilder.from_dict(tree_data)
    tree1.display()
    
    print("\n" + "=" * 60)
    print("METHOD 2: Building from simple nested dictionary")
    print("=" * 60)
    
    simple_tree = {
        "Root": {
            "Child A": {
                "Grandchild 1": {
                    "Great-Grandchild A": {},
                    "Great-Grandchild B": {}
                },
                "Grandchild 2": {}
            },
            "Child B": {
                "Grandchild 3": {}
            },
            "Child C": {}
        }
    }
    
    tree2 = TreeBuilder.from_nested_dict(simple_tree)
    tree2.display()
    
    print("\n" + "=" * 60)
    print("METHOD 3: Building from indented text")
    print("=" * 60)
    
    text_tree = """
Root
  Child A
    Grandchild 1
      Great-Grandchild A
      Great-Grandchild B
    Grandchild 2
  Child B
    Grandchild 3
  Child C
    """
    
    tree3 = TreeBuilder.from_indented_text(text_tree)
    tree3.display()
    
    print("\n" + "=" * 60)
    print("METHOD 4: Building from path list")
    print("=" * 60)
    
    paths = [
        "Root/Child A/Grandchild 1/Great-Grandchild A",
        "Root/Child A/Grandchild 1/Great-Grandchild B",
        "Root/Child A/Grandchild 2",
        "Root/Child B/Grandchild 3",
        "Root/Child C"
    ]
    
    tree4 = TreeBuilder.from_paths(paths)
    tree4.display()
    
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