#!/bin/bash

rm -rf tmp 2>/dev/null
mkdir tmp 2>/dev/null
cd tmp

function split_gif() {
    ANIMATED=$1
    convert ../$ANIMATED -scene 1 +adjoin frame_%04d.gif
}

function scale_down() {
    FRAME=$1
    convert $FRAME -resize 10x10 -trim +repage TRIMMED_$FRAME
}

function get_rgb_at() {
    FRAME=$1
    X_POS=$2
    Y_POS=$3

    convert $FRAME -format "%[fx:int(255*r)],%[fx:int(255*g)],%[fx:int(255*b)]" info:
}

function get_rgb_for() {
    
    FRAME=$1
    convert $FRAME txt:- | \
        xargs -L1 echo | \
        sed -e 's,#.*$,,'
}

split_gif pacman.gif
for F in `ls -1 | grep frame_`
do
    scale_down $F
    get_rgb_for TRIMMED_$F >> RGB_VALS.txt
done

