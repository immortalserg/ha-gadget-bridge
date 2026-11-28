# Legacy realtime steps

Reference: Gadgetbridge GitHub master, app/src/main/java/nodomain/freeyourgadget/gadgetbridge/service/devices/huami/HuamiSupport.java, handleRealtimeSteps(byte[]). The implementation accepts exactly 13 bytes and decodes bytes 1 and 2 as unsigned little-endian steps. Remaining bytes are not decoded by this method. The previous speculative three-field layout was removed. The GitHub mirror is historical; current Codeberg revision and hardware validation remain outstanding.
