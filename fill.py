#!/opt/local/bin/python

tag = 'template'

def remove_pattern(s, pattern):
    import re
    return re.sub(pattern, '', s,)

def files_with_substring(s):
    return glob('*%s*' % s)

def fill_templates(files, data):
    from Cheetah.Template import Template
    return (str(Template(file=filename, searchList=data)) for filename in files)

# needs ability to define order and filenames, also to add custom parsers
def build_dict():
    import yaml
    data = {}
    try:
        import yaml
        with open('definitions.yaml','r') as f:
            data.update(yaml.load(f))
    except: pass
    try:
        import definitions
        data.update(definitions.__dict__)
    except: pass
    return data


def setup_working_dir():
    import os, sys
    sys.path.insert(1,os.getcwd())

if __name__ == '__main__':
    from glob import glob
    from itertools import izip

    # allow us to import from the working dir instead
    setup_working_dir()

    #opts to define definitions
    data = build_dict()

    in_files = files_with_substring(tag)
    out_files = (remove_pattern(filename, tag) for filename in in_files)
    outputs = izip(out_files, fill_templates(in_files, data))

    for (filename, output) in outputs:
        with open(filename, 'w') as f:
            f.write(str(output))
