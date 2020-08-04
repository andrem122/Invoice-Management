#!/bin/bash
curl -n -X DELETE https://api.heroku.com/apps/project-management-novaone-two/dynos \
  -H "Content-Type: application/json" \
  -H "Accept: application/vnd.heroku+json; version=3" \
  -H "Authorization: Bearer $HEROKU_API_KEY"

curl -n -X POST https://api.heroku.com/apps/project-management-novaone-two/dynos \
  -d '{
  "attach": false,
  "command": "python manage.py rundramatiq",
  "env": {
    "COLUMNS": "80",
    "LINES": "24"
  },
  "force_no_tty": null,
  "size": "Free",
  "type": "run",
  "time_to_live": 1800
}' \
  -H "Content-Type: application/json" \
  -H "Accept: application/vnd.heroku+json; version=3" \
  -H "Authorization: Bearer $HEROKU_API_KEY"
