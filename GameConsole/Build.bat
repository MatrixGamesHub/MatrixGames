@ECHO OFF
CLS
PUSHD %~dp0


IF NOT EXIST C:\Python34\python.exe GOTO ALTERNITIVE

@ECHO ON
C:\Python34\python.exe Make_win.py compile
@ECHO OFF
GOTO DONE

:ALTERNITIVE
@ECHO ON
python Make_win.py compile
@ECHO OFF

:DONE

POPD
