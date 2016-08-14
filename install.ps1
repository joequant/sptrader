$ScriptDir = Split-Path -parent $MyInvocation.MyCommand.Path
Import-module $ScriptDir\modules

#filenames
$pyversion = "3.5.2"
$pyfile = "python-$($pyversion)-webinstall.exe"
$pypath = "c:\\Program Files (x86)\\Python35-32\\Scripts"
$vcredist = "vcredist_x86.exe"
$spzipfile = "SPAPIDLL_R8.742_WIN32.zip"
$sslzipfile = "openssl-1.0.2h-i386-win32.zip"

#start
hello_world
Write-Output "Starting install"
Write-Output "Downloading python"
wget "https://www.python.org/ftp/python/$($pyversion)/$($pyfile)" -OutFile "$($env:TEMP)/$($pyfile)"
Start-Process "$($env:TEMP)/$($pyfile)" "PrependPath=1 InstallAllUsers=1 Include_test=0" -Wait
Remove-Item "$($env:TEMP)/$($pyfile)"
$env:Path += ";$($pypath)"
Start-Process pip "install cffi Flask gevent" -Verb runAs

Write-Output "Downloading VC redistribution"
wget "http://download.microsoft.com/download/1/6/5/165255E7-1014-4D0A-B094-B6A430A6BFFC/$($vcredist)" -OutFile "$($env:TEMP)/$($vcredist)"
Write-Output "Installing VC redistribution"
Start-Process "$($env:TEMP)/$($vcredist)" -Wait
Remove-Item "$($env:TEMP)/$($vcredist)"

New-Item dll -type directory -force
unzip -filename $spzipfile -url http://spsystem.info/download/API/R8742 -dir dll -name SPTrader
unzip -filename $sslzipfile -url "https://indy.fulgan.com/SSL/" -dir dll -name OpenSSL
Pause

