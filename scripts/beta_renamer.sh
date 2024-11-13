#/bin/sh

if grep -q "beta" <<< "$1"; then
    sed -i "" 's/"PyES Beta"/"PyES Beta"/g; s/"PyES"/"PyES Beta"/g' src/build/settings/base.json
else
    sed -i "" 's/"PyES Beta"/"PyES"/g; s/"PyES"/"PyES"/g' src/build/settings/base.json
fi