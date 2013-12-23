#!/bin/bash
function pause(){
   read -p "$*"
}

python3 "./Brautec starten.py"

pause 'Press [Enter] key to continue...'
