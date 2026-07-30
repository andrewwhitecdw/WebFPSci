:: Copyright (c) 2021 NVIDIA CORPORATION & AFFILIATES
:: This script requires the Python launcher (py) in the user's path

cd /d "%~dp0"

start py -m http.server 8000 
timeout /t 2 /nobreak >nul 2>&1
start http://localhost:8000/index.html