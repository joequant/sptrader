cd ..
If (Test-Path sptrader.zip) {
   Remove-Item sptrader.zip
}
Compress-Archive -Path sptrader\*.md -DestinationPath sptrader.zip
Compress-Archive -Path sptrader\*.ps1 -Update -DestinationPath sptrader.zip
Compress-Archive -Path sptrader\*.psm -Update -DestinationPath sptrader.zip
Compress-Archive -Path sptrader\sptrader\*.py -Update -DestinationPath sptrader.zip
Compress-Archive -Path sptrader\static\*.html -Update -DestinationPath sptrader.zip
Compress-Archive -Path sptrader\static\*.css -Update -DestinationPath sptrader.zip
Compress-Archive -Path sptrader\static\*.js -Update -DestinationPath sptrader.zip
Compress-Archive -Path sptrader\tests\*.py -Update -DestinationPath sptrader.zip
