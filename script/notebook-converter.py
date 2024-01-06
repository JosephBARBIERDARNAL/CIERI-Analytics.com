from nbconvert import HTMLExporter
from bs4 import BeautifulSoup


def remove_tags(soup, tags, css_class=None):
    for elements in soup.find_all(tags, class_=css_class):
        elements.extract()


def convert_to_html_path(first_path):
    if not first_path.endswith('.ipynb'):
        raise ValueError("The provided path does not have a .ipynb extension")
    parts = first_path.split('.')
    parts[-1] = 'html'
    second_path = '.'.join(parts)
    return second_path


def convert_notebook(notebook_path, template_path='templates/template-notebook.html'):
    
    # convert the notebook to HTML
    html_exporter = HTMLExporter()
    body, _ = html_exporter.from_file(notebook_path)

    # load template 
    with open(template_path, 'r', encoding='utf-8') as file:
        template_html = file.read()

    # parse both HTML contents and extract the main content
    soup_template = BeautifulSoup(template_html, 'html.parser')
    soup_notebook = BeautifulSoup(body, 'html.parser')
    main_content = soup_notebook.find('body')

    # remove unwanted tags
    remove_tags(main_content, 'div', 'jp-InputPrompt jp-InputArea-prompt')
    remove_tags(main_content, 'div', 'jp-OutputPrompt jp-OutputArea-prompt')
    remove_tags(main_content, 'a', 'anchor-link')

    # merge the contents
    container = soup_template.find('div', class_='container')
    container.clear()  
    container.append(main_content)

    # write the combined HTML to the output file
    output_path = convert_to_html_path(notebook_path)
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(str(soup_template))

# Example usage
notebook_path = 'projects/share/code/work-with-share.ipynb'
convert_notebook(notebook_path)
