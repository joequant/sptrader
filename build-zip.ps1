cd ..
Remove-Item build -Force -Recurse
New-Item -ItemType directory build -Force
cd build
If (Test-Path sptrader.zip) {
   Remove-Item sptrader.zip
}
New-Item -ItemType directory sptrader
New-Item -ItemType directory sptrader\sptrader
New-Item -ItemType directory sptrader\static
New-Item -ItemType directory sptrader\tests
Copy-Item ..\sptrader\*.md sptrader
Copy-Item ..\sptrader\*.ps1 sptrader
Copy-Item ..\sptrader\*.psm sptrader
Copy-Item ..\sptrader\*.json sptrader
Copy-Item ..\sptrader\sptrader\*.py sptrader\sptrader
Copy-Item ..\sptrader\static\*.html sptrader\static
Copy-Item ..\sptrader\static\*.css sptrader\static
Copy-Item ..\sptrader\static\*.js sptrader\static
Copy-Item ..\sptrader\tests\*.py sptrader\tests
Compress-Archive -Path sptrader -DestinationPath sptrader.zip
