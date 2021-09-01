from pathlib import Path

class DirStruct:
    def __init__(self, root=".", tgt_dir_html="content/blog", tgt_dir_tex="public/tex", pandoc_post_dir="pandoc_posts", static_tgt="static/blog", public="public"):
        self.root = Path(root)
        self.tgt_dir_html = self.root / tgt_dir_html if tgt_dir_html != None else None
        self.tgt_dir_tex = self.root / tgt_dir_tex if tgt_dir_tex != None else None
        self.pandoc_post_dir = self.root / pandoc_post_dir if pandoc_post_dir != None else None
        self.static_tgt = self.root / static_tgt if static_tgt != None else None
        self.public = self.root / public if public != None else None

        # Init
        for d in [self.tgt_dir_html, self.tgt_dir_tex, self.pandoc_post_dir, self.static_tgt, self.public]:
            if d is None: continue
            d.mkdir(parents=True, exist_ok=True)
