:: Copyright (c) 2021 NVIDIA CORPORATION & AFFILIATES
:: This script requires a valid python installation in the user's path

start py -m http.server 8000 
py -c "import socket,time,sys;t=time.time()+30;exec('while time.time()<t:\n try:\n  s=socket.socket();s.settimeout(0.1);s.connect((\"127.0.0.1\",8000));s.close();sys.exit(0)\n except OSError:\n  time.sleep(0.1)\n');sys.exit(1)"
if errorlevel 1 exit /b 1
start http://localhost:8000/index.html