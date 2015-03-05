#! /usr/bin/env python3

import sys
import os
import subprocess
import json
import datetime

config_file = 'config.json'

if __name__ == '__main__':
    if not os.path.isfile(config_file):
        print(config_file, "not found.")
        sys.exit()
    else:
        with open(config_file) as f:
            config = json.load(f)

    one_day = datetime.timedelta(days=1)

    meeting_date = datetime.datetime.strptime(config['meeting_date'], '%Y-%m-%d').date()

    if config['next_meeting'] == '':
        next_meeting = meeting_date + one_day
        while (next_meeting.month == meeting_date.month):
            next_meeting = next_meeting + one_day
        while (next_meeting.weekday != 1):
            next_meeting = next_meeting + one_day
    else:
        next_meeting = datetime.datetime.strptime(config['next_meeting'], '%Y-%m-%d').date()

    post_file = config['post_file']
    pdf_file = '../newsletters/bsrcc-newsletter-' + meeting_date.strftime('%Y-%m') + '.pdf'
    meeting_date_str = meeting_date.strftime('%B %Y')
    next_meeting_str = next_meeting.strftime('%B') + str(next_meeting.day)
    with open(post_file) as f:
        post_md = f.read()
    post_md = subprocess.check_output(['rmfm'], input=post_md.encode())
    post_html = subprocess.check_output(['kramdown'], input=post_md).decode()
    template_html = subprocess.check_output(['mustache', 'officers.yaml', 'template.mustache']).decode()
    out_html = template_html.format(content=post_html, date=meeting_date_str, next_meeting=next_meeting_str)
    with open('tmp.html', 'w') as f:
        f.write(out_html)
    subprocess.check_output(['compass', 'compile'])
    subprocess.check_output(['wkhtmltopdf', '-s', 'Letter', '--print-media-type', '-B', '0.5in', '-L', '0.5in', '-R', '0.5in', '-T', '0.5in', 'tmp.html', pdf_file])
