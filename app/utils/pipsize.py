import os
import pkg_resources
from hurry.filesize import size


def calc_container(path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size


dists = [d for d in pkg_resources.working_set]
total_size = 0
for dist in dists:
    try:
        path = os.path.join(dist.location, dist.project_name)
        _size = calc_container(path)
        if _size / 1000 > 1.0:
            print(f"{dist}: {size(_size)}")
            print("-" * 40)
            total_size += _size

    except OSError:
        "{} no longer exists".format(dist.project_name)

print(f"Total size: {size(total_size)}")
