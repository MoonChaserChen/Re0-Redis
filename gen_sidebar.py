import os
from shutil import copyfile
import codecs
import re

suffix = ".md"
gen_file_name = "summary.md"
doc_path = "docs"
read_me_file = "README.md"
cname_file = "CNAME"

ignore_files = [gen_file_name, ".git", read_me_file, "images"]


def sorted_alphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(data, key=alphanum_key)


def print_file(c_dir, depth, sidebar_file, readme_file):
    for f in sorted_alphanumeric(os.listdir(c_dir)):
        re_f = os.path.join(c_dir, f)
        is_d = os.path.isdir(re_f)
        if is_d and f not in ignore_files:
            content = "\t" * depth + "- " + f + "\n"
            sidebar_file.write(content)
            readme_file.write(content)
            print_file(re_f, depth + 1, sidebar_file, readme_file)
        else:
            if suffix in f and f not in ignore_files:
                f_n = os.path.splitext(f)[0]
                content = "\t" * depth + "- [" + f_n + "](/" + re_f[2:] + ")\n"
                sidebar_file.write(content)
                readme_file.write(content)


os.chdir(doc_path)
copyfile("../" + read_me_file, read_me_file)
copyfile("../" + cname_file, cname_file)

# 为README.md生成目录；生成左侧sidebar(summary.md)
g_f = codecs.open(gen_file_name, 'w', encoding='utf-8')
r_f = codecs.open(read_me_file, 'a', encoding='utf-8')
r_f.write("\n## 目录")
print_file(".", 0, g_f, r_f)
g_f.close()
r_f.close()
