import os, datetime

def make_paths(root_dir, component, qualified_name):
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
            # Beginning of source files listings in CMake.
            'source_begin_marker': 'set(BROKER_SRC',
            # Beginning of unit test listings in CMake.
            'test_begin_marker': 'set(tests',
            # Relative path to the source file for CMake.
            'source_path': rel_cpp,
            # Relative path to the unit test file for CMake.
            'test_path': rel_tst,
            # CMake entry for this test suite.
            'test_suite': rel_tst,
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
    # Extract the unqualified class name.
    class_name = namev[-1]
    # Return replacements for our template files.
    return {
        'class': class_name,
        'qualified-class': '.'.join(namev[1:]),
        'namespace': namespace,
        'hpp':  '/'.join(namev) + '.hh',
        'year': datetime.datetime.now().year
    }
