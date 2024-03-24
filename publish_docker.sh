#!/bin/sh

# author: martin@affolter.net

. _config.sh

doctl registry login

cnt="${containername}_amd64:$tagname"

docker buildx create --use --name mybuilder --platform linux/amd64

# docker buildx build --platform linux/amd64 -t "$cnt" .

# docker tag "$cnt" "registry.digitalocean.com/$registry/$cnt"

# docker push "registry.digitalocean.com/$registry/$cnt"
docker buildx build --platform linux/amd64 -t "registry.digitalocean.com/$registry/$containername:$tagname" --push .
