export JEKYLL_VERSION=3.8
docker run --rm \
  -v $(pwd):/srv/jekyll \
  -p 4000:4000 \
  jekyll/jekyll:$JEKYLL_VERSION \
  jekyll serve
