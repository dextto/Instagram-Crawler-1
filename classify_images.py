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
    num = int(len(file_list) / 10)

    likes = [f[2] for f in file_list]

    for f in file_list:
        f[2] = str(f[2])

    grades = []
    for i in range(9):
        grades.append(likes[i * num:(i + 1) * num])
    grades.append(likes[num * 9:])

    print(grades)
    print(len(file_list))
    print(len(grades))
    temp = sum(grades, [])
    print(len(temp))

    for i in range(10):
        if i == 9:
            break
        p_grade = grades[i]
        n_grade = grades[i+1]
        p_last = p_grade[-1]
        n_first = grades[i+1][1]
        if p_last != n_first:
            continue

        num = p_last
        p_cnt = p_grade.count(num)
        n_cnt = grades[i+1].count(num)

        if p_cnt < n_cnt:
            p_grade = p_grade[0:-p_cnt]
            for _ in range(p_cnt):
                n_grade.insert(0, num)
        elif p_cnt > n_cnt:
            for _ in range(n_cnt):
                p_grade.append(num)
            n_grade = n_grade[n_cnt:]
        else:
            cnt = p_cnt
            if len(p_grade) <= len(n_grade):
                p_grade = p_grade[:-cnt]
                for _ in range(cnt):
                    n_grade.insert(0, num)
            else:
                for _ in range(cnt):
                    p_grade.append(num)
                n_grade = n_grade[cnt:]

        grades[i] = p_grade
        grades[i+1] = n_grade
    print(grades)

    print(file_list)
    _sum = 0
    for i in range(len(grades)):
        grade_path = f'{path}/grade{str("%02d" % i)}'
        if not os.path.isdir(grade_path):
            os.mkdir(grade_path)

        grade = grades[i]
        for ii in range(len(grade)):
            try:
                shutil.copy(f'{path}/{"".join(file_list[_sum])}', grade_path)
            except IndexError:
                print(_sum)
                raise
            _sum = _sum + 1

    make_zip(path)


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
