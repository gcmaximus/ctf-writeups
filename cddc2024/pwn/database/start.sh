#!/bin/bash

nsjail -Ml --port 18439 --user 99999 --group 99999 --time_limit 30 --chroot /jail -- database
