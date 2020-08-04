#!/bin/bash
curl -n -X DELETE https://api.heroku.com/apps/project-management-novaone-two/dynos \
  -H "Content-Type: application/json" \
  -H "Accept: application/vnd.heroku+json; version=3" \
  -H "Authorization: Bearer 4a0eca9f-36a3-4a2c-a398-a158f5cc48c5"

curl -n -X POST https://api.heroku.com/apps/project-management-novaone-two/dynos \
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
  -H "Accept: application/vnd.heroku+json; version=3" \
  -H "Authorization: Bearer 4a0eca9f-36a3-4a2c-a398-a158f5cc48c5"
