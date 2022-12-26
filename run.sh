if grep -qi microsoft /proc/version; then
  eval "env/Scripts/python.exe main.py"
else
  eval "env/bin/python3 main.py";
fi