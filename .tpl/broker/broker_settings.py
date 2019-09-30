import os, datetime

def make_paths(root_dir, qualified_name):
    if not qualified_name.startswith('broker::'):
        raise Exception('qualified name must start with "broker::"')
    namev = qualified_name.split('::')
    if len(namev) < 2:
        raise Exception('qualified name does not contain a valid class name')
    # Extract the unqualified class name.
    class_name = namev[-1]
    # Compute paths to .cpp files relative to component directory.
    rel_cpp = os.path.join('src', '/'.join(namev[1:-1]), class_name + '.cc')
    rel_tst = os.path.join('cpp', '/'.join(namev[1:-1]), class_name + '.cc')
    # Get the absolute path to our component.
    component_dir = os.path.join(root_dir, "broker")
    return {
        # Absolute paths to generated files.
        'hpp': os.path.join(component_dir, "include", '/'.join(namev[:-1]), class_name + '.hh'),
        'cpp': os.path.join(component_dir, rel_cpp),
        'tst': os.path.join(component_dir, 'tests', rel_tst),
        # CMake settings.
        'cmake': {
            # Path of the CMakeLists.txt.
            'file': os.path.join(component_dir, 'CMakeLists.txt'),
            # Path of the CMakeLists.txt for the unit tests.
            'test_file': os.path.join(component_dir, 'tests', 'CMakeLists.txt'),
            # Name of the sources variable in CMake.
            'source_var': 'BROKER_SRC',
            # Name of the unit test variable in CMake.
            'test_var': 'tests',
            # Relative path to the source file for CMake.
            'source_path': rel_cpp,
            # Relative path to the unit test file for CMake.
            'test_path': rel_tst,
        },
    }

def make_tpl_replacements(qualified_name):
    if not qualified_name.startswith('broker::'):
        raise Exception('qualified name must start with "broker::"')
    namev = qualified_name.split('::')
    if len(namev) < 2:
        raise Exception('qualified name does not contain a valid class name')
    # Extract the namespace without the class name.
    namespace = '::'.join(namev[:-1])
    ns_open = "\n".join(map(lambda x: 'namespace ' + x + ' {', namev[:-1]))
    ns_close = "\n".join(map(lambda x: '} // namespace ' + x, reversed(namev[:-1])))
    # Extract the unqualified class name.
    class_name = namev[-1]
    # Return replacements for our template files.
    return {
        'class': class_name,
        'open-namespaces': ns_open,
        'close-namespaces': ns_close,
        'hpp':  '/'.join(namev) + '.hh',
        'header-guard':  ('_'.join(namev) + '_HH').upper(),
        'year': datetime.datetime.now().year
    }
