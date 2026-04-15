#!/usr/bin/env python3
import os
import re
from datetime import datetime

def extract_title(file_path):
    """
    Extracts the title from a markdown file.
    Priority:
    1. yaml frontmatter 'title:'
    2. first H1 header '# Title'
    3. filename (capitalized)
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # 1. Try YAML frontmatter
            frontmatter_match = re.search(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
            if frontmatter_match:
                lines = frontmatter_match.group(1).split('\n')
                for line in lines:
                    if line.strip().startswith('title:'):
                        title = line.replace('title:', '').strip().strip('"').strip("'")
                        if title:
                            return title
            
            # 2. Try first H1
            h1_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
            if h1_match:
                return h1_match.group(1).strip()
    except Exception:
        pass
    
    # 3. Fallback to filename
    basename = os.path.basename(file_path)
    if basename == 'index.md' or basename == 'INDEX.md':
        parent_dir = os.path.basename(os.path.dirname(file_path))
        if parent_dir and parent_dir != 'references':
            return parent_dir.replace('-', ' ').replace('_', ' ').capitalize()
        return "Overview"
    
    return os.path.splitext(basename)[0].replace('-', ' ').replace('_', ' ').capitalize()

def generate_index(root_dir):
    docs = {}
    
    for root, dirs, files in os.walk(root_dir):
        # Skip hidden directories and assets/images
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['assets', 'images', 'img', 'static']]
        
        md_files = [f for f in files if f.endswith('.md') and f.upper() != 'INDEX.MD']
        if not md_files:
            continue
            
        rel_path = os.path.relpath(root, root_dir)
        if rel_path == '.':
            category = 'General'
        else:
            # Create a nice category name from the folder path
            category = rel_path.replace('/', ' > ').replace('-', ' ').replace('_', ' ').title()
            
        docs[category] = []
        for f in sorted(md_files):
            full_path = os.path.join(root, f)
            title = extract_title(full_path)
            # Create a path relative to the references directory for the link
            link_path = os.path.relpath(full_path, root_dir)
            docs[category].append(f"- [{title}]({link_path})")

    # Build the Markdown content
    lines = [
        "# LINE Developers Documentation Index",
        "",
        f"Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "This is a comprehensive index of all available LINE Developers documentation, organized by category.",
        ""
    ]
    
    # Sort categories: General first, then alphabetical
    categories = sorted(docs.keys(), key=lambda x: (x != 'General', x.lower()))
    
    for category in categories:
        lines.append(f"## {category}")
        lines.extend(docs[category])
        lines.append("")

    return "\n".join(lines)

if __name__ == "__main__":
    base_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'references')
    output_file = os.path.join(base_dir, 'INDEX.md')
    
    if not os.path.exists(base_dir):
        print(f"⚠️ Error: Reference directory {base_dir} does not exist. Run sync-docs.sh first.")
        os.makedirs(base_dir, exist_ok=True)
    
    print(f"🔍 Scanning {base_dir}...")
    index_content = generate_index(base_dir)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(index_content)
        
    print(f"✅ Generated {output_file}")
