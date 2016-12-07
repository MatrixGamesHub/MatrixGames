@PUSHD %~dp0


:CLEAN
@echo [ clean up ... ]
@FOR /D %%f in (dist build) DO @IF EXIST %%f @RD /s /q "%%f"
@FOR /D /R . %%f in (__pycache__) DO @IF EXIST %%f @RD /s /q "%%f"
@GOTO DONE


:DONE
@POPD
