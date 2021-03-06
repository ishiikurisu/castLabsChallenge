# castLabs Python Programming Challenge

This is my take on the [castLabs programming task](https://github.com/castlabs/python_programming_task).

This repo implements a [RFC2616](https://www.ietf.org/rfc/rfc2616.txt) proxy
that appends a new field to the request as specified in the task.


## Prepare

Create a JSON file named `config/secrets.json` inside the `src` folder 
with the proxy's secrets. It may contain one of the following fields:

- `JWT_SECRET` with the secret hex string for the appended JWT
- `UPSTREAM` with the upstrea URL for this proxy.

It should look like this:

``` json
{
    "JWT_SECRET": "SUPER SECRET HEX STRING",
    "UPSTREAM": "https://reqres.in/api/users"
}
```

## Execute

It's possible to use Docker to execute the application using Docker:

```
docker-compose build
docker-compose up
```

This will start the application on port 5000.


## Develop

It's recommended to use `virtualenv` to execute the app locally.
On Unix systems, you can use the following:

``` sh
python3 -m virtualenv venv -p python3
source venv/bin/activate
```

To install requirements:

``` sh
pip install -r requirements.txt
```

To execute the program locally:

``` sh
export FLASK_APP=app.py
flask run
```

### Testing

There are 2 implemented test suites:

- Running `make test` will execute a couple of unit tests for common functionalities;
- Running `make stress` will verify a proxy that's deployed in another server to verify it works as expected;
