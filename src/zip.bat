@echo off
set ZIP=C:\PROGRA~1\7-Zip\7z.exe a -tzip -y -r
set REPO=the_old_switcheroo
set VERSION=0.0.1

fsum -r -jm -md5 -d%REPO% * > checksum.md5
move checksum.md5 %REPO%/checksum.md5

quick_manifest.exe "The Old Switcheroo" "%REPO%" >%REPO%/manifest.json

echo %VERSION% >%REPO%/VERSION

REM %ZIP% %REPO%_v%VERSION%_Anki20.zip *.py %REPO%/*

cd %REPO%
%ZIP% ../%REPO%_v%VERSION%_Anki21.ankiaddon *

%ZIP% ../%REPO%_v%VERSION%_CCBC.adze *
