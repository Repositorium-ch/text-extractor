#!/bin/sh

# author: martin@affolter.net

. _config.sh

docker build -t "$containername:$tagname" .
