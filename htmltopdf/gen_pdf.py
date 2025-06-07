#! /usr/bin/env python3

import datetime
import json
import os
import subprocess
import sys


def rmfm(input_str):
    sections = input_str.split("---\n", maxsplit=2)
    if sections[0] != "":
        return input_str
    return sections[2]


config_file = "config.json"

if __name__ == "__main__":
    if not os.path.isfile(config_file):
        print(config_file, "not found.")
        sys.exit()
    else:
        with open(config_file) as f:
            config = json.load(f)

    one_day = datetime.timedelta(days=1)

    meeting_date = datetime.datetime.strptime(config["meeting_date"], "%Y-%m-%d").date()

    if config["next_meeting"] == "":
        next_meeting = meeting_date + one_day
        while next_meeting.month == meeting_date.month:
            next_meeting = next_meeting + one_day
        while next_meeting.weekday() != 5:
            next_meeting = next_meeting + one_day
    else:
        next_meeting = datetime.datetime.strptime(
            config["next_meeting"], "%Y-%m-%d"
        ).date()

    post_file = config["post_file"]
    pdf_file = "bsrcc-newsletter-" + meeting_date.strftime("%Y-%m") + ".pdf"
    meeting_date_str = meeting_date.strftime("%B %Y")
    next_meeting_str = next_meeting.strftime("%B ") + str(next_meeting.day)
    with open(post_file) as f:
        post_md = rmfm(f.read()).encode()
    post_html = subprocess.check_output(
        ["podman", "run", "-i", "--rm", "tortxof/webdev", "kramdown"], input=post_md
    ).decode()
    template_html = subprocess.check_output(
        [
            "podman",
            "run",
            "--rm",
            "-v",
            "{}:/host".format(os.getcwd()),
            "tortxof/webdev",
            "mustache",
            "officers.yaml",
            "template.mustache",
        ]
    ).decode()
    out_html = template_html.format(
        content=post_html, date=meeting_date_str, next_meeting=next_meeting_str
    )
    with open("tmp.html", "w") as f:
        f.write(out_html)
    subprocess.check_output(
        [
            "podman",
            "run",
            "--rm",
            "-v",
            "{}:/host".format(os.getcwd()),
            "tortxof/webdev",
            "compass",
            "compile",
            "--force",
        ]
    )
    subprocess.check_output(
        [
            "podman",
            "run",
            "--rm",
            "-v",
            "{}:/host".format(os.getcwd()),
            "tortxof/wkhtmltopdf",
            "wkhtmltopdf",
            "-s",
            "Letter",
            "--print-media-type",
            "-B",
            "0.5in",
            "-L",
            "0.5in",
            "-R",
            "0.5in",
            "-T",
            "0.5in",
            "--footer-center",
            "www.bsrcc.com",
            "--footer-right",
            "Page [page] of [topage]",
            "--footer-font-size",
            "9",
            "--footer-font-name",
            "Lora",
            "tmp.html",
            pdf_file,
        ]
    )
    subprocess.check_output(["mv", pdf_file, "../newsletters"])
