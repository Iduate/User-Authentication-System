@echo off
echo =========================================================
echo    Professional README to Word Document Exporter
echo =========================================================
echo.
echo This will create a comprehensive Word document from your
echo README.md with professional formatting and styling.
echo.

echo Installing required packages...
pip install python-docx
echo.

echo Exporting README.md to professional Word document...
python export_professional_readme.py
echo.

echo =========================================================
echo Export complete! 
echo Check the generated .docx file in this folder.
echo =========================================================
echo.
pause
