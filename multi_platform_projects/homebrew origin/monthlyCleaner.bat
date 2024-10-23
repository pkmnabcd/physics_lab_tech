@echo off

for %%f in (OH_Andover_ALO*day*.dat) do (
  .\chileTempCleanerAndGrapher.bat %%f
)
