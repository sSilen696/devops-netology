#!/bin/bash
# display command line options

count=1
while [[ -n "$1" ]]; do    
    echo "\$* Parameter #$count = $param"
    count=$(( $count + 1 ))
done
