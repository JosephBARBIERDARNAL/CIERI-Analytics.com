from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
from nbconvert import HTMLExporter
from bs4 import BeautifulSoup
import os
import platform


def remove_tags(soup, tag, css_class=None):
    for elements in soup.find_all(tag, class_=css_class):
        elements.extract()


def wrap_tags(soup, template, tag, css_class=None):
    for table in soup.find_all('table'):
        div_df_container = template.new_tag(tag, attrs={'class': css_class})
        table.wrap(div_df_container)    


def apply_syntax_highlighting(soup):
    formatter = HtmlFormatter(style='default')  # Choose a style for highlighting
    for code in soup.find_all('pre'):  # Loop through all code elements
        code_text = code.get_text()  # Extract the code text
        highlighted_code = highlight(code_text, PythonLexer(), formatter)  # Apply highlighting
        code.replace_with(BeautifulSoup(highlighted_code, 'html.parser'))  # Replace original code
    style_tag = soup.new_tag('style', type='text/css')
    style_tag.string = formatter.get_style_defs('.highlight')  # Add CSS for highlighting
    soup.body.insert(0, style_tag)


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
    apply_syntax_highlighting(soup_notebook)
    main_content = soup_notebook.find('body')

    # remove unwanted tags
    remove_tags(main_content, 'div', 'jp-InputPrompt jp-InputArea-prompt')
    remove_tags(main_content, 'div', 'jp-OutputPrompt jp-OutputArea-prompt')
    remove_tags(main_content, 'a', 'anchor-link')

    # wrap tables in a <div class="dataframe-container">
    wrap_tags(main_content, soup_template, 'div', 'dataframe-container')

    # change width and height of plotly plots
    iframe = main_content.find('iframe')
    if iframe is not None and 'img/plotly/' in iframe['src']:
        iframe['width'] = '1030'
        iframe['height'] = '650'

    # add spacing before all h2 elements
    for h2 in main_content.find_all('h2'):
        h2.insert_before(soup_template.new_tag('br'))

    # merge the contents
    container = soup_template.find('div', class_='container')
    container.clear()
    container.append(main_content)

    # write the combined HTML to the output file
    output_path = convert_to_html_path(notebook_path)
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(str(soup_template))


# Example usage
notebook_path = 'projects/share/cancer-visualization.ipynb'
convert_notebook(notebook_path)

# Open the HTML file in the browser
adress = f"http://localhost:8000/{convert_to_html_path(notebook_path)}"
run_server = "python -m http.server"
os_name = platform.system()

if os_name == 'Darwin': # macOS
    openfile = f"open {adress}"
    os.system(openfile)
    os.system(run_server)
    
elif os_name == 'Windows': # Windows
    openfile = f"start {adress}"
    os.system(openfile)
    os.system(run_server)

else: # other
    print("\nSee the HTML output at:")
    print(f"{adress}\n")
    os.system(run_server)