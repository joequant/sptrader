$ScriptDir = Split-Path -parent $MyInvocation.MyCommand.Path
Import-module $ScriptDir\modules

hello_world
Write-Output "Starting install"

Write-Output "Downloading python"
wget "https://www.python.org/ftp/python/3.5.2/python-3.5.2-webinstall.exe" -OutFile "$($env:TEMP)/python-3.5.2-webinstall.exe"
Start-Process "$($env:TEMP)/python-3.5.2-webinstall.exe" "PrependPath=1 InstallAllUsers=1 Include_test=0" -Wait
Remove-Item "$($env:TEMP)/python-3.5.2-webinstall.exe"
$env:Path += ";c:\\Program Files (x86)\\Python35-32\\Scripts"
Start-Process pip "install cffi Flask gevent" -Verb runAs

Write-Output "Downloading VC redistribution"
wget "http://download.microsoft.com/download/1/6/5/165255E7-1014-4D0A-B094-B6A430A6BFFC/vcredist_x86.exe" -OutFile "$($env:TEMP)/vcredist_x86.exe"
Write-Output "Installing VC redistribution"
Start-Process "$($env:TEMP)/vcredist_x86" -Wait
Remove-Item "$($env:TEMP)/vcredist_x86.exe"

New-Item dll -type directory -force
unzip -filename "SPAPIDLL_R8.742_WIN32.zip" -url http://spsystem.info/download/API/R8742 -dir dll -name SPTrader
unzip -filename openssl-1.0.2h-i386-win32.zip -url "https://indy.fulgan.com/SSL/" -dir dll -name OpenSSL
Pause

