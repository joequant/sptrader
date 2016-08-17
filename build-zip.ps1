cd ..
Compress-Archive -Path sptrader\*.md -DestinationPath sptrader.zip
Compress-Archive -Path sptrader\*.ps1 -Update -DestinationPath sptrader.zip
Compress-Archive -Path sptrader\*.psm -Update -DestinationPath sptrader.zip
Compress-Archive -Path sptrader\sptrader -Update -DestinationPath sptrader.zip
Compress-Archive -Path sptrader\static -Update -DestinationPath sptrader.zip
Compress-Archive -Path sptrader\tests -Update -DestinationPath sptrader.zip
