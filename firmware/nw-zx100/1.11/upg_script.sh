#!/bin/sh

NVP_FNI="0x00000000"
NVP_SID="0x00000000"
NVP_MLK="0x41544b20"

##################################
echo "------ INIT SEQUENCE ------"

ROOTFS_TMP_DIR=/tmp/rootfs

source /install_script/constant.txt

_UPDATE_FN_=`nvpstr ufn`
if [ "$?" != 0 ]; then
	echo "nvpstr(ufn) error"
	fwfb /root/fwup_err.rgb
	exit 1
fi


####################################################
echo "------ FORMAT AND MOUNT ROOT PARTITION ------"

if [ -e /usr/local/bin/icx_mkfs.ext4 ]; then
    MKFS_CMD="/usr/local/bin/icx_mkfs.ext4"
else
    MKFS_CMD="mkfs.ext3"
fi
echo "MKFS_CMD=$MKFS_CMD"

$MKFS_CMD $COMMON_ROOTFS_PARTITION
if [ "$?" != 0 ]; then
	echo "mkfs(root) error"
	fwfb /root/fwup_err.rgb
	exit 1
fi

mkdir $ROOTFS_TMP_DIR
if [ "$?" != 0 ]; then
	echo "mkdir(tmp) error"
	fwfb /root/fwup_err.rgb
	exit 1
fi

if [ -e /usr/local/bin/icx_mount.ext4 ]; then
    MOUNT_CMD="/usr/local/bin/icx_mount.ext4"
else
    MOUNT_CMD="mount -t ext3"
fi
echo "MOUNT_CMD=$MOUNT_CMD"

$MOUNT_CMD $COMMON_ROOTFS_PARTITION $ROOTFS_TMP_DIR
if [ "$?" != 0 ]; then
	echo "mount(root) error"
	fwfb /root/fwup_err.rgb
	exit 1
fi

#################################################
echo "------ WRITE COMMON KERNEL & ROOTFS ------"

fwpup -f /contents/$_UPDATE_FN_.UPG -k 1 -r 2 | tar -C $ROOTFS_TMP_DIR -xvzf -
if [ "$?" != 0 ]; then
	echo "fwpup error"
	fwfb /root/fwup_err.rgb
	exit 1
fi

###########################################
echo "------ UNMOUNT ROOT PARTITION ------"

sync
if [ "$?" != 0 ]; then
	echo "sync error"
	fwfb /root/fwup_err.rgb
	exit 1
fi

umount $ROOTFS_TMP_DIR
if [ "$?" != 0 ]; then
	echo "umount(mnt) error"
	fwfb /root/fwup_err.rgb
	exit 1
fi

###############################
echo "------ UPDATE NVP ------"

/usr/local/bin/nvpflag -x fni $NVP_FNI
if [ "$?" != 0 ]; then
	echo "nvpflag fni $NVP_FNI error"
	exit 1
fi

/usr/local/bin/nvpflag -x sid $NVP_SID
if [ "$?" != 0 ]; then
	echo "nvpflag sid $NVP_SID error"
	exit 1
fi

/usr/local/bin/nvpflag -x mlk $NVP_MLK
if [ "$?" != 0 ]; then
	echo "nvpflag mlk $NVP_MLK error"
	exit 1
fi

###########################################
echo "------ UPDATED!! ------"

exit 0
