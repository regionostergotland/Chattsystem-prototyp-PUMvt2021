@echo off
if exist "compiled-javascript" (
    if exist "compiled-javascript\*.js" (
        del "compiled-javascript\*.js"
    )
    rmdir "compiled-javascript"
)