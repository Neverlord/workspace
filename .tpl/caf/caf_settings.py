import os, datetime

component_dirs = {
    'libcaf_core': os.path.join('caf', 'libcaf_core'),
    'libcaf_io': os.path.join('caf', 'libcaf_io'),
    'libcaf_openssl': os.path.join('caf', 'libcaf_openssl'),
    'libcaf_opencl': os.path.join('caf', 'libcaf_opencl'),
    'libcaf_bb': os.path.join('incubator', 'libcaf_bb'),
    'libcaf_net': os.path.join('incubator', 'libcaf_net'),
}

def get_component(qualified_name):
    if qualified_name.startswith('caf::io'):
        return 'libcaf_io'
    if qualified_name.startswith('caf::openssl'):
        return 'libcaf_openssl'
    if qualified_name.startswith('caf::opencl'):
        return 'libcaf_opencl'
    if qualified_name.startswith('caf::bb'):
        return 'libcaf_bb'
    if qualified_name.startswith('caf::net'):
        return 'libcaf_net'
    return 'libcaf_core'

def make_paths(root_dir, qualified_name):
    if not qualified_name.startswith('caf::'):
        raise Exception('qualified name must start with "caf::"')
    namev = qualified_name.split('::')
    if len(namev) < 2:
        raise Exception('qualified name does not contain a valid class name')
    # Extract the unqualified class name.
    class_name = namev[-1]
    # Compute paths to .cpp files relative to component directory.
    rel_cpp = os.path.join('src', '/'.join(namev[1:-1]), class_name + '.cpp')
    rel_tst = os.path.join('test', '/'.join(namev[1:-1]), class_name + '.cpp')
    # Get the absolute path to our component.
    component = get_component(qualified_name)
    component_dir = os.path.join(root_dir, component_dirs[component])
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
        'qualified-class': '.'.join(namev[1:]),
        'open-namespaces': ns_open,
        'close-namespaces': ns_close,
        'hpp':  '/'.join(namev) + '.hpp',
        'year': datetime.datetime.now().year
    }

