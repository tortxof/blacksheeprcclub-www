# Black Sheep RC Club

## Official website of the Black Sheep RC Club, located in Pendleton, SC.

### Posting a newsletter.

When creating the post, add `newsletter` frontmatter with the year and month
`YYYY-MM`.

    newsletter: 2015-10

Once the post is complete, update the `htmltopdf/post.md` symlink in to point to
the new post. Then update `htmltopdf/config.json` with the meeting date and next
meeting date if it's not the first Tuesday.

The `gen_pdf.py` script uses two docker images: `tortxof/webdev` and `tortxof/wkhtmltopdf`.
Make sure those are built/pulled before running `gen_pdf.py`.

    cd htmltopdf
    ./gen_pdf.py

The script will generate a pdf of the newsletter and place it in the
`newsletters` directory.
