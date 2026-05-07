import re

files_to_update = [
    "grow/code.html",
    "path/code.html",
    "atelier/code.html",
    "journal/code.html",
    "about/code.html"
]

with open("/Users/tangyaoyue/Kezhongke_web/home/code.html", "r", encoding="utf-8") as f:
    home_content = f.read()

# Extract the FULL nav block
nav_match = re.search(r'(<nav id="top-nav".*?</nav>)', home_content, re.DOTALL)
if nav_match:
    full_nav = nav_match.group(1)
else:
    print("Could not find full nav in home/code.html")
    exit(1)

for file_path in files_to_update:
    full_path = f"/Users/tangyaoyue/Kezhongke_web/{file_path}"
    try:
        with open(full_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Replace the entire existing nav block with the full one from home
        content = re.sub(r'<nav id="top-nav".*?</nav>', full_nav, content, flags=re.DOTALL)

        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
            print(f"Fixed {file_path}")
            
    except FileNotFoundError:
        print(f"File not found: {full_path}")
