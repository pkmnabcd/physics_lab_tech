@echo off

for %%f in (OH_Andover_ALO*day*.dat) do (
  .\chileTempCleanerAndGrapher.bat %%f
)
:: Make a c++ program that does this instead so it can filter them properly
