# QEMU Guest Setup

The QEMU configuration depends on the embedded platform.

The intended architecture is:

Windows Host
    |
    | Selenium + Firefox
    |
    v
QEMU
    |
    v
Embedded Linux
    |
    v
Embedded Web Application


## Network

Example:

Host:

127.0.0.1:8080

        |

        v

QEMU Guest:

127.0.0.1:5000


Then configure:

$env:TARGET_URL="http://127.0.0.1:8080"

and run:

behave