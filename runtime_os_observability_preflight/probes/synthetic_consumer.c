#define _GNU_SOURCE
#include <errno.h>
#include <fcntl.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/ptrace.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>

static void die(const char *message) {
    fprintf(stderr, "%s: %s\n", message, strerror(errno));
    fflush(stderr);
    _exit(111);
}

static int open_and_read(const char *path) {
    char buffer[64];
    int fd = open(path, O_RDONLY | O_CLOEXEC);
    if (fd < 0) die("open allowed");
    ssize_t amount = read(fd, buffer, sizeof(buffer));
    if (amount < 0) die("read allowed");
    return fd;
}

static void wait_byte(void) {
    char value;
    ssize_t amount;
    do {
        amount = read(STDIN_FILENO, &value, 1);
    } while (amount < 0 && errno == EINTR);
    if (amount != 1) _exit(112);
}

static void mode_hold_tree(const char *allowed, const char *nonce) {
    printf("PRE pid=%ld ppid=%ld nonce=%s\n", (long)getpid(), (long)getppid(), nonce);
    fflush(stdout);
    wait_byte();
    int fd = open_and_read(allowed);
    pid_t descendant = fork();
    if (descendant < 0) die("fork");
    if (descendant == 0) {
        for (;;) pause();
    }
    printf("POST pid=%ld descendant=%ld fd=%d nonce=%s\n", (long)getpid(), (long)descendant, fd, nonce);
    fflush(stdout);
    wait_byte();
    kill(descendant, SIGTERM);
    waitpid(descendant, NULL, 0);
    close(fd);
    _exit(0);
}

static void mode_single_open(const char *allowed) {
    int fd = open_and_read(allowed);
    close(fd);
    _exit(0);
}

static void mode_attach_wait(const char *allowed, const char *nonce) {
    printf("ATTACH_READY pid=%ld ppid=%ld nonce=%s\n", (long)getpid(), (long)getppid(), nonce);
    fflush(stdout);
    wait_byte();
    int fd = open_and_read(allowed);
    close(fd);
    printf("ATTACH_DONE nonce=%s\n", nonce);
    fflush(stdout);
    wait_byte();
    _exit(0);
}

static void mode_idle(const char *nonce) {
    printf("IDLE_READY pid=%ld ppid=%ld nonce=%s\n", (long)getpid(), (long)getppid(), nonce);
    fflush(stdout);
    wait_byte();
    _exit(0);
}

static void mode_ptrace_traceme(void) {
    errno = 0;
    long rc = ptrace(PTRACE_TRACEME, 0, NULL, NULL);
    int saved_errno = errno;
    printf("ptrace_traceme_rc=%ld errno=%d message=%s\n", rc, saved_errno,
           saved_errno ? strerror(saved_errno) : "OK");
    fflush(stdout);
    _exit(rc == 0 ? 0 : 1);
}

static void mode_tamper(const char *path) {
    errno = 0;
    int fd = open(path, O_WRONLY | O_TRUNC | O_CLOEXEC);
    int saved_errno = errno;
    if (fd >= 0) {
        const char marker[] = "tampered-by-synthetic-consumer\n";
        (void)write(fd, marker, sizeof(marker) - 1);
        close(fd);
    }
    printf("tamper_open_rc=%d errno=%d message=%s\n", fd, saved_errno,
           saved_errno ? strerror(saved_errno) : "OK");
    fflush(stdout);
    _exit(fd < 0 ? 0 : 3);
}

int main(int argc, char **argv) {
    if (argc < 2) return 64;
    if (strcmp(argv[1], "hold-tree") == 0 && argc == 4) {
        mode_hold_tree(argv[2], argv[3]);
    } else if (strcmp(argv[1], "single-open") == 0 && argc == 3) {
        mode_single_open(argv[2]);
    } else if (strcmp(argv[1], "attach-wait") == 0 && argc == 4) {
        mode_attach_wait(argv[2], argv[3]);
    } else if (strcmp(argv[1], "idle") == 0 && argc == 3) {
        mode_idle(argv[2]);
    } else if (strcmp(argv[1], "ptrace-traceme") == 0 && argc == 2) {
        mode_ptrace_traceme();
    } else if (strcmp(argv[1], "tamper") == 0 && argc == 3) {
        mode_tamper(argv[2]);
    } else {
        fprintf(stderr, "invalid arguments\n");
        return 64;
    }
    return 0;
}
