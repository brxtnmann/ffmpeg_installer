@echo off
setlocal

"C:\Users\YourName\AppData\Local\Programs\Python\Python39\python.exe" "%~dp0gif_converter.py" %*

set /p add_shortcut=Do you want to add a shortcut to the desktop? (y/n): 
if /i "%add_shortcut%"=="y" (
    echo Creating shortcut...
    set shortcut_target="%~dp0run_gif_converter.bat"
    set shortcut_location="%userprofile%\Desktop\GifConverter.lnk"
    mklink /h "%shortcut_target%" "%shortcut_location%"
    if !errorlevel! == 0 (
        echo Shortcut created on desktop.
    ) else (
        echo Failed to create shortcut.
    )
)

endlocal
pause