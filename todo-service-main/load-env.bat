@echo off
for /f "tokens=1,2 delims==" %%G in (.env) do (
    set %%G=%%H
)
