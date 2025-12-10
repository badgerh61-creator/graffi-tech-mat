@echo off
wmic logicaldisk get freespace,size,caption > disk_report.txt

for /f "skip=1 tokens=1,2,3" %%A in ('wmic logicaldisk get freespace,size,caption') do (
  set FS=%%B
  if "!FS!"=="" goto :continue
  if %%B lss 5000000000 (
    echo WARNING: Drive %%A has low space: %%B bytes
  )
  :continue
)

echo Storage validation complete.
exit /b 0
