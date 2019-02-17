import os

def get_component_path(root_dir, qualified_name):
    return os.path.join(root_dir, 'core')

def make_paths(root_dir, qualified_name):
    if not qualified_name.startswith('tenzir::'):
        raise Exception('qualified name must start with "tenzir::"')
    namev = qualified_name.split('::')
    if len(namev) < 2:
        raise Exception('qualified name does not contain a valid class name')
    # Extract the unqualified class name.
    class_name = namev[-1]
    # Compute paths to .cpp files relative to component directory.
    rel_cpp = os.path.join('src', '/'.join(namev[1:-1]), class_name + '.cpp')
    rel_tst = os.path.join('test', '/'.join(namev[1:-1]), class_name + '.cpp')
    # Get the absolute path to our component.
    component_dir = os.path.join(get_component_path(root_dir, qualified_name),
                                 component)
    return {
        # Absolute paths to generated files.
        'hpp': os.path.join(component_dir, '/'.join(namev[:-1]), class_name + '.hpp'),
        'cpp': os.path.join(component_dir, rel_cpp),
        'tst': os.path.join(component_dir, rel_tst),
        # CMake settings.
        'cmake': {
            # Path of the CMakeLists.txt
            'file': os.path.join(component_dir, 'CMakeLists.txt'),
            # Name of the sources variable in CMake.
            'source_var': 'libtenzir_sources',
            # Relative path to the source file for CMake.
            'source_path': rel_cpp,
            # Name of the unit test variable in CMake.
            'test_var': 'tests',
            # Relative path to the unit test file for CMake.
            'test_path': rel_tst,
        },
    }

def make_tpl_replacements(qualified_name):
    if not qualified_name.startswith('tenzir::'):
        raise Exception('qualified name must start with "tenzir::"')
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
        'namespace': namespace,
        'hpp':  '/'.join(namev) + '.hpp',
    }

