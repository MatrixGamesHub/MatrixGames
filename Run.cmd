@ECHO OFF
CLS
PUSHD %~dp0
CD ./GameConsole/src

@ECHO ON
start C:\PythonVirtualEnv\MatrixGames\Scripts\python GameConsole.py
@ECHO OFF

POPD
