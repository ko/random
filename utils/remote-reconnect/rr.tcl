#!/usr/bin/expect -f

set ip [lindex $argv 0]
set username [lindex $argv 1]
set password [lindex $argv 2]
spawn telnet -l $username $ip
expect -re "Password:"
send "sunStone\n"
interact
