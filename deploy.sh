#!/usr/bin/env bash
task sops:lock
git commit -am "$*" && task flux:deploy
