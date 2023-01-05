Form Manager
============

[![Backend Tests](https://github.com/ScilifelabDataCentre/form-manager/actions/workflows/backend-tests.yml/badge.svg)](https://github.com/ScilifelabDataCentre/form-manager/actions/workflows/backend-tests.yml)
[![codecov](https://codecov.io/github/ScilifelabDataCentre/form-manager/branch/main/graph/badge.svg?token=MQX98Q3NYU)](https://codecov.io/github/ScilifelabDataCentre/form-manager)
[![Black formatting](https://github.com/ScilifelabDataCentre/form-manager/actions/workflows/python-black.yml/badge.svg)](https://github.com/ScilifelabDataCentre/form-manager/actions/workflows/python-black.yml)
[![CodeQL](https://github.com/ScilifelabDataCentre/form-manager/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/ScilifelabDataCentre/form-manager/actions/workflows/codeql-analysis.yml)
[![Trivy Scan](https://github.com/ScilifelabDataCentre/form-manager/actions/workflows/trivy.yaml/badge.svg)](https://github.com/ScilifelabDataCentre/form-manager/actions/workflows/trivy.yaml)

Form Manager is a simple system (backend/frontend) to receive web form `POST` submissions.

Login is performed using OpenID connect. There is no internal user account management.

When a form is added, it will be given a unique ID. Form submission can then be done using POST to `/api/v1/form/<identifier>/incoming`. The full url for submissions is also available:  `/api/v1/form/<identifier>/url`.

Features:
* Send the form submission to an email address
* Recaptcha validation (v2 confirmed to work)
* Redirection to wanted page after submission

Created using:
* Database: MongoDB
* Backend: Python (Flask)
* Frontend: Vue (Quasar)

The backend can be found in the `form_manager` folder, while the frontend is found in `frontend`.


## Configuration

All configuration options are listed in `form_manager/conf.py`. Modify that file to change the configuration.


## Development

A complete development environment can be activated locally by running:

```
docker-compose --profile dev up
```

It will set up a database, a mail catcher, and one instance each of the backend and frontend, reachable at [http://localhost:5050](http://localhost:5050). The backend and frontend instance will use your local code, adapting to your changes.

If `FLASK_ENV` is set to `development` (done by default if you run the above command), you can log in by using the endpoint [http://localhost:5050/api/v1/development/login/linus@example.com](http://localhost:5050/api/v1/development/login/linus@example.com), where `linus@example.com` may be exchanged to any email you want to log in as.

The easiest way to use development environment is to paste the url to the login endpoint in a web browser, and then open [http://localhost:5050](http://localhost:5050) to use the system.


## Testing

The tests can be run using the command:

```
docker-compose --profile testing up --exit-code-from test
```


## Required Run Environment

Form manager require a MongoDB instance, as well an instance of the frontend and backend. See the `docker-compose.yml` file.

Backend and frontend container images are available from Packages in the Github repository.
