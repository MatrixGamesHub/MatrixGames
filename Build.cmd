@PUSHD %~dp0
@SET PYTHON=C:\PythonVirtualEnv\MatrixGames\Scripts\python.EXE
@SET IMG2PY=C:\PythonVirtualEnv\MatrixGames\Scripts\img2py.exe
@SET CONVERT=C:\PythonVirtualEnv\MatrixGames\Scripts\convert.exe
@IF NOT EXIST %PYTHON% GOTO ERROR


:RUN
@CALL Clean.cmd
@echo [ creating icons ... ]
@%PYTHON% Applications\IconCreator\IconCreator.py build

@echo [ creating python resource file ... ]
@%IMG2PY% -f    -c -n logo_16   .\build\logo_016x016.png   .\build\Images.py
@%IMG2PY% -f -a -c -n logo_32   .\build\logo_032x032.png   .\build\Images.py
@%IMG2PY% -f -a -c -n logo_48   .\build\logo_048x048.png   .\build\Images.py
@%IMG2PY% -f -a -c -n logo_64   .\build\logo_064x064.png   .\build\Images.py
@%IMG2PY% -f -a -c -n logo_128  .\build\logo_128x128.png   .\build\Images.py
@%IMG2PY% -f -a -c -n logo_256  .\build\logo_256x256.png   .\build\Images.py
@%IMG2PY% -f -a -c -n logo_512  .\build\logo_512x512.png   .\build\Images.py

@echo [ copy python resource file ... ]
@copy /Y .\build\Images.py .\Applications\GameConsole\res\

@echo [ creating windows icon (*.ico) ... ]
@%CONVERT% .\build\logo_016x016.png .\build\logo_032x032.png .\build\logo_048x048.png .\build\logo_064x064.png .\build\logo_128x128.png .\build\logo_256x256.png .\build\logo.ico

@echo [ building application ... ]
@%PYTHON% Setup.py build
@GOTO DONE


:ERROR
@ECHO ON
@ECHO.
@ECHO You need the python virtual environment. Please visit http://www.matrixgames.rocks/developers.php
@ECHO OFF
@GOTO DONE


:DONE
@echo [ Done! ]
@POPD
