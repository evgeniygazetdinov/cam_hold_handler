if grep -qi microsoft /proc/version; then
  eval "env/Scripts/python.exe tornado_proto.py"
else
  eval "env/bin/python3 tornado_proto.py";
fi
if [[ $1 -eq 'first_run' ]] ; then
  echo 'download image';
  eval "docker run --name postgres_blog -p 45455:5432 -e POSTGRES_USER=blog -e POSTGRES_PASSWORD=blog -e POSTGRES_DB=blog -d postgres"
fi
if [[ $1 -eq '666' ]] ; then
  echo "run already downloaded image";
  eval "docker start postgres_blog";
fi;