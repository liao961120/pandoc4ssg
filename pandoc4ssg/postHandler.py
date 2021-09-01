import os
import yaml
import toml
import shutil
import pypandoc
from pathlib import Path
from .utils import copy_and_overwrite, get_pandoc_meta, rm_dir
from .dirStruct import DirStruct


class PostHandler:
    def __init__(self, meta_keep=None, meta_new=None, use_toml=True, output_exts=".html", output_dir=True, pandoc_html_extra_args=None, pandoc_tex_extra_args=None, dir_struct=DirStruct()):
        # Static Site Paths
        self.paths = dir_struct
        # Post meta data
        self.meta = {}
        self.meta_keep = meta_keep
        self.meta_new = meta_new
        self.use_toml = use_toml
        if meta_keep is None:
            self.meta_keep = {'title', 'subtitle', 'date', 'author'}
        if meta_new is None:
            self.meta_new = [
                ('template', 'bare.html'), 
                ('raw', True)
            ]
        
        # Pandoc args
        self.output_exts = output_exts
        self.output_dir = output_dir
        self.pandoc_html_extra = pandoc_html_extra_args
        self.pandoc_tex_extra = pandoc_tex_extra_args
        if pandoc_html_extra_args is None:
            self.pandoc_html_extra = [
                '--citeproc',
                '--shift-heading-level-by=-1'
            ]
        if pandoc_tex_extra_args is None:
            self.pandoc_tex_extra = [
                '--standalone',
                '--citeproc',
                '--number-sections',
                '--shift-heading-level-by=-1'   
            ]


    def build_post_html(self, fp:Path):
        meta = self._get_new_meta(fp)

        # Make paths absolute
        old_dir = os.getcwd()
        new_dir = fp.parent.absolute()
        infile = str(fp.absolute())

        os.chdir(new_dir)
        output = pypandoc.convert_file(infile, 'html5', extra_args=self.pandoc_html_extra)
        os.chdir(old_dir)

        outpath = self.paths.tgt_dir_html / (fp.stem + self.output_exts)
        if self.output_dir:
            outdir = (self.paths.tgt_dir_html / fp.stem)
            if outdir.exists(): rm_dir(outdir)
            outdir.mkdir(parents=True, exist_ok=False)
            outpath = outdir / f"index{self.output_exts}"

        with open(outpath, "w", encoding="utf-8") as f:
            f.write(meta + output)

        # Copy dependencies
        for fp in self.paths.pandoc_post_dir.glob("*"):
            if fp.is_dir(): 
                if self.output_dir:
                    copy_and_overwrite(fp, outdir / fp.name)
                else:
                    copy_and_overwrite(fp, self.paths.static_tgt / fp.name)


    def build_post_tex(self, fp):
        z_dir = self.paths.tgt_dir_tex / fp.stem
        z_dir.mkdir(parents=True, exist_ok=True)

        # Make paths absolute
        old_dir = os.getcwd()
        new_dir = fp.parent.absolute()
        infile = str(fp.absolute())
        outfile = str((z_dir / "main.tex").absolute())

        os.chdir(new_dir)
        pypandoc.convert_file(infile, 'tex', outputfile=outfile, extra_args=self.pandoc_tex_extra)
        os.chdir(old_dir)

        # Copy dependencies
        for fp in self.paths.pandoc_post_dir.glob("*"):
            if fp.is_dir(): copy_and_overwrite(fp, z_dir / fp.name)
        # Zip dir (for overleaf upload)
        outfp = str(self.paths.tgt_dir_tex / z_dir.stem)
        shutil.make_archive(outfp, 'zip', str(z_dir))


    def _get_new_meta(self, fp):
        meta = get_pandoc_meta(fp)
        meta_out = {}
        for k, v in meta.items():
            if k in self.meta_keep:
                meta_out[k] = v
        for k, v in self.meta_new: meta_out[k] = v
        if self.use_toml:
            return '+++\n' + toml.dumps(meta_out) + '+++\n\n'
        else:
            return '---\n' + yaml.dump(meta_out) + '---\n\n'
