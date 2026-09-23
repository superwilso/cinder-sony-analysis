/* fbtool — frame capture + touch injection for crawling the stock/W1 UI on an NW-A55.
 *
 * fb0 is 480x800 BGRA, triple-buffered; /sys/class/graphics/fb0/pan says which buffer is live.
 * Touch is protocol A on /dev/input/event1 at 2x screen coordinates, and needs SYN_MT_REPORT.
 *
 *   fbtool hash                                  print the live frame's hash (status bar excluded)
 *   fbtool grab OUT                              write the live frame to OUT (RLE), print hash
 *   fbtool tap X Y                               tap at screen coordinates
 *   fbtool swipe X0 Y0 X1 Y1 DUR_MS HOLD_MS      drag; HOLD_MS > 0 parks at the end so nothing flings
 *   fbtool key DEV CODE                          press+release a key on an input device
 *   fbtool wait BASE QUIET_MS TIMEOUT_MS OUT     wait for the frame to differ from BASE (hex, or 0)
 *                                                and then hold still for QUIET_MS; writes OUT and
 *                                                prints "changed HASH", or "same HASH" on timeout,
 *                                                or "off" if the backlight is 0.
 *
 * RLE file: "RLE1", u32 run count, then runs of (u16 length, u32 BGRA pixel), little endian.
 */
#include <fcntl.h>
#include <linux/input.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>

#define W 480
#define H 800
#define NPIX (W * H)
#define FRAME (NPIX * 4)
#define TOP 80 /* status bar: live clock/battery/format, never part of "the screen changed" */

static uint32_t buf[NPIX];

static long now_ms(void)
{
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return ts.tv_sec * 1000L + ts.tv_nsec / 1000000L;
}

static int read_int_file(const char *p, int dflt)
{
    char b[64] = {0};
    int fd = open(p, O_RDONLY);
    if (fd < 0) return dflt;
    int n = read(fd, b, sizeof b - 1);
    close(fd);
    if (n <= 0) return dflt;
    return atoi(b);
}

static int live_index(void)
{
    char b[64] = {0};
    int fd = open("/sys/class/graphics/fb0/pan", O_RDONLY);
    if (fd < 0) return 0;
    int n = read(fd, b, sizeof b - 1);
    close(fd);
    if (n <= 0) return 0;
    char *c = strchr(b, ',');
    return c ? atoi(c + 1) / H : 0;
}

static int read_frame(void)
{
    int fd = open("/dev/graphics/fb0", O_RDONLY);
    if (fd < 0) return -1;
    off_t off = (off_t)live_index() * FRAME;
    size_t got = 0;
    while (got < FRAME) {
        ssize_t n = pread(fd, (char *)buf + got, FRAME - got, off + got);
        if (n <= 0) break;
        got += n;
    }
    close(fd);
    return got == FRAME ? 0 : -1;
}

static uint64_t hash_frame(void)
{
    uint64_t h = 1469598103934665603ULL;
    /* The right 8 px are Sony's scrollbar, which fades out a second after a scroll: a hash over it
     * would call one settled screen two different screens. */
    for (int y = TOP; y < H; y++) {
        const uint32_t *row = buf + y * W;
        for (int x = 0; x < W - 8; x++) {
            h ^= row[x] & 0x00ffffff;
            h *= 1099511628211ULL;
        }
    }
    return h;
}

static int write_rle(const char *out)
{
    FILE *f = fopen(out, "wb");
    if (!f) return -1;
    uint32_t runs = 0;
    fwrite("RLE1", 1, 4, f);
    fwrite(&runs, 4, 1, f);
    int i = 0;
    while (i < NPIX) {
        uint32_t p = buf[i];
        int j = i + 1;
        while (j < NPIX && buf[j] == p && j - i < 65535) j++;
        uint16_t len = (uint16_t)(j - i);
        fwrite(&len, 2, 1, f);
        fwrite(&p, 4, 1, f);
        runs++;
        i = j;
    }
    fseek(f, 4, SEEK_SET);
    fwrite(&runs, 4, 1, f);
    fclose(f);
    return 0;
}

/* ── input ─────────────────────────────────────────────────────────────────────────────────── */
static int ev_fd = -1;

static void emit(int type, int code, int value)
{
    struct input_event e;
    memset(&e, 0, sizeof e);
    e.type = type;
    e.code = code;
    e.value = value;
    if (write(ev_fd, &e, sizeof e) != sizeof e) perror("write");
}

static void contact(int x, int y, int first)
{
    if (first) emit(EV_KEY, BTN_TOUCH, 1);
    emit(EV_ABS, ABS_MT_TOUCH_MAJOR, 40);
    if (first) emit(EV_ABS, ABS_MT_WIDTH_MAJOR, 40);
    emit(EV_ABS, ABS_MT_POSITION_X, x * 2);
    emit(EV_ABS, ABS_MT_POSITION_Y, y * 2);
    emit(EV_SYN, SYN_MT_REPORT, 0);
    emit(EV_SYN, SYN_REPORT, 0);
}

static void lift(void)
{
    emit(EV_ABS, ABS_MT_TOUCH_MAJOR, 0);
    emit(EV_SYN, SYN_MT_REPORT, 0);
    emit(EV_KEY, BTN_TOUCH, 0);
    emit(EV_SYN, SYN_REPORT, 0);
}

static int open_touch(void)
{
    ev_fd = open("/dev/input/event1", O_WRONLY);
    if (ev_fd < 0) { perror("event1"); return -1; }
    return 0;
}

int main(int argc, char **argv)
{
    if (argc < 2) { fprintf(stderr, "usage: see source\n"); return 2; }
    const char *cmd = argv[1];

    if (!strcmp(cmd, "hash")) {
        if (read_frame()) return 1;
        printf("%016llx\n", (unsigned long long)hash_frame());
        return 0;
    }
    if (!strcmp(cmd, "grab") && argc == 3) {
        if (read_frame() || write_rle(argv[2])) return 1;
        printf("%016llx\n", (unsigned long long)hash_frame());
        return 0;
    }
    if (!strcmp(cmd, "tap") && argc == 4) {
        if (open_touch()) return 1;
        /* NO "wake touch" first. A dimmed panel (brightness 2) takes an injected tap like a lit one —
         * and injected taps never bring the brightness back up, so a wake touch was only ever a
         * second, unaimed tap. There is no spot that is dead on every screen: at (472,118) it
         * flipped the Equalizer panel's Direct switch, at (20,118) it opened the Library's
         * "turn on USB DAC?" dialog (both 2026-09-23). */
        contact(atoi(argv[2]), atoi(argv[3]), 1);
        usleep(60000);
        lift();
        return 0;
    }
    if (!strcmp(cmd, "swipe") && argc == 8) {
        if (open_touch()) return 1;
        int x0 = atoi(argv[2]), y0 = atoi(argv[3]), x1 = atoi(argv[4]), y1 = atoi(argv[5]);
        int dur = atoi(argv[6]), hold = atoi(argv[7]);
        int steps = dur / 16 > 2 ? dur / 16 : 2;
        contact(x0, y0, 1);
        for (int i = 1; i <= steps; i++) {
            usleep(16000);
            contact(x0 + (x1 - x0) * i / steps, y0 + (y1 - y0) * i / steps, 0);
        }
        for (int t = 0; t < hold; t += 50) { /* parked: same point, so the release has no velocity */
            usleep(50000);
            contact(x1, y1, 0);
        }
        lift();
        return 0;
    }
    if (!strcmp(cmd, "key") && argc == 4) {
        ev_fd = open(argv[2], O_WRONLY);
        if (ev_fd < 0) { perror(argv[2]); return 1; }
        int code = atoi(argv[3]);
        emit(EV_KEY, code, 1);
        emit(EV_SYN, SYN_REPORT, 0);
        usleep(60000);
        emit(EV_KEY, code, 0);
        emit(EV_SYN, SYN_REPORT, 0);
        return 0;
    }
    if (!strcmp(cmd, "wait") && argc == 6) {
        uint64_t base = strtoull(argv[2], NULL, 16);
        int quiet = atoi(argv[3]), timeout = atoi(argv[4]);
        const char *out = argv[5];
        long t0 = now_ms(), stable_since = 0;
        uint64_t last = 0;
        int changed = 0;
        for (;;) {
            if (read_int_file("/sys/class/leds/lcd-backlight/brightness", 1) == 0) {
                printf("off\n");
                return 0;
            }
            if (read_frame()) return 1;
            uint64_t h = hash_frame();
            long t = now_ms();
            if (h != base) changed = 1;
            if (h != last) { last = h; stable_since = t; }
            if (changed && t - stable_since >= quiet) break;
            if (!changed && t - t0 >= timeout) {
                printf("same %016llx\n", (unsigned long long)h);
                return 0;
            }
            if (t - t0 >= timeout + 4000) break; /* animating forever: take what is there */
            usleep(20000);
        }
        if (write_rle(out)) return 1;
        printf("changed %016llx\n", (unsigned long long)last);
        return 0;
    }
    fprintf(stderr, "fbtool: bad command\n");
    return 2;
}
