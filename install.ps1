Write-Output "Hello World!!!"
Write-Output "Starting install"
$client = New-Object System.Net.WebClient
$shell_app = new-object -com shell.application
Write-Output "Dowloading python"
$client.DownloadFile("https://www.python.org/ftp/python/3.5.2/python-3.5.2-webinstall.exe", "python-3.5.2-webinstall.exe")
Start-Process ./python-3.5.2-webinstall PrependPath=1 -Wait
Remove-Item python-3.5.2-webinstall.exe

New-Item dll -type directory -force
Write-Output "Installing SPTrader"
$filename_sptrader = "SPAPIDLL_R8.742_WIN32.zip"
$client.DownloadFile("http://spsystem.info/download/API/R8742/$($filename_sptrader)",
"dll/" + $filename_sptrader)
$zip_file = $shell_app.namespace((Get-Location).Path + "\dll\$filename_sptrader")
$destination = $shell_app.namespace((Get-Location).Path + "\dll")
$destination.Copyhere($zip_file.items())
Remove-Item "dll/$($filename_sptrader)"
pip install cffi

Write-Output "Installing openssl"
$shell_app = new-object -com shell.application
$client.DownloadFile("https://indy.fulgan.com/SSL/openssl-1.0.2h-i386-win32.zip",
"dll/openssl-1.0.2h-i386-win32.zip")
$zip_file = $shell_app.namespace((Get-Location).Path + "\dll\openssl-1.0.2h-i386-win32.zip")
$destination = $shell_app.namespace((Get-Location).Path + "\dll")
$destination.Copyhere($zip_file.items())
Remove-Item "dll/openssl-1.0.2h-i386-win32.zip"

Write-Output "Press any key to finish"
$x = $host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
