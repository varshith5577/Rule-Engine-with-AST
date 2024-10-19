import operator

# Define supported operators and functions for rule evaluation
OPERATORS = {
    'AND': operator.and_,
    'OR': operator.or_,
    '>': operator.gt,
    '<': operator.lt,
    '>=': operator.ge,
    '<=': operator.le,
    '==': operator.eq,
    '!=': operator.ne,
}

class Node:
    """
    Represents a node in the Abstract Syntax Tree (AST).
    """
    def __init__(self, node_type, left=None, right=None, value=None):
        self.type = node_type 
        self.left = left    
        self.right = right   
        self.value = value    

    def __repr__(self):
        return f"Node(type={self.type}, value={self.value})"

# Helper function to check if the token is an operator
def is_operator(token):
    return token.upper() in OPERATORS

# Parser: Create AST from a rule string
def create_rule(rule_string):
    """
    Parse the rule string and return the root node of the corresponding AST.
    This function parses simple expressions like 'age > 30 AND department == "Sales"'
    """
    tokens = rule_string.replace('(', '').replace(')', '').split()  
    stack = []
    current_node = None

    for token in tokens:
        if is_operator(token):
            current_node = Node("operator", value=token.upper())
            if len(stack) >= 2:
                current_node.right = stack.pop()
                current_node.left = stack.pop()
            stack.append(current_node)
        elif token.isnumeric():
            stack.append(Node("operand", value=int(token)))
        elif token.startswith('"') and token.endswith('"'):  
            stack.append(Node("operand", value=token.strip('"')))
        elif token.isidentifier():
            stack.append(Node("operand", value=token))
    
    if not stack:
        raise ValueError("Invalid rule string, could not form an AST")

    return stack[-1] if stack else None


# Combine multiple rules into a single AST
def combine_rules(rules):
    """
    Combines multiple rules into a single AST using 'AND' or 'OR' operators.
    """
    if not rules:
        return None

    combined_node = rules[0]
    for rule in rules[1:]:
        combined_node = Node("operator", left=combined_node, right=rule, value="AND")
    return combined_node


def evaluate_rule(node, data):
    """
    Recursively evaluates the AST based on the provided data.
    """
    if node is None:
        raise ValueError("The node cannot be None")

    if node.type == "operand":
        if isinstance(node.value, str) and node.value in data:
            return data[node.value]
        return node.value

    elif node.type == "operator":
        left_value = evaluate_rule(node.left, data)
        right_value = evaluate_rule(node.right, data)

        if node.value in OPERATORS:
            operator_func = OPERATORS[node.value]
            if node.value in ['AND', 'OR']:
                return operator_func(bool(left_value), bool(right_value))
            return operator_func(left_value, right_value)

    return False


# Utility to print the AST (for debugging purposes)
def print_ast(node, level=0):
    """
    Utility to print the AST for visualization.
    """
    if node is not None:
        print("  " * level + f"{node.value}")
        print_ast(node.left, level + 1)
        print_ast(node.right, level + 1)


# Example Test Cases

rule1 = create_rule('age > 30 AND department == "Sales"')

rule2 = create_rule('age < 25 AND department == "Marketing"')

combined_rule = combine_rules([rule1, rule2])

# Test data
user_data1 = {
    "age": 35,
    "department": "Sales",
    "salary": 60000,
    "experience": 3
}

user_data2 = {
    "age": 22,
    "department": "Marketing",
    "salary": 55000,
    "experience": 2
}

# Evaluate the combined rule
print("User 1 matches rule:", evaluate_rule(combined_rule, user_data1))  
print("User 2 matches rule:", evaluate_rule(combined_rule, user_data2))  

# Print the AST for visualization
print("AST for Combined Rule:")
print_ast(combined_rule)
