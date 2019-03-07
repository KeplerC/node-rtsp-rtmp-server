#!/bin/sh

sudo coffee server.coffee | python3 latency.py
