import os, datetime

def make_paths(root_dir, component, qualified_name):
    if not qualified_name.startswith('caf::'):
        raise Exception('qualified name must start with "caf::"')
    namev = qualified_name.split('::')
    if len(namev) < 2:
        raise Exception('qualified name does not contain a valid class name')
    # Extract the unqualified class name.
    class_name = namev[-1]
    # Compute paths to .cpp files relative to component directory.
    rel_cpp = os.path.join('src', class_name + '.cpp')
    rel_tst = os.path.join('test', class_name + '.cpp')
    # Get the absolute path to our component.
    component_dir = os.path.join(root_dir, component)
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
            'source_var': component.upper() + '_SRCS',
            # Relative path to the source file for CMake.
            'source_path': rel_cpp,
        },
    }

def get_component(qualified_name):
    if qualified_name.startswith('caf::io'):
        return 'libcaf_io'
    if qualified_name.startswith('caf::openssl'):
        return 'libcaf_openssl'
    if qualified_name.startswith('caf::opencl'):
        return 'libcaf_opencl'
    return 'libcaf_core'

def make_tpl_replacements(qualified_name):
    if not qualified_name.startswith('caf::'):
        raise Exception('qualified name must start with "caf::"')
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
        'hpp':  '/'.join(namev) + '.hpp',
        'year': datetime.datetime.now().year
    }

