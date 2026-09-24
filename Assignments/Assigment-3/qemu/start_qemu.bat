@echo off

echo ========================================
echo QEMU Embedded Device Simulation
echo ========================================

echo.
echo Starting QEMU...
echo.

REM --------------------------------------------------
REM Replace this section with your actual QEMU
REM configuration.
REM --------------------------------------------------

REM Example:
REM
REM qemu-system-x86_64 ^
REM     -m 1024 ^
REM     -drive file=images\embedded.qcow2,if=virtio ^
REM     -netdev user,id=n1,hostfwd=tcp::8080-:5000 ^
REM     -device virtio-net-pci,netdev=n1 ^
REM     -nographic

echo QEMU configuration must be changed
echo according to your embedded platform.

pause