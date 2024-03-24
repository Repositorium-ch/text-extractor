#!/bin/bash

# author: martin@affolter.net

. _docker.sh
. _config.sh

. build.sh

is_container_running "$containername"

datafolder="$(pwd)/data/"
if test -f "$datafolder"; then
  echo "Server-Folder \"$datafolder\" does not exist"
fi

scriptsfolder="$(pwd)/scripts"
if test -f "$scriptsfolder"; then
  echo "Server-Folder \"$scriptsfolder\" does not exist"
fi

datavolume="$datafolder:/usr/src/data"
scriptsvolume="$scriptsfolder:/usr/src/scripts"

# create the container
docker run -d -p 8080:5000 -e "API_KEY=test" -v "$datavolume" -v "$scriptsvolume" --name "$containername" "$containername:$tagname"

# start a bash shell inside the running Docker container
# docker exec -it unstructured bash