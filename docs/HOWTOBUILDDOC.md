In order to build documentation use custome docker container:

    $ docker run -it -v <PATH_TO_REPO>/ansible-pan/:/documents/ ivanbojer/spinx-with-rtd
    $ cd docs
    $ make modulesasmd
