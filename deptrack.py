
import sys, os, argparse, re

_extensions = ['.h', '.c', '.hpp', '.cpp', '.cc']
_regex = ()

def _get_fnames(dir, exclude = []):

    for d in exclude + [dir]:
        if not os.path.exists(d) or not os.path.isdir(d):
            print(d)
            raise FileNotFoundError(f"Directory does not exists/is not available: {d}")

    result = []
    for (dirname, _, fnames) in os.walk(dir):

        skip = False
        for excluded in exclude:
            if os.path.commonpath([excluded]) == os.path.commonpath([excluded, dirname]):
                skip = True
                break
        if skip: continue

        for fname in fnames:
            (_, ext) = os.path.splitext(fname) 
            if ext in _extensions:
                path = os.path.join(dirname, fname)
                result.append(path)
    return result

def _get_includes(fname):

    lines = []

    if not os.path.exists(fname) or not os.path.isfile(fname):
        raise FileNotFoundError(f"File not found: {fname}")

    with open(fname) as file:
        lines = file.readlines()
    
    includes = []
    for line in lines:

        match_ = _regex.match(line)

        if match_ is None:
            continue

        groups = match_.groups()

        if None in groups:
            continue

        includes.append(groups[3])
        
    return includes
        

def _parse_args():

    # TODO: Add usage section
    parser = argparse.ArgumentParser(
        prog="deptrack"
    )

    parser.add_argument('path')
    parser.add_argument('-e', '--exclude', action='append')

    config = parser.parse_args()
    return config

def _connection_str(fname):

    # TODO: Use some sort of stringbuffer
    str = ''

    for include in _get_includes(fname):
        str += f"    \"{os.path.basename(include)}\" -> \"{os.path.basename(include)}\"\n"

    return str

if __name__ == '__main__':

    config = _parse_args()

    # TODO: Handle errors
    fnames = _get_fnames(config.path, config.exclude)

    _regex = re.compile('( *)#include( *)("|<)(.*)("|>)( *)')

    str = "digraph DependencyGraph {\nranksep=2\n"

    nodes = ""

    basefnames = [os.path.basename(name) for name in fnames]

    for fname in basefnames:
        nodes += f"    \"{fname}\"\n"

    connections = ""
    source_subg = "    subgraph {\n        rank=\"same\";\n"

    for fname in fnames:

        (_, ext) = os.path.splitext(fname)
        if ext in ['.c', '.cc', '.cpp']:
            source_subg += f"        \"{os.path.basename(fname)}\";\n"

        includes = _get_includes(fname)

        for include in includes:
            baseinclude = os.path.basename(include)
            if baseinclude not in basefnames:
                nodes +=  f"    \"{baseinclude}\"\n"

            connections += f"    \"{baseinclude}\" -> \"{os.path.basename(fname)}\"\n"

    str += nodes + "\n" + source_subg + '}\n\n' + connections + "}"

    with open("output.dot", "w") as output:
        output.write(str)