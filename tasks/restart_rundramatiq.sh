#!/bin/bash
curl -n -X POST https://api.heroku.com/apps/project-management-novaone/dynos \
  -d '{
  "attach": false,
  "command": "python manage.py rundramatiq",
  "env": {
    "COLUMNS": "80",
    "LINES": "24"
  },
  "force_no_tty": null,
  "size": "Hobby",
  "type": "run",
  "time_to_live": 1800
}' \
  -H "Content-Type: application/json" \
  -H "Accept: application/vnd.heroku+json; version=3"

curl -n -X DELETE https://api.heroku.com/apps/project-management-novaone/dynos \
  -H "Content-Type: application/json" \
  -H "Accept: application/vnd.heroku+json; version=3"
