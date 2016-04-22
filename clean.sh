#! /bin/bash

rm db_flask_blog_dev.sqlite

find . -name "*~" | xargs rm
find . -name "*.pyc" | xargs rm
