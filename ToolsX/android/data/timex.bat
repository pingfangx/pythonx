@echo off
rem from:[《dos 计算时间差的方法总结》](http://blog.pingfangx.com/2392.html)
rem thanks:[dudubird.《批处理计算时间差的方法总结》](http://conducer.blog.51cto.com/841262/1377650)
set start_file_name=%~dp0start_time.txt
if "%1%"=="save" goto save
for /f "tokens=1,2" %%i in (%start_file_name%) do (
    set start_date=%%i
    set start_time=%%j
)
rem echo %start_date%
rem echo %start_time%

set /a start_year=%start_date:~0,4%
set /a start_month=1%start_date:~5,2%-100
set /a start_day=1%start_date:~8,2%-100


set /a start_hour=%start_time:~0,2%
set /a start_minute=1%start_time:~3,2%-100
set /a start_second=1%start_time:~6,2%-100

rem echo %start_year%
rem echo %start_month%
rem echo %start_day%
rem echo %start_hour%
rem echo %start_minute%
rem echo %start_second%



set current_date=%date%
set current_time=%time%

set /a current_year=%current_date:~0,4%
set /a current_month=1%current_date:~5,2%-100
set /a current_day=1%current_date:~8,2%-100


set /a current_hour=%current_time:~0,2%
set /a current_minute=1%current_time:~3,2%-100
set /a current_second=1%current_time:~6,2%-100

rem echo %current_year%
rem echo %current_month%
rem echo %current_day%
rem echo %current_hour%
rem echo %current_minute%
rem echo %current_second%


if %current_hour% LSS %start_hour% set /a current_hour=%current_hour%+24
set /a ts1=%start_hour%*3600+%start_minute%*60+%start_second%
set /a ts2=%current_hour%*3600+%current_minute%*60+%current_second%
set /a ts=%ts2%-%ts1%
set /a h=%ts%/3600
set /a m=(%ts%-%h%*3600)/60
set /a s=%ts%%%60

echo spend %h%:%m%:%s%
goto exit

:save
set save_time=%date:~0,10% %time%
echo %save_time% > %start_file_name%
echo save start time: %save_time%

:exit