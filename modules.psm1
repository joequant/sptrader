function hello_world {
Write-Output "Hello world!"
}

$shell_app = new-object -com shell.application

function unzip($filename, $url, $dir, $name) {
Write-Output "Installing $($name)"
wget "$($url)/$($filename)" -OutFile "$($dir)\\$($filename)"
Expand-Archive -Path "$($dir)\\$($filename)" -Destination "$($dir)" -Force
Remove-Item "$($dir)\\$($filename)"
}

function Pause {
Write-Output "Press any key to finish"
$x = $host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
}

export-modulemember -Function hello_world, unzip, Pause

