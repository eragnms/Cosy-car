Cosycar
----------

Helps keep your car cosy during cold days...

Install and run
================

The script can be invoked by:
- cd into the directory /cosycar and execute

  $ python -m cosycar

or with

  $ ./cosycar-runner.py

Install the script with (cd into the root of the project):

  $ pip install .
  $ cp ~/.config/cosycar_template.cfg ~/.config/cosycar.cfg

After installation of the script it can be invoked with:

  $ cosycar

Docker
========

Build the container (cd into the root of the project):

  $ docker build -t cosycar .

Run integration test:

  $ docker run cosycar integration

Run cosycar:

  $ docker run cosycar [params]


