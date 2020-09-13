
def export_to_html(response, filename):
    with open('../_output_htmls/'+filename, 'wb') as f:
        f.write(response.content)
