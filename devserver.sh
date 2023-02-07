export JEKYLL_VERSION=4.2.2
podman run --rm \
  -v $(pwd):/srv/jekyll \
  -p 4000:4000 \
  docker.io/jekyll/jekyll:$JEKYLL_VERSION \
  jekyll serve
