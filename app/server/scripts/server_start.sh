#!/usr/bin/env bash

/bin/bash -c '/apps/inst_edu_backend/env.sh'
/apps/venv/bin/gunicorn -b 127.0.0.1:8000 -w 4 -k uvicorn.workers.UvicornWorker main:api --name instedu_svc --chdir /apps/inst_edu_backend --access-logfile /apps/logs/instedu_api/access.log --error-logfile /apps/logs/instedu_api/errors.log --user apiuser