import os
import yaml
import shutil

def get_pandoc_meta(fp):
    yaml_str = ""
    with open(fp, encoding="utf-8") as f:
        inYaml = False
        for line in f:
            if line.startswith('---') and (not inYaml):
                inYaml = True
                continue
            if (line.startswith('---') or line.startswith('...')) and inYaml:
                break
            if inYaml: yaml_str += line
    return yaml.load(yaml_str, Loader=yaml.FullLoader)


def copy_and_overwrite(from_path, to_path):
    if os.path.exists(to_path):
        shutil.rmtree(to_path)
    shutil.copytree(from_path, to_path)


def rm_dir(path):
    shutil.rmtree(path)
