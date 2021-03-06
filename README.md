# CampusCircle

## What is this?

This is a simple client for getting the calendar from the _NS Solutions CampusSquare_ portal (aka _Loyola_ at Sophia University, _TWINS_ at Tsukuba University...) and outputting them in a nicer and more modern format.

Note: I have stopped developing this as I no longer need this or have a way to test this, since I have finished my exchange semester at a university using this.

## Why?

I got tired of having to log in _every single time_ I wanted to check my schedule. Also, CampusSquare is kind of slow, so loading it, logging in and then finding my schedule would take a moment.

Oh, and it `alert`s you after 15 minutes because you're logged out, which tends to steal focus on Firefox for Android.

## Running this and stuff

This currently uses WSGI as I'm hosting it on a shared server using _Phusion Passenger_.
Currently this requires you to put your username and password in the config.json file.

To run this locally, I use `uwsgi`:

```
pip install -r requirements.txt
cd public_python
uwsgi --yaml config.yaml:app
```
I recommend setting up a virtualenv for this.

As the frontend is written in Elm, you may wanna use elm-live if you want to work on this.

## Other stuff

I have absolutely no connection to NS Solutions or CampusSquare, other than having to use it at my university.

## Other things you may want to take a look at

There's a client called [_Twin:te_](https://github.com/HikaruEgashira/twinte_frontend) by Github user @HikaruEgashira which I found while making this, however this is not based on it.
