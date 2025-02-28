import tkinter as tk
from tkinter import filedialog
import json

def load_config():
    """Load color and symbol settings from the JSON file."""
    try:
        with open('text2blog_settings.json', 'r') as file:
            config = json.load(file)
    except FileNotFoundError:
        # Default configuration if the JSON file is missing
        config = {
            "window_bg": "#2e2e2e",
            "text_box_bg": "#2e2e2e",
            "text_box_fg": "#ffffff",
            "button_bg": "#4e4e4e",
            "button_fg": "#ffffff",
            "status_label_bg": "#2e2e2e",
            "status_label_fg": "#ffffff",
            "symbols": {
                "main_title": "#####",
                "section_title": "####",
                "subsection_title": "###",
                "subsubsection_title": "##"
            }
        }
    return config

def convert_text_to_html(input_text, config):
    lines = input_text.split('\n')
    content_html = []
    sidebar_links = []
    step_counter = 0
    article_open = False
    main_title = ""

    for line in lines:
        if line.startswith(config["symbols"]["main_title"]):
            main_title = line[len(config["symbols"]["main_title"]):].strip()
        elif line.startswith(config["symbols"]["section_title"]):
            link_text = line[len(config["symbols"]["section_title"]):].strip()
            sidebar_links.append(f'<a href="#step{step_counter}">{link_text}</a>')
        elif line.startswith(config["symbols"]["subsection_title"]):
            if article_open:
                content_html.append('</article>')
            article_open = True
            content_html.append(f'<article class="post" id="step{step_counter}">')
            content_html.append(f'    <h2>{line[len(config["symbols"]["subsection_title"]):].strip()}</h2>')
            step_counter += 1
        elif line.startswith(config["symbols"]["subsubsection_title"]):
            content_html.append(f'    <h4>{line[len(config["symbols"]["subsubsection_title"]):].strip()}</h4>')
        elif line.strip():
            content_html.append(f'    <p>{line.strip()}</p>')

    if article_open:
        content_html.append('</article>')

    sidebar_html = '<div class="sidebar">\n'
    if main_title:
        sidebar_html += f'    <h1>{main_title}</h1>\n'
    sidebar_html += '\n'.join(sidebar_links)
    sidebar_html += '\n</div>'

    full_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{main_title}</title>
    <link rel="stylesheet" href="../styles/style.css">
</head>
<body>
    <header>
        <h1>stelarn pages</h1>
        <nav>
            <ul>
                <li><a href="../index.html" class="active">Home</a></li>
                <li><a href="../about.html">About</a></li>
                <li><a href="../contact.html">Contact</a></li>
            </ul>
        </nav>
    </header>
    {sidebar_html}
    <div class="content">
        <section class="Title&Description">
            {''.join(content_html)}
        </section>
    </div>
    <footer>
        <p>&copy; 2025 stelarn pages. All rights reserved.</p>
    </footer>
</body>
</html>'''

    return full_html

def submit_action():
    input_text = text_box.get("1.0", tk.END)
    html_content = convert_text_to_html(input_text, config)
    save_path = filedialog.asksaveasfilename(defaultextension=".html", filetypes=[("HTML files", "*.html")])
    if save_path:
        with open(save_path, 'w') as file:
            file.write(html_content)
        status_label.config(text=f"File saved: {save_path}")

root = tk.Tk()
root.title("Text to HTML Converter")

# Load configuration (colors and symbols) from the JSON file
config = load_config()

# Set the window background color
root.configure(bg=config["window_bg"])

# Create a frame to hold the text box and status label
frame = tk.Frame(root, bg=config["window_bg"])
frame.pack(fill='both', expand=True, padx=10, pady=10)

# Create a text box with the loaded colors
text_box = tk.Text(frame, wrap='word', bg=config["text_box_bg"], fg=config["text_box_fg"], insertbackground='white', font=('Arial', 12))
text_box.pack(fill='both', expand=True, padx=5, pady=5)

# Create a submit button with the loaded colors
submit_button = tk.Button(frame, text="Submit", command=submit_action, bg=config["button_bg"], fg=config["button_fg"], font=('Arial', 12))
submit_button.pack(pady=5)

# Create a status label with the loaded colors
status_label = tk.Label(frame, text="", bg=config["status_label_bg"], fg=config["status_label_fg"], font=('Arial', 10))
status_label.pack(pady=5)

root.mainloop()
