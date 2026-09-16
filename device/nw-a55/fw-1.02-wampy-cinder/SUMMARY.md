# Device map — NW-A55, firmware 1.02, with Wampy and Cinder

| | |
|---|---|
| Model (property) | NW-A50Series |
| Board | BBDMP5_linux |
| SoC (cpuinfo Hardware) | MT8590 |
| CPU cores | 2 |
| RAM | 456 MB |
| Kernel | Linux version 3.10.26 (slave@azslave5q) (gcc version 4.8 (GCC) ) #1 SMP PREEMPT Wed Jul 31 16:22:50 JST 2019 |
| Android base (props) | 5.0 (SDK 21) |

## Partitions (`/proc/dumchar_info`)

```
Part_Name	Size	StartAddr	Type	MapTo
preloader    0x0000000000040000   0x0000000000000000   2   /dev/misc-sd
mbr          0x0000000000080000   0x0000000000000000   2   /dev/block/mmcblk0
ebr1         0x0000000000080000   0x0000000000080000   2   /dev/block/mmcblk0p1
ebr2         0x0000000000080000   0x0000000000100000   2   /dev/block/mmcblk0
ebr3         0x0000000000080000   0x0000000000180000   2   /dev/block/mmcblk0
ebr4         0x0000000000080000   0x0000000000200000   2   /dev/block/mmcblk0
ebr5         0x0000000000080000   0x0000000000280000   2   /dev/block/mmcblk0
ebr6         0x0000000000080000   0x0000000000300000   2   /dev/block/mmcblk0
ebr7         0x0000000000080000   0x0000000000380000   2   /dev/block/mmcblk0
ebr8         0x0000000000080000   0x0000000000400000   2   /dev/block/mmcblk0
ebr9         0x0000000000080000   0x0000000000480000   2   /dev/block/mmcblk0
pro_info     0x0000000000300000   0x0000000000500000   2   /dev/block/mmcblk0p2
nvram        0x0000000000500000   0x0000000000800000   2   /dev/block/mmcblk0p3
protect_f    0x0000000000a00000   0x0000000000d00000   2   /dev/block/mmcblk0p4
protect_s    0x0000000000a00000   0x0000000001700000   2   /dev/block/mmcblk0p5
seccfg       0x0000000000020000   0x0000000002100000   2   /dev/block/mmcblk0p6
uboot        0x0000000000060000   0x0000000002120000   2   /dev/block/mmcblk0p7
bootimg      0x0000000001000000   0x0000000002180000   2   /dev/block/mmcblk0p8
recovery     0x0000000001000000   0x0000000003180000   2   /dev/block/mmcblk0p9
sec_ro       0x0000000000600000   0x0000000004180000   2   /dev/block/mmcblk0p10
misc         0x0000000000080000   0x0000000004780000   2   /dev/block/mmcblk0p11
logo         0x0000000000300000   0x0000000004800000   2   /dev/block/mmcblk0p12
expdb        0x0000000000a00000   0x0000000004b00000   2   /dev/block/mmcblk0p13
tee1         0x0000000000500000   0x0000000005500000   2   /dev/block/mmcblk0p14
tee2         0x0000000000500000   0x0000000005a00000   2   /dev/block/mmcblk0p15
kb           0x0000000000100000   0x0000000005f00000   2   /dev/block/mmcblk0p16
dkb          0x0000000000100000   0x0000000006000000   2   /dev/block/mmcblk0p17
xhrome       0x0000000000100000   0x0000000006100000   2   /dev/block/mmcblk0p18
android      0x0000000032000000   0x0000000006200000   2   /dev/block/mmcblk0p19
cache        0x0000000001c00000   0x0000000038200000   2   /dev/block/mmcblk0p20
cm4          0x0000000000080000   0x0000000039e00000   2   /dev/block/mmcblk0p21
nvp          0x0000000000f00000   0x0000000039e80000   2   /dev/block/mmcblk0p22
var          0x0000000006e00000   0x000000003ad80000   2   /dev/block/mmcblk0p23
db           0x0000000006400000   0x0000000041b80000   2   /dev/block/mmcblk0p24
option1      0x0000000000800000   0x0000000047f80000   2   /dev/block/mmcblk0p25
option2      0x0000000008000000   0x0000000048780000   2   /dev/block/mmcblk0p26
option3      0x0000000040000000   0x0000000050780000   2   /dev/block/mmcblk0p27
usrdata      0x0000000002800000   0x0000000090780000   2   /dev/block/mmcblk0p28
contents     0x0000000dfc880000   0x0000000092f80000   2   /dev/block/mmcblk0p29
bmtpool      0x0000000000000000   0x0000000000000000   2   /dev/block/mmcblk0p30
Part_Name:Partition name you should open;
Size:size of partition
StartAddr:Start Address of partition;
Type:Type of partition(MTD=1,EMMC=2)
MapTo:actual device you operate
```

## Mounts

| device | mount point | fs | options |
|---|---|---|---|
| `rootfs` | `/` | rootfs | `rw` |
| `tmpfs` | `/dev` | tmpfs | `rw,relatime,size=4096k,mode=755` |
| `tmpfs` | `/tmp` | tmpfs | `rw,relatime,size=32768k` |
| `tmpfs` | `/dev/shm` | tmpfs | `rw,relatime,size=65536k` |
| `/emmc@android` | `/system` | ext4 | `ro,noatime,data=ordered` |
| `/emmc@cache` | `/cache` | ext4 | `rw,nodev,noexec,noatime,discard,data=ordered` |
| `/emmc@usrdata` | `/data` | ext4 | `rw,nodev,noexec,noatime,discard,data=ordered` |
| `/emmc@var` | `/var` | ext4 | `rw,nodev,noexec,noatime,discard,data=ordered` |
| `/emmc@db` | `/db` | ext4 | `rw,nodev,noexec,noatime,discard,data=ordered` |
| `/emmc@option1` | `/opt1` | ext4 | `ro,nodev,noexec,noatime,data=ordered` |
| `/emmc@option2` | `/opt2` | ext4 | `ro,nodev,noexec,noatime,data=ordered` |
| `/emmc@option3` | `/opt3` | ext4 | `ro,nodev,noexec,noatime,data=ordered` |
| `/emmc@contents` | `/contents` | vfat | `rw,noexec,noatime,fmask=0000,dmask=0000,allow_utime=0022,codepage=437,iocharset=iso8859-1,shortname=mixed,utf8,errors=remount-ro,discard` |
| `/dev/block/mmcblk1p1` | `/contents_ext` | vfat | `rw,noexec,noatime,fmask=0000,dmask=0000,allow_utime=0022,codepage=437,iocharset=iso8859-1,shortname=mixed,utf8,errors=remount-ro` |

## Processes that host Sony services

Every `hagodaemon` below is one `service` line of the booted init scripts; the library list is what the process actually MAPPED, and the sockets are the unix sockets it holds. uid 1005 appears only on the `logwrapper` parents, which are left out.

### `/system/vendor/sony/bin/hagodaemon AudioAnalyzerService userAndGroup=system,system sub_sm`
pid 321, uid 100

Sony libraries: `libAudioAnalyzerService.so`, `libConfigurationService.so`, `libConnMgrService.so`, `libDmpConfig.so`, `libDmpFeature.so`, `libFuncArchUtils.so`, `libFuncMgrService.so`, `libNcAsmService.so`, `libPathMgrService.so`, `libPowerMgrServiceClient.so`, `libSoundService.so`, `libSoundServiceFw.so`, `libVolumeService.so`, `libaudiohal-a2dpsnksingletrack.so`, `libaudiohal-adleralsa.so`, `libaudiohal-analyzer.so`, `libaudiohal-dualtrackmixalsa.so`, `libaudiohal-genericalsa.so`, `libaudiohal-listener.so`, `libaudiohal-uacalsasingletrack.so`, `libpstcore.so`

### `/system/vendor/sony/bin/hagodaemon AudioInPlayerService TunerPlayerService userAndGroup=system,system nice=-10 sub_sm`
pid 326, uid 100

Sony libraries: `libAudioInPlayerService.so`, `libConfigurationService.so`, `libFuncArchUtils.so`, `libSoundService.so`, `libTunerPlayerService.so`, `libpstcore.so`

### `/system/vendor/sony/bin/hagodaemon BtCommonService BtTransmitterService BtBleCommonService BtBleRemoteService BtPlayerService capabilities=23 sub_sm`
pid 333, uid 100

Sony libraries: `libBleFunctionHandler.so`, `libBtBleCommonService.so`, `libBtBleRemoteService.so`, `libBtCommonService.so`, `libBtCompIf.so`, `libBtMw.so`, `libBtPlayerService.so`, `libBtTransmitterService.so`, `libConfigurationService.so`, `libFuncArchUtils.so`, `libKeyService.so`, `libLogupStub.so`, `libSoundService.so`, `libpstcore.so`

Sockets: `/tmp/bt.app.gap`, `/tmp/bt.ext.adp`, `/tmp/bt.ext.adp.a2dp`, `/tmp/bt.ext.adp.a2dp.data`, `/tmp/bt.ext.adp.a2dp.data.src`, `/tmp/bt.ext.adp.avrcp`, `/tmp/bt.ext.adp.gattc`, `/tmp/bt.ext.adp.gatts`, `/tmp/bt.ext.adp.hid`, `/tmp/bt.ext.adp.l2cap`, `/tmp/bt.ext.adp.spp`, `@pst::services::bttransmitterservice`

### `/system/vendor/sony/bin/hagodaemon ConnMgrServiceFw userAndGroup=system,system sub_sm`
pid 318, uid 100

Sony libraries: `libBtCompIf.so`, `libBtMw.so`, `libBtTransmitterService.so`, `libConfigurationService.so`, `libConnMgrService.so`, `libConnMgrServiceFw.so`, `libDmpConfig.so`, `libDmpFeature.so`, `libFuncArchUtils.so`, `libFuncMgrService.so`, `libFuncMgrServiceFw.so`, `libLogupStub.so`, `libPathMgrService.so`, `libSoundService.so`, `libUsbDeviceAudioPlayerService.so`, `libUsbDeviceConnectionService.so`, `libUsbHostConnectionService.so`, `libUsbMgrService.so`, `libWMPortService.so`, `libWiredHpService.so`, `libWiredHpServiceFw.so`, `libpstcore.so`

### `/system/vendor/sony/bin/hagodaemon EventRouter sub_sm`
pid 323, uid 100

Sony libraries: `libEventRouter.so`, `libpstcore.so`

### `/system/vendor/sony/bin/hagodaemon FuncMgrServiceFw userAndGroup=system,system sub_sm`
pid 320, uid 100

Sony libraries: `libConfigurationService.so`, `libConnMgrService.so`, `libConnMgrServiceFw.so`, `libDmpConfig.so`, `libDmpFeature.so`, `libFuncArchUtils.so`, `libFuncMgrService.so`, `libFuncMgrServiceFw.so`, `libPathMgrService.so`, `libPathMgrServiceFw.so`, `libUsbMgrService.so`, `libUsbMgrServiceFw.so`, `libWiredHpService.so`, `libpstcore.so`

### `/system/vendor/sony/bin/hagodaemon MediaStoreService PlayerService userAndGroup=system,system capabilities=13 sub_sm`
pid 310, uid 100; LD_PRELOAD=/system/vendor/unknown321/lib/libdmp_feature.so

Sony libraries: `libConfigurationService.so`, `libConnMgrService.so`, `libDmpConfig.so`, `libDmpFeature.so`, `libFuncArchUtils.so`, `libMediaStoreService.so`, `libNcAsmService.so`, `libPathMgrService.so`, `libPlayerService.so`, `libPowerMgrServiceClient.so`, `libSoundService.so`, `libSoundServiceFw.so`, `libVolumeService.so`, `libaudiohal-a2dpsnksingletrack.so`, `libaudiohal-adleralsa.so`, `libaudiohal-analyzer.so`, `libaudiohal-dualtrackmixalsa.so`, `libaudiohal-genericalsa.so`, `libaudiohal-listener.so`, `libaudiohal-uacalsasingletrack.so`, `libcnpysort.so`, `libcrypto.so.1.1`, `libcurl.so.4`, `libpstcore.so`, `libssl.so.1.1`

### `/system/vendor/sony/bin/hagodaemon MemmonService sub_sm`
pid 329, uid 0

Sony libraries: `libMemmonService.so`, `libpstcore.so`

### `/system/vendor/sony/bin/hagodaemon NcServiceFw userAndGroup=system,system capabilities=12 sub_sm`
pid 327, uid 100

Sony libraries: `libConfigurationService.so`, `libConnMgrService.so`, `libConnMgrServiceFw.so`, `libDmpConfig.so`, `libDmpFeature.so`, `libFuncArchUtils.so`, `libFuncMgrService.so`, `libFuncMgrServiceFw.so`, `libNcServiceFw.so`, `libPathMgrService.so`, `libPathMgrServiceFw.so`, `libUsbMgrService.so`, `libWiredHpService.so`, `libpstcore.so`

### `/system/vendor/sony/bin/hagodaemon NfcService sub_sm`
pid 331, uid 100

Sony libraries: `libNfcService.so`, `libpstcore.so`

### `/system/vendor/sony/bin/hagodaemon OneTrackPlayerService userAndGroup=system,system sub_sm`
pid 311, uid 100

Sony libraries: `libConfigurationService.so`, `libConnMgrService.so`, `libDmpConfig.so`, `libDmpFeature.so`, `libFuncArchUtils.so`, `libNcAsmService.so`, `libOneTrackPlayerService.so`, `libPathMgrService.so`, `libPowerMgrServiceClient.so`, `libSoundService.so`, `libSoundServiceFw.so`, `libVolumeService.so`, `libaudiohal-a2dpsnksingletrack.so`, `libaudiohal-adleralsa.so`, `libaudiohal-analyzer.so`, `libaudiohal-dualtrackmixalsa.so`, `libaudiohal-genericalsa.so`, `libaudiohal-listener.so`, `libaudiohal-uacalsasingletrack.so`, `libcrypto.so.1.1`, `libcurl.so.4`, `libpstcore.so`, `libssl.so.1.1`

### `/system/vendor/sony/bin/hagodaemon PathMgrServiceFw userAndGroup=system,system sub_sm`
pid 313, uid 100

Sony libraries: `libConfigurationService.so`, `libConnMgrService.so`, `libConnMgrServiceFw.so`, `libFuncArchUtils.so`, `libFuncMgrService.so`, `libPathMgrServiceFw.so`, `libTunerPlayerService.so`, `libVolumeGlue.so`, `libWiredHpService.so`, `libpstcore.so`

### `/system/vendor/sony/bin/hagodaemon PowerMgrServiceFw userAndGroup=system,system capabilities=12 sub_sm`
pid 312, uid 100

Sony libraries: `libConfigurationService.so`, `libFuncArchUtils.so`, `libPowerMgrServiceFw.so`, `libPowerService.so`, `libpstcore.so`

### `/system/vendor/sony/bin/hagodaemon PowerService sub_sm`
pid 315, uid 0

Sony libraries: `libConfigurationService.so`, `libFuncArchUtils.so`, `libPowerService.so`, `libpstcore.so`

### `/system/vendor/sony/bin/hagodaemon RecorderService userAndGroup=system,system sub_sm`
pid 322, uid 100

Sony libraries: `libRecorderService.so`, `libcrypto.so.1.1`, `libcurl.so.4`, `libpstcore.so`, `libssl.so.1.1`

### `/system/vendor/sony/bin/hagodaemon RemoteCmdInjCtrlDaemon userAndGroup=system,system sub_sm`
pid 302, uid 100

Sony libraries: `libBtCompIf.so`, `libBtMw.so`, `libBtTransmitterService.so`, `libConfigurationService.so`, `libConnMgrService.so`, `libFuncArchUtils.so`, `libLogupStub.so`, `libPathMgrService.so`, `libPathMgrServiceFw.so`, `libRemoteCmdInjCtrlDaemon.so`, `libWMPortService.so`, `libpstcore.so`

### `/system/vendor/sony/bin/hagodaemon SoundServiceFw capabilities=23 userAndGroup=system,system nice=-15 sub_sm`
pid 330, uid 100; LD_PRELOAD=/system/vendor/unknown321/lib/libsound_service_fw.so

Sony libraries: `libBtCompIf.so`, `libBtMw.so`, `libBtTransmitterService.so`, `libConfigurationService.so`, `libConnMgrService.so`, `libDmpConfig.so`, `libDmpFeature.so`, `libFuncArchUtils.so`, `libFuncMgrService.so`, `libLogupStub.so`, `libNcAsmService.so`, `libNcServiceFw.so`, `libPathMgrService.so`, `libPathMgrServiceFw.so`, `libPowerMgrServiceClient.so`, `libPowerMgrServiceFw.so`, `libSoundServiceFw.so`, `libVolumeService.so`, `libVolumeServiceFw.so`, `libaudiohal-a2dpsnksingletrack.so`, `libaudiohal-adleralsa.so`, `libaudiohal-analyzer.so`, `libaudiohal-dualtrackmixalsa.so`, `libaudiohal-genericalsa.so`, `libaudiohal-listener.so`, `libaudiohal-uacalsasingletrack.so`, `libpstcore.so`

### `/system/vendor/sony/bin/hagodaemon StorageMgrServiceFw sub_sm`
pid 337, uid 0

Sony libraries: `libConfigurationService.so`, `libConnMgrService.so`, `libConnMgrServiceFw.so`, `libDmpConfig.so`, `libDmpFeature.so`, `libFuncArchUtils.so`, `libFuncMgrService.so`, `libInitialObject.so`, `libStorageMgrServiceFw.so`, `libWiredHpService.so`, `libpstcore.so`

### `/system/vendor/sony/bin/hagodaemon TimerService capabilities=1,3,25,35 userAndGroup=system,system sub_sm`
pid 303, uid 100

Sony libraries: `libConfigurationService.so`, `libTimerService.so`, `libpstcore.so`

### `/system/vendor/sony/bin/hagodaemon UpdateService sub_sm`
pid 317, uid 100

Sony libraries: `libConfigurationService.so`, `libFuncArchUtils.so`, `libLogupStub.so`, `libUpdateService.so`, `libUsbDeviceConnectionService.so`, `libcrypto.so.1.1`, `libpstcore.so`

### `/system/vendor/sony/bin/hagodaemon UsbHostConnectionService UsbDeviceConnectionService UsbDeviceAudioPlayerService userAndGroup=system,system capabilities=1,12 nice=-10 sub_sm`
pid 328, uid 100

Sony libraries: `libConnMgrService.so`, `libConnMgrServiceFw.so`, `libFuncArchUtils.so`, `libFuncMgrService.so`, `libLogupStub.so`, `libSoundService.so`, `libUsbDeviceAudioPlayerService.so`, `libUsbDeviceConnectionService.so`, `libUsbHostConnectionService.so`, `libWiredHpService.so`, `libpstcore.so`

### `/system/vendor/sony/bin/hagodaemon UsbMgrServiceFw userAndGroup=system,system capabilities=12 sub_sm`
pid 306, uid 100

Sony libraries: `libConfigurationService.so`, `libConnMgrService.so`, `libConnMgrServiceFw.so`, `libDmpConfig.so`, `libDmpFeature.so`, `libFuncArchUtils.so`, `libFuncMgrService.so`, `libUsbMgrServiceFw.so`, `libWiredHpService.so`, `libpstcore.so`

### `/system/vendor/sony/bin/hagodaemon VolumeGlue userAndGroup=system,system sub_sm`
pid 305, uid 100

Sony libraries: `libFuncArchUtils.so`, `libVolumeGlue.so`, `libpstcore.so`

### `/system/vendor/sony/bin/hagodaemon VolumeServiceFw userAndGroup=system,system sub_sm`
pid 304, uid 100

Sony libraries: `libBtCompIf.so`, `libBtMw.so`, `libBtTransmitterService.so`, `libConfigurationService.so`, `libConnMgrService.so`, `libConnMgrServiceFw.so`, `libDmpConfig.so`, `libDmpFeature.so`, `libFuncArchUtils.so`, `libFuncMgrService.so`, `libLogupStub.so`, `libPathMgrService.so`, `libPathMgrServiceFw.so`, `libVolumeGlue.so`, `libVolumeServiceFw.so`, `libWiredHpService.so`, `libpstcore.so`

### `/system/vendor/sony/bin/hagodaemon WMPortService KeyService ConfigurationService DisplayService userAndGroup=system,system capabilities=1,12 sub_sm`
pid 316, uid 100

Sony libraries: `libConfigurationService.so`, `libDisplayService.so`, `libKeyService.so`, `libWMPortService.so`, `libpstcore.so`

### `/system/vendor/sony/bin/hagodaemon WiredHpServiceFw userAndGroup=system,system capabilities=12 sub_sm`
pid 336, uid 100

Sony libraries: `libFuncArchUtils.so`, `libWiredHpServiceFw.so`, `libpstcore.so`

### `/system/vendor/sony/bin/hagodaemon appmgrservice sub_sm`
pid 314, uid 100

Sony libraries: `libappmgrservice.so`, `libpstcore.so`

### `/system/vendor/sony/bin/hagodaemon userAndGroup=system,system groups=log,chrome capabilities=5,22 daemonNum=28`
pid 324, uid 100

Sony libraries: `libpstcore.so`

### `/system/vendor/unknown321/bin/cinder-home`
pid 683, uid 100

Sony libraries: `libBtCommonService.so`, `libBtCompIf.so`, `libBtMw.so`, `libBtTransmitterService.so`, `libConfigurationService.so`, `libConnMgrService.so`, `libDisplayService.so`, `libDmpConfig.so`, `libDmpFeature.so`, `libEffectCtrlDmp.so`, `libFuncArchUtils.so`, `libInitialObject.so`, `libLogupStub.so`, `libMediaStoreService.so`, `libMediaStoreServiceClient.so`, `libNcAsmService.so`, `libNfcService.so`, `libPathMgrService.so`, `libPlayerService.so`, `libPlayerServiceClient.so`, `libPlayerServiceClientUtil.so`, `libPowerMgrServiceClient.so`, `libPowerMgrServiceFw.so`, `libSoundService.so`, `libSoundServiceFw.so`, `libStorageMgrServiceFw.so`, `libUsbDeviceAudioPlayerService.so`, `libVolumeService.so`, `libappmgrservice.so`, `libaudiohal-a2dpsnksingletrack.so`, `libaudiohal-adleralsa.so`, `libaudiohal-analyzer.so`, `libaudiohal-dualtrackmixalsa.so`, `libaudiohal-genericalsa.so`, `libaudiohal-listener.so`, `libaudiohal-uacalsasingletrack.so`, `libcnpysort.so`, `libcrypto.so.1.1`, `libcurl.so.4`, `libeaselcore.so`, `libeaselcui.so`, `libjson.so`, `libpstcore.so`, `libssl.so.1.1`

### `/system/vendor/unknown321/bin/pstserver 8`
pid 325, uid 0

Sony libraries: `libAudioAnalyzerServiceClient.so`, `libConfigurationService.so`, `libDmpConfig.so`, `libDmpFeature.so`, `libEffectCtrlDmp.so`, `libPlayerServiceClient.so`, `libTunerPlayerService.so`, `libpstcore.so`

### Init services (booted ramdisk)

| service | command |
|---|---|
| `66xx_launcherA` | `/system/bin/6620_launcherA -p /system/etc/firmware/` |
| `66xx_launcherC` | `/system/bin/6620_launcherC -m 4 -p /system/etc/firmware/` |
| `adbd` | `/sbin/adbd --root_seclabel=u:r:su:s0` |
| `autokd` | `/system/bin/autokd` |
| `bdpprog_shell` | `/bin/bdpwrapper /bin/sh /usr/bin/bdpprog.sh` |
| `boot_complete` | `/bin/sh /sbin/boot_complete.sh` |
| `bootanimation` | `/bin/logwrapper /system/xbin/icx_bootanimation` |
| `cast_installer` | `/bin/logwrapper /bin/bash /usr/bin/cast_installer.sh` |
| `cast_receiver` | `/bin/logwrapper /chrome/cast_cli start cast async \` |
| `console` | `/bin/sh -I` |
| `dhcpcd` | `/bin/dhcpcd wlan0 -B --noarp -h audiocast` |
| `dpfd` | `system/bin/dpfd` |
| `ffu` | `/system/bin/ffu` |
| `fuse_usbotg` | `/system/bin/sdcard -u 1023 -g 1023 -w 1023 -d /mnt/media_rw/usbotg /storage/usbotg` |
| `hagoromo1` | `/bin/logwrapper /system/vendor/sony/bin/hagodaemon userAndGroup=system,system groups=log,chrome capabilities=5,22 daemonNum=28` |
| `hagoromo10` | `/bin/logwrapper /system/vendor/sony/bin/hagodaemon OneTrackPlayerService userAndGroup=system,system sub_sm` |
| `hagoromo11` | `/bin/logwrapper /system/vendor/sony/bin/hagodaemon SoundServiceFw capabilities=23 userAndGroup=system,system nice=-15 sub_sm` |
| `hagoromo12` | `/bin/logwrapper /system/vendor/sony/bin/hagodaemon NcServiceFw userAndGroup=system,system capabilities=12 sub_sm` |
| `hagoromo13` | `/bin/logwrapper /system/vendor/sony/bin/hagodaemon VolumeServiceFw userAndGroup=system,system sub_sm` |
| `hagoromo14` | `/bin/logwrapper /system/vendor/sony/bin/hagodaemon VolumeGlue userAndGroup=system,system sub_sm` |
| `hagoromo15` | `/bin/logwrapper /system/vendor/sony/bin/hagodaemon RecorderService userAndGroup=system,system sub_sm` |
| `hagoromo16` | `/bin/logwrapper /system/vendor/sony/bin/hagodaemon AudioAnalyzerService userAndGroup=system,system sub_sm` |
| `hagoromo17` | `/bin/logwrapper /system/vendor/sony/bin/hagodaemon ConnMgrServiceFw userAndGroup=system,system sub_sm` |
| `hagoromo18` | `/bin/logwrapper /system/vendor/sony/bin/hagodaemon FuncMgrServiceFw userAndGroup=system,system sub_sm` |
| `hagoromo19` | `/bin/logwrapper /system/vendor/sony/bin/hagodaemon PathMgrServiceFw userAndGroup=system,system sub_sm` |
| `hagoromo2` | `/bin/logwrapper /system/vendor/sony/bin/hagodaemon appmgrservice sub_sm` |
| `hagoromo20` | `/bin/logwrapper /system/vendor/sony/bin/hagodaemon PowerMgrServiceFw userAndGroup=system,system capabilities=12 sub_sm` |
| `hagoromo21` | `/bin/logwrapper /system/vendor/sony/bin/hagodaemon RemoteCmdInjCtrlDaemon userAndGroup=system,system sub_sm` |
| `hagoromo22` | `/bin/logwrapper /system/vendor/sony/bin/hagodaemon UsbMgrServiceFw userAndGroup=system,system capabilities=12 sub_sm` |
| `hagoromo23` | `/bin/logwrapper /system/vendor/sony/bin/hagodaemon StorageMgrServiceFw sub_sm` |
| `hagoromo24` | `/bin/logwrapper /system/vendor/sony/bin/hagodaemon WiredHpServiceFw userAndGroup=system,system capabilities=12 sub_sm` |
| `hagoromo25` | `/bin/logwrapper /system/vendor/sony/bin/hagodaemon NfcService sub_sm` |
| `hagoromo26` | `/bin/logwrapper /system/vendor/sony/bin/hagodaemon MemmonService sub_sm` |
| `hagoromo27` | `/bin/logwrapper /system/vendor/sony/bin/hagodaemon BtCommonService BtTransmitterService BtBleCommonService BtBleRemoteService BtPlayerService capabilities=23 sub_sm` |
| `hagoromo28` | `/bin/logwrapper /system/vendor/sony/bin/hagodaemon AudioInPlayerService TunerPlayerService userAndGroup=system,system nice=-10 sub_sm` |
| `hagoromo3` | `/bin/logwrapper /system/vendor/sony/bin/hagodaemon PowerService sub_sm` |
| `hagoromo4` | `/bin/logwrapper /system/vendor/sony/bin/hagodaemon EventRouter sub_sm` |
| `hagoromo5` | `/bin/logwrapper /system/vendor/sony/bin/hagodaemon TimerService capabilities=1,3,25,35 userAndGroup=system,system sub_sm` |
| `hagoromo6` | `/bin/logwrapper /system/vendor/sony/bin/hagodaemon WMPortService KeyService ConfigurationService DisplayService userAndGroup=system,system capabilities=1,12 sub_sm` |
| `hagoromo7` | `/bin/logwrapper /system/vendor/sony/bin/hagodaemon UpdateService sub_sm` |
| `hagoromo8` | `/bin/logwrapper /system/vendor/sony/bin/hagodaemon UsbHostConnectionService UsbDeviceConnectionService UsbDeviceAudioPlayerService userAndGroup=system,system capabilities=1,12 nice=-10 sub_sm` |
| `hagoromo9` | `/bin/logwrapper /system/vendor/sony/bin/hagodaemon MediaStoreService PlayerService userAndGroup=system,system capabilities=13 sub_sm` |
| `icx_console` | `/system/bin/icx_console` |
| `icx_diag` | `/system/bin/dodiag.sh` |
| `icx_hdump_log` | `/system/xbin/icx_hdump_log -c` |
| `icx_syslog` | `/system/xbin/icx_syslog -n 32 -l 6 -d "/emmc@var"` |
| `imdb_shell` | `/usr/imdb/etc/init.d/imdbdog.sh` |
| `load_sony_driver` | `/system/bin/load_sony_driver` |
| `mount_msc1` | `/system/bin/mount_partition contents` |
| `mtkbt` | `/bin/mtkbt > /tmp/mtkbt.log` |
| `net_mgr` | `/bin/net_mgr` |
| `nvram_daemon` | `/system/bin/nvram_daemon` |
| `pstserver` | `/bin/logwrapper /system/vendor/unknown321/bin/pstserver 8` |
| `scrobbler` | `/bin/logwrapper /system/vendor/unknown321/bin/scrobbler` |
| `set_iserial` | `/system/bin/set_iserial.sh` |
| `sntpd` | `/bin/sntpd` |
| `sshd` | `/usr/bin/sshd -G -r /etc/rsa_host_key -F` |
| `stp_dump` | `/system/bin/stp_dump3` |
| `ueventd` | `/sbin/ueventd` |
| `unmount_msc1` | `/system/bin/umount /contents` |
| `wampy` | `/bin/logwrapper /system/vendor/unknown321/bin/wampy` |
| `watchdog` | `/bin/watchdog -F` |
| `wmtLoader` | `/system/bin/logwrapper /system/bin/wmt_loader` |
| `wpa_supplicant` | `/system/bin/logwrapper /system/bin/wpa_supplicant \` |

## ALSA PCM devices

```
00-00: cxd3778gf-hires-out DAI_CXD3778GF_DAC-0 :  : playback 1
00-01: cxd3778gf-standard DAI_CXD3778GF_STD-1 :  : playback 1 : capture 1
00-02: dsdenc DAI_CXD3778GF_ICX-2 :  : playback 1
00-03: cxd3778gf-dsd-out DAI_CXD3778GF_ICX-3 :  : playback 1
00-04: cxd3778gf-icx-lowpower DAI_CXD3778GF_ICX-4 :  : playback 1
00-05: cxd3778gf-icx-lowpower_test DAI_CXD3778GF_ICX-5 :  : playback 1
```

## Input devices

| node | name |
|---|---|
| `/dev/input/event8` | AVRCP |
| `/dev/input/event7` | BLEREMOTE |
| `/dev/input/event6` | BTTRAN |
| `/dev/input/event5` | WMPORT |
| `/dev/input/event4` | icx_key |
| `/dev/input/event0` | mtk-kpd |
| `/dev/input/event3` | m_batch_input |
| `/dev/input/event2` | hwmdata |
| `/dev/input/event1` | himax-hx8526-icx |

## I2C devices (bus-address → driver name)

| device | name |
|---|---|
| `0-0010` | mkl17z32vda4_fw |
| `0-004c` | pcm1795 |
| `0-004e` | CODEC_CXD3778GF |
| `0-007f` | kd_camera_hw |
| `1-0048` | himax-hx8526-icx |
| `1-004e` | CODEC_CXD3778GF_EXT |
| `1-0050` | dummy_eeprom |
| `1-0055` | dummy_cam_cal |
| `2-0010` | Si4708icx |
| `2-0028` | cxd224x-i2c |
| `2-0050` | mt_m24c16 |
| `2-0051` | dummy |
| `2-0052` | dummy |
| `2-0053` | dummy |
| `2-0054` | dummy |
| `2-0055` | dummy |
| `2-0056` | dummy |
| `2-0057` | dummy |
| `2-006b` | bq24262_wmport |
| `i2c-0` | mt-i2c |
| `i2c-1` | mt-i2c |
| `i2c-2` | mt-i2c |

## Loaded kernel modules

`icx_usbconn`, `icx_carddet`, `cxd3778gf_dnc_core`, `wm_key`, `mtk_stp_bt_soc`, `mtk_stp_wmt_soc`, `mtk_wmt_detect`, `radio_si4708icx`, `icx_nvp_emmc`

## Misc character devices (major:minor)

`RT_Monitor` 10:50, `aed0` 10:52, `aed1` 10:51, `alarm` 10:54, `android_adb` 10:26, `ashmem` 10:60, `asrc1` 10:44, `asrc2` 10:43, `asrc3` 10:42, `asrc4` 10:41, `asrc5` 10:40, `audacc` 10:38, `audrtc` 10:39, `binder` 10:61, `cpu_dma_latency` 10:29, `cxd224x-i2c` 10:32, `device-mapper` 10:236, `ebc` 10:47, `fuse` 10:229, `hid-keyboard` 10:33, `hwmsensor` 10:31, `icx_usbscsi` 10:0, `ion` 10:62, `log_events` 10:58, `log_main` 10:59, `log_metrics` 10:55, `log_radio` 10:57, `log_system` 10:56, `logksystem` 10:48, `loop-control` 10:237, `m_batch_misc` 10:30, `mali` 10:63, `misc-sd` 10:46, `mt_otg_test` 10:45, `mtfreqhopping` 10:35, `mtgpio` 10:36, `mtk-kpd` 10:34, `mtp_usb` 10:25, `network_latency` 10:28, `network_throughput` 10:27, `psaux` 10:1, `snapshot` 10:231, `sw_sync` 10:53, `tun` 10:200, `uhid` 10:239, `uinput` 10:223, `usb_accessory` 10:24, `xLog` 10:49, `xt_qtaguid` 10:37
