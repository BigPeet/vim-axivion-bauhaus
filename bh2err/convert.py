def convert_to_dicts(path, version):
    print("Path:", path)
    print("Version:", version)

    # Return some mock data for testing
    return [{"filename" : "README.md",
        "lnum" : "10",
        "col" : "2",
        "text" : "You've done goofed.",
        "type" : "E"}]
