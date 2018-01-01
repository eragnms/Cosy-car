Cosycar
----------

Helps keep your car cosy during cold days.

The script will help with controlling one or more heaters in a car. The heaters
must be controlled over a Z-wave network with a Vera controller.

The user tells the script that the car is about to leave at a certain time and
the script will then start the heaters at a appropriate time ahead of the
departure. When to start the heaters is determined by the script through a
function that uses the temperature and a table specifying the amount of energy
required for a certain temperature. The temperature is fetched from Wunderground
and thus one needs to acquire a wunder key at their site. The wunder key should
be specified in the configuration file of the script together with the location
of the car.

The energy table specifying the amount of energy required for a certain
temperature is specified in the configuration file that comes with the script.
It is up to the user to set up a energy table that suites his car.

One can use the switches -l, -s or -a to tell the script of departure times.
Alternatively one can define a gmail account in the configuration file (also
set the "check_email" switch to True) to which one can email departure times.
If an email is sent to the gmail address with a subject on the format HHMM a
departure time will be set by the script. By sending an email with the subject
"Cancel" or "cancel" a departure time that has been set will be deleted. 
The script can only deal with one departure time at a time.

If the current time is 19:00 on a Tuesday and a departure time is set to
"20:15" with the -a switch or to "2015" in an email then the departure time
will be at 15 minutes past eight on the same Tuesday evening.
If the current time is 19:00 on a Tuesday and a departure time is set to
"07:15" with the -a switch or to "0715" in an email then the departure time
will be at 15 minutes past seven on Wednesday morning. Thus it is not currently
possible to set a departure time further into the future than 24 hours.

The script should be executed with some interval by for example a cron job on a
server and will then check if any of the heaters should be running at the
moment. If any heater should run, the script will start them, respectively stop
any heaters that should not run. To check if any heaters should run, run the
script with the switch -c.

The configuration file is be installed in the folder $HOME/.config when the
script is installed.

In the configuration file the user can connect a number of heaters to sections
of the car. For example one can place a block heater in the engine and one
compartment heater in the compartment of the car. One also defines the power
of each heater in the configuration file.

Installation
================

Install the script with (cd into the root of the project):

  $ pip install --user .

Then copy or merge the configuration template file into the configuration file.

  $ cp ~/.config/cosycar_template.cfg ~/.config/cosycar.cfg

Run the script
===============

The script can after installtion be run with:

  $ $HOME/.local/bin/cosycar 

Testing
=========

The script can be invoked by:
- cd into the directory /cosycar and execute

  $ python -m cosycar

or with

  $ ./cosycar-runner.py

To install in a virtual env:

  $ pip install .

Unittests can be run with:

  $ python -m unittest

Docker
========

(Docker support is not fully implemented nor tested yet)

Build the container (cd into the root of the project):

  $ docker build -t cosycar .

Run integration test:

  $ docker run cosycar integration

Run cosycar:

  $ docker run cosycar [params]


