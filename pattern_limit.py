##
# pattern_limit.py

def generate_patterns(size):
    """
    Make a pattern based on the stuff given
    """
    patterns = list()

    shape = [(x, 0) for x range(size)]

    while shape not in patterns:
        patterns.append(shape)


def main():
    pass  #it passes- kan

if __name__ == "__main__":
    main()
