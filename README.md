# Using Pandoc with Static Site Generators

This library aims to make it easy to write posts in [Pandoc's Markdown](https://pandoc.org/MANUAL.html#pandocs-markdown) and build them to static sites with ANY Static Site Generators (SSG) you want. After specifying the directory structure (`pandoc4ssg.DirStruct`) of your static site (depends on the SSG you used) and options for compiling posts (`pandoc4ssg.PostHandler`), `pandoc4ssg` builds the site for you.


## Hugo

Below is an example that builds markdown files located in `pandoc_posts/` into a [Hugo](https://gohugo.io) site. See [pandoc4ssg-example](https://github.com/liao961120/pandoc4ssg-example) for details.


```python
import pandoc4ssg

dir_struct = pandoc4ssg.DirStruct(
    tgt_dir_html="content/post",
    tgt_dir_tex="public/tex",
    pandoc_post_dir="pandoc_posts",
    static_tgt=None,
    public="public"
)

post_handler = pandoc4ssg.PostHandler(
    meta_keep = ["title", "subtitle", "author", "date", "categories", "tags"],
    meta_new=[("new_field", True)],
    use_toml=False,
    output_exts=".html",
    output_dir=True,
    pandoc_html_extra_args=['--citeproc'],
    dir_struct=dir_struct
)

pandoc4ssg.build(ssg_cmd="hugo -D", post_handler=post_handler)
```
