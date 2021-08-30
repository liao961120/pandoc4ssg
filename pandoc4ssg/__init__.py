#%%
import os
import yaml
import toml
import shutil
import pypandoc
from pathlib import Path

root = Path('.')
target_dir_post = root / 'content/blog'
target_dir_tex = root / 'public/tex'
post_dir = root / 'pandoc_posts'
static = root / 'static/blog/figures' 
public = root / 'public'
target_dir_tex.mkdir(parents=True, exist_ok=True)


def build():
    # Build html posts to content/
    for fp in post_dir.glob("*.md"):
        build_post_html(fp, target_dir_post)

    # Build site to public/
    os.system("zola build")

    # Build tex posts to public/tex/
    for fp in post_dir.glob("*.md"):
        build_post_tex(fp, target_dir_tex)



def build_post_html(fp, target_dir):
    meta = get_pandoc_meta(fp)
    meta = dump_meta_toml(meta)

    # Make paths absolute
    old_dir = os.getcwd()
    new_dir = fp.parent.absolute()
    infile = str(fp.absolute())

    os.chdir(new_dir)
    output = pypandoc.convert_file(
            infile, 'html5', 
            extra_args=[
                '--citeproc',
                '--number-sections',
                '--csl=deps/citation-style.csl',
                '--shift-heading-level-by=-1'
    ])
    os.chdir(old_dir)

    with open(target_dir / fp.name, "w", encoding="utf-8") as f:
        f.write(meta + output)

    # Copy dependencies
    copy_and_overwrite(post_dir / 'figures', static)


def build_post_tex(fp, target_dir):
    z_dir = target_dir / fp.stem
    z_dir.mkdir(parents=True, exist_ok=True)

    # Make paths absolute
    old_dir = os.getcwd()
    new_dir = fp.parent.absolute()
    infile = str(fp.absolute())
    outfile = str((z_dir / "main.tex").absolute())

    os.chdir(new_dir)
    pypandoc.convert_file(
        infile, 'tex', 
        outputfile=outfile,
        extra_args=[
            '--standalone',
            '--citeproc',
            '--number-sections',
            '--csl=deps/citation-style.csl',
            '--shift-heading-level-by=-1'
    ])
    os.chdir(old_dir)

    # Copy dependencies
    copy_and_overwrite(post_dir / 'figures', z_dir / 'figures')
    outfp = str(target_dir / z_dir.stem)
    shutil.make_archive(outfp, 'zip', str(z_dir))


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


def dump_meta_toml(meta):
    keep = {'title', 'subtitle', 'date', 'author'}
    new = [
        ('template', 'bare.html'), 
        ('raw', True)
    ]
    meta_out = {}
    for k, v in meta.items():
        if k in keep:
            meta_out[k] = v
    for k, v in new: meta_out[k] = v
    return '+++\n' + toml.dumps(meta_out) + '+++\n\n'


def copy_and_overwrite(from_path, to_path):
    if os.path.exists(to_path):
        shutil.rmtree(to_path)
    shutil.copytree(from_path, to_path)
