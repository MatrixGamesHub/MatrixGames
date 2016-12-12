@ECHO OFF

PUSHD %~dp0
SET BUILD_DIR=build
SET DIST_DIR=dist
SET IMAGES_DIST_DIR=%DIST_DIR%\images

SET PYTHON=C:\PythonVirtualEnv\MatrixGames\Scripts\python.EXE
SET IMG2PY=C:\PythonVirtualEnv\MatrixGames\Scripts\img2py.exe
SET CONVERT=C:\PythonVirtualEnv\MatrixGames\Scripts\convert.exe


IF NOT EXIST %PYTHON% CALL :ERROR_ENV
IF NOT EXIST %IMG2PY% CALL :ERROR_ENV
IF NOT EXIST %CONVERT% CALL :ERROR_ENV

IF ERRORLEVEL 1 GOTO DONE

IF "%1" == "" CALL :HELP
IF "%1" == "all" CALL :ALL
IF "%1" == "app" CALL :SERVICE
IF "%1" == "clean" CALL :CLEAN


:DONE
    IF ERRORLEVEL 1 (
        ECHO build faulty
    ) ELSE (
        ECHO build successful
    )
    POPD
    EXIT /B %ERRORLEVEL%

::--------------------------------------------------------------------------------------

:ERROR_ENV
    ECHO.
    ECHO You need the python virtual environment. Please visit http://www.matrixgames.rocks/developers.php
    EXIT /B 1


:ERROR_CLEAN
    ECHO.
    ECHO Could not clean up the environment. Make sure that the build and dist directories are not in use.
    EXIT /B 1


:HELP
    ECHO.Please use `Make ^<target^>` where ^<target^> is one of
    ECHO.  all        clean up environment and build all targets
    ECHO.  app        builds the application
    ECHO.  clean      clean up environment
    ECHO.
    EXIT /B 0


:ALL
    CALL :CLEAN
    CALL :CREATE_ENV
    CALL :BUILD_APP
    CALL :CLEAN_BUILD
    EXIT /B %ERRORLEVEL%


:APP
    CALL :CLEAN
    CALL :CREATE_ENV
    CALL :BUILD_APP
    CALL :CLEAN_BUILD
    EXIT /B %ERRORLEVEL%


:CLEAN
    IF ERRORLEVEL 1 EXIT /B %ERRORLEVEL%
    ECHO [ clean up ... ]
    FOR /D %%f in (%DIST_DIR%, %BUILD_DIR%) DO IF EXIST %%f RD /s /q "%%f"
    FOR /D /R . %%f in (__pycache__) DO IF EXIST %%f RD /s /q "%%f"

    IF EXIST %BUILD_DIR% CALL :ERROR_CLEAN
    IF EXIST %DIST_DIR% CALL :ERROR_CLEAN

    IF ERRORLEVEL 1 EXIT /B %ERRORLEVEL%

    ECHO [ clean up done ]
    ECHO.
    EXIT /B %ERRORLEVEL%


:CLEAN_BUILD
    IF ERRORLEVEL 1 EXIT /B %ERRORLEVEL%
    ECHO [ clean build directory ... ]
    FOR /D %%f in (%BUILD_DIR%) DO IF EXIST %%f RD /s /q "%%f"
    ECHO [ clean build directory done ]
    ECHO.
    EXIT /B %ERRORLEVEL%


:CREATE_ENV
    IF ERRORLEVEL 1 EXIT /B %ERRORLEVEL%
    ECHO [ create build environment ... ]
    IF NOT EXIST %BUILD_DIR% MKDIR %BUILD_DIR%
    IF NOT EXIST %DIST_DIR% MKDIR %DIST_DIR%
    ECHO [ create build environment done ]
    ECHO.
    EXIT /B %ERRORLEVEL%


:BUILD_APP
    IF ERRORLEVEL 1 EXIT /B %ERRORLEVEL%

    ECHO [ creating icons ... ]
    CALL %PYTHON% Applications\IconCreator\IconCreator.py %IMAGES_DIST_DIR%

    IF ERRORLEVEL 1 GOTO BUILD_APP_DONE

    ECHO.
    ECHO [   creating python resource file ... ]
    CALL %IMG2PY% -f    -c -n logo_16  %IMAGES_DIST_DIR%\logo_016x016.png %IMAGES_DIST_DIR%\Images.py
    CALL %IMG2PY% -f -a -c -n logo_32  %IMAGES_DIST_DIR%\logo_032x032.png %IMAGES_DIST_DIR%\Images.py
    CALL %IMG2PY% -f -a -c -n logo_48  %IMAGES_DIST_DIR%\logo_048x048.png %IMAGES_DIST_DIR%\Images.py
    CALL %IMG2PY% -f -a -c -n logo_64  %IMAGES_DIST_DIR%\logo_064x064.png %IMAGES_DIST_DIR%\Images.py
    CALL %IMG2PY% -f -a -c -n logo_128 %IMAGES_DIST_DIR%\logo_128x128.png %IMAGES_DIST_DIR%\Images.py
    CALL %IMG2PY% -f -a -c -n logo_256 %IMAGES_DIST_DIR%\logo_256x256.png %IMAGES_DIST_DIR%\Images.py
    CALL %IMG2PY% -f -a -c -n logo_512 %IMAGES_DIST_DIR%\logo_512x512.png %IMAGES_DIST_DIR%\Images.py

    ECHO.
    ECHO [   move python resource file ... ]
    MOVE /Y %IMAGES_DIST_DIR%\Images.py .\Applications\GameConsole\res\

    ECHO.
    ECHO [   creating windows icon (*.ico) ... ]
    CALL %CONVERT% %IMAGES_DIST_DIR%\logo_016x016.png %IMAGES_DIST_DIR%\logo_032x032.png %IMAGES_DIST_DIR%\logo_048x048.png %IMAGES_DIST_DIR%\logo_064x064.png %IMAGES_DIST_DIR%\logo_128x128.png %IMAGES_DIST_DIR%\logo_256x256.png %IMAGES_DIST_DIR%\logo.ico

    IF ERRORLEVEL 1 GOTO BUILD_APP_DONE

    ECHO [ creating icons done ]

    ECHO.
    ECHO [ build app ... ]
    CALL %PYTHON% setup.py build

    ECHO [ build app done ]
    ECHO.

    :BUILD_APP_DONE
    EXIT /B %ERRORLEVEL%
