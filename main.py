import glob
import os
import sys
import yaml

CONFIGURATION_BASE_DIR = "./conf"
CONFIG_FILENAME = "config.yaml"
BOOKMARK_FILENAME = "dd-ts-bookmarks"
RELEASE_DIR = "./release"

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
            try:
                bookmarks = yaml.safe_load(fp)["bookmarks"]
                for bookmark in bookmarks:
                    html_accumulator += "\n" + "\t"*(depth+1) + f"<DT><A HREF=\"{bookmark['url']}\">{bookmark['label']}</A></DT>"
            except TypeError: # Skip empty yaml files
                pass
            except KeyError as e:
                raise KeyError(f"An error was encountered parsing a configuration yaml file: {config_file}. Most likely the 'url' or 'label' field is missing. From {str(e)}") from e

    # Iterate over sub-folders, return recursive call
    subfolders = [ f.path for f in os.scandir(current_directory) if f.is_dir() ]
    if not subfolders:
        html_accumulator += "\n" + "\t"*depth + "</DL>"
        return html_accumulator
    else:
        for subfolder in subfolders:
            html_accumulator = generate_bookmark_html(subfolder, html_accumulator, depth + 1)
        html_accumulator += "\n" + "\t"*depth + "</DL>"
        return html_accumulator

def generate_bookmarks():
    """ Generates a bookmark HTML string
    """
    html = "<DL>"
    for directory in [ f.path for f in os.scandir(CONFIGURATION_BASE_DIR) if f.is_dir() ]:
        html += generate_bookmark_html(directory, "")
    html += "\n</DL>"

    return html

def generate_release(commit_id):
    bookmark_html = generate_bookmarks()
    for fpath in glob.glob(os.path.join(RELEASE_DIR, f"{BOOKMARK_FILENAME}*.html")):
        os.remove(fpath)
    with open(os.path.join(RELEASE_DIR ,f"{BOOKMARK_FILENAME}_{commit_id}.html"), "w") as fp_w:
        fp_w.write(bookmark_html)

    # TODO:
    # Update readme file with a list of available bookmarks w/ comments

if __name__ == '__main__':
    try:
        commit_id = sys.argv[1]
        commit_id = commit_id[-7:]
        generate_release(commit_id)
    except IndexError:
        print("Please pass in a commit ID as the first argument of this script", file=sys.stderr)
        
