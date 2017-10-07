#!/bin/ksh

set -v

rm -rf onymos_components/onymos-plugin-digime
ionic platform rm android
ionic plugin rm onymos-plugin-digime
ionic plugin add cordova-plugin-device

cp -R ~/onymos/dev/products/onymos_src/pre-release/onymos-plugin-digime onymos_components/

ionic platform add android
ionic build android
ionic run android

echo -ne '\007'
echo -ne '\007'
echo -ne '\007'
