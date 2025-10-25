# Client-server testing

## Task 1

Evaluate the code of `app/main.py` and `client.py` and provide a brief overview of potential problems which may affect the reliability and/or performance of the server, client and their interaction. Feel free to provide ideas about fixing said problems.

## Task 2

Start the server-side applications (see "Running apps" below), then execute file `client.py`. You should see an output `Minimum Python version: ~=x.y` with some values of `x` and `y`.

Write at least two basic end-to-end tests that cover some aspects of client-server interaction.

Write at least two basic unit tests: one for testing the server app, one for testing the client app. Unit tests may cover any aspect of any part of code, small or big.

## Task 3

Document your solution to task 2. The documentation must _briefly_ explain how to get it up & running. The target audience for this technical documentation are imaginary fellow developers, who would have to productize, evolve, support and maintain it.

## Running apps

Requirements:

1. Docker
2. Python 3.10+

Start the apps with `docker compose up -d --build`. Navigate to `http://localhost:8000/` and enter username `user` and password `password`. Verify that the resulting web page shows a JSON document.

Note: The `data` container is only accessed by the server and it is serving the required example data.

What technology to use?

The only requirement is to use Python. Otherwise it is up to you which tech stack to use, including testing framework and/or related packages. Bare-bones pytest is also fine.

There are only practical limitations, all related to the fact that we want to try and run your solution:

- Please use only open source software. No commercial software.
- Please use only technologies that one can try, once it's set up, offline. No
  cloud-based solutions.
- Also we kindly ask you not to publish the solution source anywhere either.
- Please use only stable releases. No nightly builds.
- Please make it reasonably straightforward for us to try your solution.


## Project Structure
```
├── ...
├── app
│   ├── __init__.py
│   └── main.py
│
├── client.py
├── compose.yaml
├── data.json
├── Dockerfile
├── pytest.ini
├── README.md
├── requirements.txt
│
├── nginx
│   ├── .htpasswd
│   ├── nginx.conf
│   └── nginx-data.conf
│
├── tests
│   ├── e2e
│   │   └── test_e2e.py
│   └── unittests
│       ├── test_client.py
│       └── test_server.py
│
├── __pycache__/
├── .pytest_cache/
├── .vscode/
```