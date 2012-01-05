#!/bin/bash
grep Naur $1 | cut -d' ' -f3 | xargs ${PREFIX}/quilt add
