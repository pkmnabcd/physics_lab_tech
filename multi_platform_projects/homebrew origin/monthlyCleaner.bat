@echo off

for ($file in Get-ChildItem | Where-Object {$_.Name -match "OH_Andover_ALO[0-9][0-9]day[0-1]{1,3}.dat$" } Select-Object Name) {
  .\chileTempCleanerAndGrapher.bat $file.Name
}
