
# pub global bin
export PUB_GLOBAL_BIN_DIR="/c/Users/cai/AppData/Local/Pub/Cache/bin"
export PATH="$PUB_GLOBAL_BIN_DIR:$PATH"
# convert.bat to no bat exec
for file in /c/Users/cai/AppData/Local/Pub/Cache/bin/*.bat; do
  __cmd="$(basename "$file" .bat)"
  alias "$__cmd"="$__cmd.bat"
done
