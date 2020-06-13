import numpy as np
import uuid
import db
# from health import calculate_final_stats

# automate this as well
opening_chars = ["\'", "\"", ")"]
string_trees = []

stats = db.init_stats("odds.json")

def create_string(command=10):
    """
    """
    id = uuid.uuid4()
    s = ""
    # automate this as well
    current_char = np.random.choice(opening_chars)
    s += current_char
    string_trees.append(db.new_string_tree(s, id))

    current_id = id
    current_prob = 0.0
    while len(s.split()) < command:
        s += " "
        s += np.random.choice(stats[current_char][0], replace=True, p=stats[current_char][1])

        # Comments with no further options, making the code get stuck
        if s[-1] in ["#"] or s[-2:] in ["--"]:
            return current_id, s
        # Avoiding duplicates
        if len(s) > 2:
            if s[-1] == s[-2] and s[-2] == s[-3]:
                s = s[:-1]

        new_id = uuid.uuid4()
        db.add_son(current_id, s, new_id)

        current_id = new_id
        current_char = s.split()[-1]
        # current_prob = calculate_final_stats(s)
        print(s, current_prob)

    return current_id, s

def new_string():
    """
    This function creates a new opening string.
    the function stores the string in  a new tree, and saves the tree in string_trees
    The function returns the string id, and the string itself
    """
    id = uuid.uuid4()
    s = ""

    # creating the string
    for i in range(random.randrange(1, 4)):
        s += np.random.choice([opts], replace=True, p=opening_odds)

    s += " "

    # making a tree for the string
    if db.is_created(s):
        return new_string() # Is there a better solution?

    string_trees.append(db.new_string_tree(s, id))

    return id, s

def add_command(id):
    """
    This function takes an id of an opening string, and creates a test string.
    The function stores the test string as a son in the tree
    The function returns the second id with the test string itself.
    """
    s_id = uuid.uuid4()
    s = db.get_value(id)

    s += random.choice(["AND", "OR", ""]) + " "
    s += random.choice(commands_group) + " "

    if db.is_created(s):
        return add_command(id) # Is there a better solution?

    db.add_son(id, s, s_id)

    return s_id, s

def add_comment(id):
    """
    The function gets the id of a string and adds a commnet to the string.
    The functon also saves the string as the son of the id node, in it's tree.
    The function returns the id and the result string
    """
    s_id = uuid.uuid4()
    s = db.get_value(id)

    s += random.choice(comment_group) + " "

    if db.is_created(s):
        return add_comment(id) # Is there a better solution?

    db.add_son(id, s, s_id)

    return s_id, s



if __name__ == '__main__':
    print(create_string()[1])