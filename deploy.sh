#!/usr/bin/env bash
git commit -am "$*" && task flux:deploy
