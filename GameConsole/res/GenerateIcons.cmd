@echo off
pushd %~dp0

call C:\Python34\Scripts\img2py -f    -c -n logo_16   .\icon\logo_16x16.png   Images.py
call C:\Python34\Scripts\img2py -f -a -c -n logo_32   .\icon\logo_32x32.png   Images.py
call C:\Python34\Scripts\img2py -f -a -c -n logo_48   .\icon\logo_48x48.png   Images.py
call C:\Python34\Scripts\img2py -f -a -c -n logo_64   .\icon\logo_64x64.png   Images.py

move Images.py ..\src\res\

popd
