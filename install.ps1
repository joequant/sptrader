Import-module ./modules

hello_world
Write-Output "Starting install"
$shell_app = new-object -com shell.application

Write-Output "Downloading python"
wget "https://www.python.org/ftp/python/3.5.2/python-3.5.2-webinstall.exe" -OutFile "$($env:TEMP)/python-3.5.2-webinstall.exe"
Start-Process "$($env:TEMP)/python-3.5.2-webinstall" PrependPath=1 -Wait
Remove-Item "$($env:TEMP)/python-3.5.2-webinstall.exe"

Write-Output "Downloading VC redistribution"
wget "http://download.microsoft.com/download/1/6/5/165255E7-1014-4D0A-B094-B6A430A6BFFC/vcredist_x86.exe" -OutFile "$($env:TEMP)/vcredist_x86.exe"
Write-Output "Installing VC redistribution"
Start-Process "$($env:TEMP)/vcredist_x86" -Wait
Remove-Item "$($env:TEMP)/vcredist_x86.exe"

New-Item dll -type directory -force
Write-Output "Installing SPTrader"
$filename_sptrader = "SPAPIDLL_R8.742_WIN32.zip"
wget "http://spsystem.info/download/API/R8742/$($filename_sptrader)" -OutFile "dll/$($filename_sptrader)"
$zip_file = $shell_app.namespace((Get-Location).Path + "\dll\$filename_sptrader")
$destination = $shell_app.namespace((Get-Location).Path + "\dll")
$destination.Copyhere($zip_file.items())
Remove-Item "dll/$($filename_sptrader)"

Write-Output "Installing openssl"
wget "https://indy.fulgan.com/SSL/openssl-1.0.2h-i386-win32.zip" -OutFile "dll/openssl-1.0.2h-i386-win32.zip"
$zip_file = $shell_app.namespace((Get-Location).Path + "\dll\openssl-1.0.2h-i386-win32.zip")
$destination = $shell_app.namespace((Get-Location).Path + "\dll")
$destination.Copyhere($zip_file.items())
Remove-Item "dll/openssl-1.0.2h-i386-win32.zip"

Write-Output "Press any key to finish"
$x = $host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
