@ECHO OFF
CLS
PUSHD %~dp0
CD src


IF NOT EXIST C:\Python34\python.exe GOTO ALTERNITIVE

@ECHO ON
C:\Python34\python.exe GameConsole.py
@ECHO OFF
GOTO DONE

:ALTERNITIVE
@ECHO ON
python GameConsole.py
@ECHO OFF

:DONE

POPD
