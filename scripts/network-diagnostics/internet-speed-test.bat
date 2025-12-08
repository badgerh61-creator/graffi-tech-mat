@echo off
REM internet-speed-test.bat
REM Quick download-based speed test using PowerShell (attempts timed download of a small test file).

echo === INTERNET SPEED TEST ===
echo Note: This is a simple heuristic test and depends on endpoint availability.

set URL=https://speed.hetzner.de/100MB.bin
set TMPFILE=%TEMP%\speedtest.tmp

echo Downloading small chunk from %URL% ...
echo (This may take a while depending on network; press Ctrl+C to cancel)
powershell -Command ^
  "$wc = New-Object System.Net.WebClient; ^
   $uri = '%URL%'; ^
   $sw = [Diagnostics.Stopwatch]::StartNew(); ^
   try { ^
     $wc.DownloadFile($uri, '%TMPFILE%'); ^
     $sw.Stop(); ^
     $len = (Get-Item '%TMPFILE%').Length; ^
     $mb = [math]::Round($len/1MB,2); ^
     $secs = [math]::Round($sw.Elapsed.TotalSeconds,2); ^
     $mbps = [math]::Round(($len*8/1MB)/$secs,2); ^
     Write-Output ('Downloaded {0} MB in {1} s -> {2} Mbps' -f $mb, $secs, $mbps) ^
   } catch { Write-Output 'Download failed: ' + $_.Exception.Message } finally { if (Test-Path '%TMPFILE%') { Remove-Item '%TMPFILE%' } }"

echo Speed test finished.
pause
