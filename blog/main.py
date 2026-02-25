import os
from pathlib import Path
from dotenv import load_dotenv

print("Loading main.py – macros plugin found this file!")

# Load .env from the utilities folder (one level up from docs/)
env_path = Path("/docs/.env") #/ ".." / ".env"
print(f"Looking for .env at: {env_path}")

if env_path.exists():
    load_dotenv(dotenv_path=env_path)
    print("✅ .env file FOUND and loaded")
else:
    print("⚠️ .env file NOT FOUND – using fallback values")

def define_env(env):
    print("define_env called – setting variables and macros")

    # Public variables with fallbacks
    domain = os.getenv("DOMAIN", "anthonychild.com")
    env.variables["domain"] = domain
    print(f"Domain set to: {domain}")

    author = os.getenv("AUTHOR", "Anthony Child")
    env.variables["author"] = author
    # print(f"Author set to: {author}")    

    current_year = os.getenv("CURRENT_YEAR", "2025")
    env.variables["current_year"] = current_year

    # Email link macro
    @env.macro
    def email_link(text: str = "Contact Me") -> str:
        email = os.getenv("EMAIL", "anthony@anthonychild.com")
        display = email[::-1]  # Light anti-spam
        return f'<a href="mailto:{email}">{text}</a> <small>(reverse: {display})</small>'

# Recipe header macro
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
        
        # Add contributor/author if present
        contributor = meta.get('contributor') or meta.get('recipe_author')
        if contributor:
            parts.append(f"**Recipe by:** {contributor}")
        
        info = " | ".join(parts)
        
        return f"""
!!! info "Recipe Info"
    {info}
"""

    print("All variables and macros defined successfully")