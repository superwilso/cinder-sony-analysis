#!/bin/bash
# W1/stock UI capture helper. Screen coords are 480x800; panel raw is 960x1600 (2x).
SP="$(cd "$(dirname "$0")" && pwd)"
EV=/dev/input/event1
tap() { # tap X Y  (screen coords)
  local rx=$(( $1 * 2 )) ry=$(( $2 * 2 ))
  adb shell "sendevent $EV 1 330 1; sendevent $EV 3 48 40; sendevent $EV 3 50 40; sendevent $EV 3 53 $rx; sendevent $EV 3 54 $ry; sendevent $EV 0 2 0; sendevent $EV 0 0 0" >/dev/null 2>&1
  adb shell "sendevent $EV 3 48 0; sendevent $EV 0 2 0; sendevent $EV 1 330 0; sendevent $EV 0 0 0" >/dev/null 2>&1
}
swipe() { # swipe X0 Y0 X1 Y1 [steps]
  local x0=$(($1*2)) y0=$(($2*2)) x1=$(($3*2)) y1=$(($4*2)) n=${5:-12} i
  local cmd="sendevent $EV 1 330 1; sendevent $EV 3 48 40; sendevent $EV 3 50 40; sendevent $EV 3 53 $x0; sendevent $EV 3 54 $y0; sendevent $EV 0 2 0; sendevent $EV 0 0 0;"
  for ((i=1;i<=n;i++)); do
    cmd+=" sendevent $EV 3 48 40; sendevent $EV 3 53 $(( x0 + (x1-x0)*i/n )); sendevent $EV 3 54 $(( y0 + (y1-y0)*i/n )); sendevent $EV 0 2 0; sendevent $EV 0 0 0;"
  done
  cmd+=" sendevent $EV 3 48 0; sendevent $EV 0 2 0; sendevent $EV 1 330 0; sendevent $EV 0 0 0"
  adb shell "$cmd" >/dev/null 2>&1
}
key() { # key CODE  (icx_key event4: e.g. 115 volup 114 voldn)
  adb shell "sendevent /dev/input/event4 1 $1 1; sendevent /dev/input/event4 0 0 0; sendevent /dev/input/event4 1 $1 0; sendevent /dev/input/event4 0 0 0" >/dev/null 2>&1
}
cap() { # cap NAME
  local n=${1:-shot}
  adb shell 'dd if=/dev/graphics/fb0 of=/tmp/fb.raw bs=1024 count=1500' >/dev/null 2>&1
  adb pull /tmp/fb.raw "$SP/shots/$n.raw" >/dev/null 2>&1
  python3 - "$SP/shots/$n" <<'PY'
import sys
from PIL import Image
base=sys.argv[1]
raw=open(base+'.raw','rb').read()
w,h=480,800
img=Image.frombytes('RGBA',(w,h),raw[:w*h*4])
b,g,r,a=img.split()
Image.merge('RGB',(r,g,b)).save(base+'.png')
PY
  rm -f "$SP/shots/$n.raw"
  echo "$SP/shots/$n.png"
}
"$@"
