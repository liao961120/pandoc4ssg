import os 
from .postHandler import PostHandler

def build_pandoc_html(ssg_cmd, post_handler: PostHandler):
    for fp in post_handler.paths.pandoc_post_dir.glob("*.md"):
        post_handler.build_post_html(fp)

def build_pandoc_tex(ssg_cmd, post_handler: PostHandler):
    for fp in post_handler.paths.pandoc_post_dir.glob("*.md"):
        post_handler.build_post_tex(fp)

def build_site(ssg_cmd, post_handler):
    os.system(ssg_cmd)

def build(ssg_cmd, post_handler, pipeline=[build_pandoc_html, build_pandoc_tex, build_site]):
    for process in pipeline: 
        process(ssg_cmd, post_handler)