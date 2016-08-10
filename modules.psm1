function hello_world {
Write-Output "Hello world!"
}

$shell_app = new-object -com shell.application

function unzip($filename, $url, $dir, $name) {
Write-Output "Installing $($name)"
wget "$($url)/$($filename)" -OutFile "$($dir)\\$($filename)"
$zip_file = $shell_app.namespace((Get-Location).Path + "\" + $dir +"\" + $filename)
$destination = $shell_app.namespace((Get-Location).Path + "\" + $dir)
$destination.Copyhere($zip_file.items())
Remove-Item "$($dir)\\$($filename)"
}

function Pause {
Write-Output "Press any key to finish"
$x = $host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
}

export-modulemember -Function hello_world, unzip, Pause

