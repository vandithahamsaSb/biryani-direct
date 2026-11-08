import os
import re
import subprocess
import zipfile

# 1. Read Markdown content
with open("Technical_Design_Document.md", "r", encoding="utf-8") as f:
    text = f.read()

# 2. Simple Markdown -> HTML converter so headings and code look clean
html_body = text
html_body = re.sub(r"^### (.*?)$", r"<h3>\1</h3>", html_body, flags=re.MULTILINE)
html_body = re.sub(r"^## (.*?)$", r"<h2>\1</h2>", html_body, flags=re.MULTILINE)
html_body = re.sub(r"^# (.*?)$", r"<h1>\1</h1>", html_body, flags=re.MULTILINE)
html_body = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", html_body)
html_body = re.sub(
    r"```(.*?)```", r"<pre><code>\1</code></pre>", html_body, flags=re.DOTALL
)
html_body = html_body.replace("\n", "<br>")

html_content = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Technical Design Document - Biryani Direct</title>
<style>
  body {{ font-family: 'Segoe UI', Arial, sans-serif; margin: 40px; color: #222; line-height: 1.6; font-size: 13px; }}
  h1 {{ color: #E65100; border-bottom: 2px solid #E65100; padding-bottom: 6px; font-size: 22px; }}
  h2 {{ color: #D84315; margin-top: 20px; border-bottom: 1px solid #ddd; padding-bottom: 4px; font-size: 17px; }}
  h3 {{ color: #BF360C; font-size: 14px; margin-top: 14px; }}
  strong {{ color: #111; }}
  pre {{ background: #f4f4f4; padding: 12px; border-radius: 4px; border: 1px solid #ddd; font-family: Consolas, monospace; }}
  code {{ font-family: Consolas, monospace; color: #c7254e; }}
</style>
</head>
<body>
{html_body}
</body>
</html>"""

temp_html = os.path.abspath("temp_doc.html")
pdf_out = os.path.abspath("Technical_Design_Document.pdf")

with open(temp_html, "w", encoding="utf-8") as f:
    f.write(html_content)

# 3. Use Edge with full local file path to convert HTML to styled PDF
edge_paths = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
]
edge_exe = next((p for p in edge_paths if os.path.exists(p)), None)

if edge_exe:
    subprocess.run(
        [
            edge_exe,
            "--headless",
            "--disable-gpu",
            f"--print-to-pdf={pdf_out}",
            temp_html,
        ]
    )
    print("✅ Created: Technical_Design_Document.pdf")
else:
    print("⚠️ Edge executable not found. PDF creation skipped.")

if os.path.exists(temp_html):
    os.remove(temp_html)

# 4. Package into Final ZIP File
zip_name = "Biryani_Direct_Submission.zip"
with zipfile.ZipFile(zip_name, "w", zipfile.ZIP_DEFLATED) as zipf:
    if os.path.exists("Technical_Design_Document.pdf"):
        zipf.write("Technical_Design_Document.pdf")
        print("📦 Added Technical_Design_Document.pdf to ZIP")
    if os.path.exists("deployment.md"):
        zipf.write("deployment.md")
        print("📦 Added deployment.md to ZIP")
    if os.path.exists("Technical_Design_Document.md"):
        zipf.write("Technical_Design_Document.md")
        print("📦 Added Technical_Design_Document.md to ZIP")

print(f"\n🎉 SUCCESS! Final Submission Package created: {zip_name}")
