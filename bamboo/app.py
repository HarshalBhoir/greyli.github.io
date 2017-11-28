import sys

from flask import Flask, render_template
from flask_flatpages import FlatPages
from flask_frozen import Freezer

app = Flask(__name__)
app.config.from_pyfile('settings.py')
pages = FlatPages(app)
freezer = Freezer(app)


@app.route('/')
def index():
	completed_pages = (page for page in pages if page.meta.get('complete'))
	sorted_posts = sorted(completed_pages, reverse=True,
                    key=lambda page: page.meta['date'])
	return render_template('index.html', pages=sorted_posts)


@app.route('/tag/<string:tag>/')
def tag(tag):
	tagged_pages = []
	for page in pages:
		if page.meta.get('tags'):
			page_tags = page.meta['tags'].split(',')
			if tag in page_tags:
				tagged_pages.append(page)
	return render_template('tag.html', pages=tagged_pages, tag=tag)


@app.route('/<path:path>/')
def page(path):
    page = pages.get_or_404(path)
    return render_template('page.html', page=page)


@app.route('/tags')
def tags():
	tags = []
	for page in pages:
		if page.meta.get('tags'):
			page_tags = page.meta['tags'].split(',')
			[tags.append(tag) for tag in page_tags if tag not in tags]
	return render_template('tags.html', tags=tags)


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        freezer.freeze()
    else:
        app.run(port=8000)