import os
import sys
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
for candidate in (HERE, HERE.parent):
    if (candidate / "mkdocs_env.py").exists():
        if str(candidate) not in sys.path:
            sys.path.insert(0, str(candidate))
        break

from mkdocs_env import load_site_env

load_site_env()

def define_env(env):

    domain = os.getenv("DOMAIN", "anthonychild.com")
    env.variables["domain"] = domain

    author = os.getenv("AUTHOR", "Anthony Child")
    env.variables["author"] = author

    env.variables["current_year"] = str(datetime.now().year)

    @env.macro
    def email_link(text: str = "Contact Me") -> str:
        email = os.getenv("EMAIL", "anthony@anthonychild.com")
        display = email[::-1]
        return f'<a href="mailto:{email}">{text}</a> <small>(reverse: {display})</small>'

    @env.macro
    def recipe_header():
        meta = env.page.meta
        parts = []

        if meta.get('prep_time'):
            parts.append(f"**Prep Time:** {meta['prep_time']}")
        if meta.get('cook_time'):
            parts.append(f"**Cook Time:** {meta['cook_time']}")
        if meta.get('servings'):
            parts.append(f"**Servings:** {meta['servings']}")
        if meta.get('yield'):
            parts.append(f"**Yield:** {meta['yield']}")
        if meta.get('difficulty'):
            parts.append(f"**Difficulty:** {meta['difficulty']}")

        contributor = meta.get('contributor') or meta.get('recipe_author')
        if contributor:
            parts.append(f"**Recipe by:** {contributor}")

        info = " | ".join(parts)

        return f"""
!!! info "Recipe Info"
    {info}
"""
