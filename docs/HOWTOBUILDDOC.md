Building current documentation
---

The makefile assumes `ansible/ansible` is checked out and in the same directory
as this repo.  If that is the case, then do this from a fresh virtualenv:

1. `pip install jinja2 pyyaml`
1. `make build`


Building the classic documentation
---

In order to build old documentation use custome docker container:

    $ docker run -it -v <PATH_TO_REPO>/ansible-pan/:/documents/ ivanbojer/spinx-with-rtd
    $ cd docs
    $ make modulesasmd
