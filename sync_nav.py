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

# Extract CSS for user-dropdown
css_match = re.search(r'(/\* User Profile Dropdown Style \*/.*?</style>)', home_content, re.DOTALL)
if css_match:
    user_dropdown_css = css_match.group(1)
else:
    print("Could not find user dropdown CSS in home/code.html")
    exit(1)

# Extract auth-state HTML
auth_state_match = re.search(r'(<!-- Auth State Container -->.*?)</div>\n</div>\n</nav>', home_content, re.DOTALL)
if auth_state_match:
    auth_state_html = auth_state_match.group(1)
else:
    print("Could not find Auth State Container in home/code.html")
    exit(1)

# Extract profile modal and JS logic
script_match = re.search(r'(<!-- Profile Editor Modal \(Liquid Glass\) -->.*?</script>)', home_content, re.DOTALL)
if script_match:
    modal_and_script = script_match.group(1)
else:
    print("Could not find Profile Modal and script in home/code.html")
    exit(1)


for file_path in files_to_update:
    full_path = f"/Users/tangyaoyue/Kezhongke_web/{file_path}"
    try:
        with open(full_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # 1. Update CSS
        if '/* User Profile Dropdown Style */' not in content:
            content = re.sub(r'(/\* Ambient Liquid Background \*/.*?\})\n    </style>', r'\1\n\n        ' + user_dropdown_css, content, flags=re.DOTALL)
            if 'User Profile Dropdown Style' not in content:
                 content = content.replace('</style>', f'\n        {user_dropdown_css}')
                 
        # 2. Update Nav CTA
        # Find the search toggle button and replace what comes after until </div></div></nav>
        content = re.sub(r'<a href=".*?nav-cta.*?</a>', auth_state_html, content, flags=re.DOTALL)

        # 3. Update Modal and JS
        # Replace from <script> to </script> right after </nav>
        # Note: some files might have <script>...</script> right after </nav>
        content = re.sub(r'<script>\n\(function\(\)\{\n  var pages=\[\n    \{name:\'首页 Home\'.*?</script>', modal_and_script, content, flags=re.DOTALL)

        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
            print(f"Updated {file_path}")
            
    except FileNotFoundError:
        print(f"File not found: {full_path}")

