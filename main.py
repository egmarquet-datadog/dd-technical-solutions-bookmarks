import os
import yaml

CONFIGURATION_BASE_DIR = "./conf"
CONFIG_FILENAME = "config.yaml"
OUTPUT_DIR = "./release"

def generate_bookmark_html(current_directory, html_accumulator, depth=1):
    """ Cute recursive function to generate the bookmark HTML file based on the directory structure of the project
    """
    # Generate directory tags
    html_accumulator += "\n" + "\t"*depth + f"<DT><H3>{os.path.basename(current_directory)}</H3></DT>"
    html_accumulator += "\n" + "\t"*depth + "<DL>"

    # Generate bookmark tags
    config_file = os.path.join(current_directory, CONFIG_FILENAME)
    if os.path.exists(config_file):
        with open(config_file, "r") as fp:
            bookmarks = yaml.safe_load(fp)[0]["bookmarks"]
            for bookmark in bookmarks:
                html_accumulator += "\n" + "\t"*(depth+1) + f"<DT><A HREF=\"{bookmark['url']}\">{bookmark['label']}</A></DT>"
    
    # Iterate over subfolders, return recusive call
    subfolders = [ f.path for f in os.scandir(current_directory) if f.is_dir() ]
    if not subfolders:
        html_accumulator += "\n" + "\t"*depth + "</DL>"
        return html_accumulator
    else:
        for subfolder in subfolders:
            html_accumulator = generate_bookmark_html(subfolder, html_accumulator, depth + 1)
        html_accumulator += "\n" + "\t"*depth + "</DL>"
        return html_accumulator

def main():
    html = "<DL>"
    for directory in [ f.path for f in os.scandir(CONFIGURATION_BASE_DIR) if f.is_dir() ]:
        html += generate_bookmark_html(directory, "")
    html += "\n</DL>"
    print(html)

if __name__ == '__main__':
    main()
