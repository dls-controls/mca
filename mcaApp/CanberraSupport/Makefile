TOP=../..
include $(TOP)/configure/CONFIG
#----------------------------------------
#  ADD MACRO DEFINITIONS AFTER THIS LINE
#=============================

INC_cygwin32 += pcap.h pcap-bpf.h bpf.h Packet32.h
INC_WIN32    += pcap.h pcap-bpf.h bpf.h Packet32.h pcap-stdinc.h bittypes.h ip6_misc.h

ifeq ($(T_A), win32-x86)
LIB_INSTALLS_WIN32    += ../os/WIN32/wpcap.lib ../os/WIN32/Packet.lib
BIN_INSTALLS_WIN32    += ../os/WIN32/wpcap.dll ../os/WIN32/Packet.dll
endif
ifeq ($(T_A), windows-x64)
LIB_INSTALLS_WIN32    += ../os/WIN32/x64/wpcap.lib ../os/WIN32/x64/Packet.lib
BIN_INSTALLS_WIN32    += ../os/WIN32/x64/wpcap.dll ../os/WIN32/x64/Packet.dll
endif
ifeq ($(T_A),cygwin-x86)
LIB_INSTALLS_cygwin32    += ../os/WIN32/wpcap.lib ../os/WIN32/Packet.lib
BIN_INSTALLS_cygwin32    += ../os/WIN32/wpcap.dll ../os/WIN32/Packet.dll
endif

include $(TOP)/configure/RULES
#----------------------------------------
#  ADD RULES AFTER THIS LINE
