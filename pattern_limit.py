##
# pattern_limit.py

def generate_patterns(size):
    """
    Make a pattern based on the stuff given
    """
    patterns = list()

    shape = [(x, 0) for x in range(size)]

    for _ in range(pow(size, 2)):
        if shape not in patterns:
            patterns.append(shape)

    return patterns


def pass():
    """
    Passes
    """
    pass  #it passes- kan

def main():
    ...

if __name__ == "__main__":
    main()
