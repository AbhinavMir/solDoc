import argparse
import os
import re
# import pprint

# Regular expression to match Solidity comments
comment_regex = r'^\s*\/\*\*([\s\S]*?)\*\/'

# Regular expression to match Solidity class declarations
class_regex = r'^\s*(contract|library|interface)\s+(\w+)\s*'
function_regex = r'^\s*(function|fallback)\s+(\w+)\s*'

def read_config():
    config = {}
    with open('config.soldoc', 'r') as f:
        for line in f:
            if not line.startswith('#'):
                key, value = line.strip().split('=')
                config[key.strip()] = value.strip()
    return config

def generate_html(comment_map):
    # Initialize the HTML string
    html = ''

    # Add the opening HTML tags 
    html += '<!DOCTYPE html>\n<html>\n<head>\n<title>Solidity Documentation</title>\n'

    # Add the Skeleton CSS framework
    html += '<link rel="stylesheet" href="../utils/style.css" />\n'

    # Close the head section and start the body section
    html += '</head>\n<body>\n'

    # Add the index at the top
    html += '<div class="container max-w-screen-lg mx-auto my-16">\n'
    html += '<h1 class="text-4xl mb-8">Index</h1>\n'
    html += '<ul>\n'
    for class_name, functions in comment_map.items():
        contract_name = class_name[1]
        html += f'<li><a href="#{contract_name}">{contract_name}</a></li>\n'
    html += '</ul>\n'
    html += '</div>\n'

    # Iterate over each class and function
    for class_name, functions in comment_map.items():
        contract_name = class_name[1]
        html += f'<div class="container max-w-screen-lg mx-auto my-16" id="{contract_name}">\n'
        html += f'<h1 class="text-4xl mb-8"><b>{contract_name}</b></h1>\n'
        for function_name, comment in functions.items():
            function_name_str = function_name[1]
            link_name = f'{contract_name}/{function_name_str}'
            # Generate HTML for the comment and function
            html += f'<div class="mb-8">'
            html += f'<h3 class="text-2xl mb-4"><a href="#{link_name}"><code>{function_name_str}</code></a></h3>'
            html += f'<p class="text-lg">{comment.strip()}</p>\n'
            html += f'</div>\n'
        html += f'</div>\n'

    # Add the closing HTML tags
    html += '</body>\n</html>'

    # Return the HTML string
    return html

def main():
    # Read configuration from file
    config = read_config()

    # Set up argument parser
    parser = argparse.ArgumentParser(description='Generate HTML documentation from Solidity files')
    parser.add_argument('directory', help='directory containing Solidity files')
    parser.add_argument('-o', '--output', help='output file name', default=config['output_path'])
    args = parser.parse_args()
    # Iterate over all files in directory
    comment_map = {}
    for filename in os.listdir(args.directory):
        # Only process Solidity files
        if filename.endswith('.sol'):
            # Read file contents
            with open(os.path.join(args.directory, filename), 'r') as f:
                content = f.read()
            
            # Find all comments in file
            comments = re.findall(comment_regex, content, flags=re.MULTILINE)

            # Find class declarations in file
            classes = re.findall(class_regex, content, flags=re.MULTILINE)

            # Find function declarations in file
            functions = re.findall(function_regex, content, flags=re.MULTILINE)
            
            # Map comments to classes
            for comment in comments:
                for class_name in classes:
                    comment_map[class_name] = {}
                    for function in functions:
                        # @ -> <br><b>@</b><br><br><
                        modified_comment = re.sub(r'(@\w+)', r'<br><b>\g<1></b>', comment.strip())
                        # * gets removed
                        modified_comment = re.sub(r'\*', r'', modified_comment)
                        # remove all the whitespaces from the comment
                        comment_map[class_name][function] = modified_comment


    # Generate HTML
    html = generate_html(comment_map)

    # Write HTML to file
    with open(args.output, 'w') as f:
        f.write(html)

if __name__ == '__main__':
    main()