import os
import sys
import shutil

cwd_path = os.getcwd()
sys.path.append(os.path.join(os.path.dirname(cwd_path), 'rt-thread', 'tools'))


# BSP dist function
def dist_do_building(BSP_ROOT, dist_dir):
    from mkdist import bsp_copy_files
    import rtconfig

    print("=> copy ch32 bsp library")
    library_dir = os.path.join(dist_dir, 'Libraries')
    library_path = os.path.join(os.path.dirname(BSP_ROOT), 'Libraries')
    if rtconfig.BSP_LIBRARY_TYPE is not None:
        bsp_copy_files(os.path.join(library_path, rtconfig.BSP_LIBRARY_TYPE),
                    os.path.join(library_dir, rtconfig.BSP_LIBRARY_TYPE))
    print("=> copy bsp drivers")
    bsp_copy_files(os.path.join(library_path, 'ch32_drivers'), os.path.join(library_dir, 'ch32_drivers'))
    shutil.copyfile(os.path.join(library_path, 'Kconfig'), os.path.join(library_dir, 'Kconfig'))
    # change RTT_ROOT in Kconfig
    if not os.path.isfile(os.path.join(dist_dir, 'Kconfig')):
        return

    with open(os.path.join(dist_dir, 'Kconfig'), 'r') as f:
        data = f.readlines()
    with open(os.path.join(dist_dir, 'Kconfig'), 'w') as f:
        for line in data:
            if line.find('source') != -1 and line.find('../libraries') != -1:
                line = line.replace('../Libraries', 'Libraries')
            f.write(line)
