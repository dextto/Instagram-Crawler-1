import operator
import os
import re
import shutil
import sys
import zipfile


def main(path):
    file_list = []
    for f in os.listdir(path):
        if os.path.isdir(f"{path}/{f}"):
            continue
        splited: list = re.split('(_|.jpg)', f)
        splited[2] = int(splited[2])
        file_list.append(splited)

    file_list = sorted(file_list, key=operator.itemgetter(2, 3))

    for f in file_list:
        f[2] = str(f[2])

    n = int(len(file_list) / 10)
    for i in range(10):
        grade_path = f'{path}/grade{str("%02d" % i)}'
        if not os.path.isdir(grade_path):
            os.mkdir(grade_path)

        cnt = n if i != 9 else int(len(file_list) - n * 9)
        for c in range(cnt):
            shutil.copy(f'{path}/{"".join(file_list[i * n + c])}', grade_path)

    # make_zip(path)


def make_zip(path):
    zip_file_path = f'{path}.zip'
    if os.path.exists(zip_file_path):
        os.remove(zip_file_path)
    zip_file = zipfile.ZipFile(zip_file_path, 'w')
    for folder, subfolders, files in os.walk(path):
        if not folder.endswith('grade', -7, -2):
            continue
        for f in files:
            zip_file.write(os.path.join(folder, f),
                           os.path.relpath(os.path.join(folder, f), path),
                           compress_type=zipfile.ZIP_DEFLATED)
    zip_file.close()


if __name__ == '__main__':
    main(sys.argv[1])
