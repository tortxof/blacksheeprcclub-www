#! /usr/bin/env python3

import sys
import subprocess

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("Usage: gen_pdf.py ../_posts/post.md ../newsletters/newsletter.pdf 'Date String'")
        sys.exit()
    post_file = sys.argv[1]
    pdf_file = sys.argv[2]
    with open(post_file) as f:
        post_md = f.read()
    post_md = subprocess.check_output(['rmfm'], input=post_md.encode())
    post_html = subprocess.check_output(['kramdown'], input=post_md).decode()
    template_html = subprocess.check_output(['mustache', 'officers.yaml', 'template.mustache']).decode()
    out_html = template_html.format(content=post_html, date=sys.argv[3])
    with open('tmp.html', 'w') as f:
        f.write(out_html)
    subprocess.check_output(['wkhtmltopdf', '-s', 'Letter', '--print-media-type', '-B', '0.5in', '-L', '0.5in', '-R', '0.5in', '-T', '0.5in', 'tmp.html', pdf_file])
