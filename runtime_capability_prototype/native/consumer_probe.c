#define _GNU_SOURCE

#include <errno.h>
#include <fcntl.h>
#include <grp.h>
#include <linux/audit.h>
#include <linux/capability.h>
#include <linux/filter.h>
#include <linux/io_uring.h>
#include <linux/seccomp.h>
#include <sched.h>
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>
#include <sys/prctl.h>
#include <sys/sendfile.h>
#include <sys/socket.h>
#include <sys/stat.h>
#include <sys/syscall.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>

#ifndef __NR_openat2
#define __NR_openat2 437
#endif
#ifndef __NR_io_uring_setup
#define __NR_io_uring_setup 425
#endif
#ifndef __NR_copy_file_range
#define __NR_copy_file_range 326
#endif
#ifndef __NR_execveat
#define __NR_execveat 322
#endif
#ifndef __NR_open_tree
#define __NR_open_tree 428
#endif
#ifndef __NR_move_mount
#define __NR_move_mount 429
#endif
#ifndef __NR_fsopen
#define __NR_fsopen 430
#endif
#ifndef __NR_fsmount
#define __NR_fsmount 432
#endif
#ifndef __NR_fspick
#define __NR_fspick 433
#endif
#ifndef __NR_pidfd_open
#define __NR_pidfd_open 434
#endif
#ifndef __NR_pidfd_getfd
#define __NR_pidfd_getfd 438
#endif
#ifndef __NR_mount_setattr
#define __NR_mount_setattr 442
#endif

#define BOOK1_LENGTH 32439

static int env_fd(const char *name) {
    const char *value = getenv(name);
    if (!value) {
        return -1;
    }
    return atoi(value);
}

static int count_token(const unsigned char *buffer, size_t length, const char *token) {
    const size_t token_length = strlen(token);
    int count = 0;
    if (token_length == 0 || token_length > length) {
        return 0;
    }
    for (size_t index = 0; index + token_length <= length; ++index) {
        if (memcmp(buffer + index, token, token_length) == 0) {
            ++count;
        }
    }
    return count;
}

static int drop_capabilities(void) {
#ifdef PR_CAP_AMBIENT
    if (prctl(PR_CAP_AMBIENT, PR_CAP_AMBIENT_CLEAR_ALL, 0, 0, 0) != 0 && errno != EINVAL) {
        return -1;
    }
#endif
    for (int capability = 0; capability <= CAP_LAST_CAP; ++capability) {
        if (prctl(PR_CAPBSET_DROP, capability, 0, 0, 0) != 0 && errno != EINVAL) {
            return -1;
        }
    }
    struct __user_cap_header_struct header = {
        .version = _LINUX_CAPABILITY_VERSION_3,
        .pid = 0,
    };
    struct __user_cap_data_struct data[2];
    memset(data, 0, sizeof(data));
    return (int)syscall(__NR_capset, &header, &data);
}

static int install_filter(void) {
    struct sock_filter filter[256];
    size_t index = 0;

#define ADD(statement) filter[index++] = (struct sock_filter)statement
#define DENY_SYSCALL(number)                                                   \
    do {                                                                       \
        ADD(BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, (number), 0, 1));             \
        ADD(BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_ERRNO | (EPERM & 0xffff)));  \
    } while (0)

    ADD(BPF_STMT(BPF_LD | BPF_W | BPF_ABS, offsetof(struct seccomp_data, arch)));
    ADD(BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, AUDIT_ARCH_X86_64, 1, 0));
    ADD(BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_KILL_PROCESS));
    ADD(BPF_STMT(BPF_LD | BPF_W | BPF_ABS, offsetof(struct seccomp_data, nr)));

#ifdef __NR_open
    DENY_SYSCALL(__NR_open);
#endif
    DENY_SYSCALL(__NR_openat);
    DENY_SYSCALL(__NR_openat2);
#ifdef __NR_creat
    DENY_SYSCALL(__NR_creat);
#endif
    DENY_SYSCALL(__NR_socket);
#ifdef __NR_connect
    DENY_SYSCALL(__NR_connect);
#endif
    DENY_SYSCALL(__NR_mmap);
    DENY_SYSCALL(__NR_sendfile);
    DENY_SYSCALL(__NR_splice);
    DENY_SYSCALL(__NR_copy_file_range);
    DENY_SYSCALL(__NR_io_uring_setup);
    DENY_SYSCALL(__NR_clone);
#ifdef __NR_clone3
    DENY_SYSCALL(__NR_clone3);
#endif
    DENY_SYSCALL(__NR_fork);
    DENY_SYSCALL(__NR_vfork);
    DENY_SYSCALL(__NR_execve);
    DENY_SYSCALL(__NR_execveat);
#ifdef __NR_chroot
    DENY_SYSCALL(__NR_chroot);
#endif
#ifdef __NR_fchdir
    DENY_SYSCALL(__NR_fchdir);
#endif
#ifdef __NR_mount
    DENY_SYSCALL(__NR_mount);
#endif
#ifdef __NR_umount2
    DENY_SYSCALL(__NR_umount2);
#endif
#ifdef __NR_pivot_root
    DENY_SYSCALL(__NR_pivot_root);
#endif
#ifdef __NR_setns
    DENY_SYSCALL(__NR_setns);
#endif
#ifdef __NR_unshare
    DENY_SYSCALL(__NR_unshare);
#endif
#ifdef __NR_open_by_handle_at
    DENY_SYSCALL(__NR_open_by_handle_at);
#endif
#ifdef __NR_name_to_handle_at
    DENY_SYSCALL(__NR_name_to_handle_at);
#endif
#ifdef __NR_ptrace
    DENY_SYSCALL(__NR_ptrace);
#endif
#ifdef __NR_process_vm_readv
    DENY_SYSCALL(__NR_process_vm_readv);
#endif
#ifdef __NR_process_vm_writev
    DENY_SYSCALL(__NR_process_vm_writev);
#endif
    DENY_SYSCALL(__NR_pidfd_open);
    DENY_SYSCALL(__NR_pidfd_getfd);
    DENY_SYSCALL(__NR_open_tree);
    DENY_SYSCALL(__NR_move_mount);
    DENY_SYSCALL(__NR_fsopen);
    DENY_SYSCALL(__NR_fsmount);
    DENY_SYSCALL(__NR_fspick);
    DENY_SYSCALL(__NR_mount_setattr);
#ifdef __NR_mkdir
    DENY_SYSCALL(__NR_mkdir);
#endif
#ifdef __NR_mkdirat
    DENY_SYSCALL(__NR_mkdirat);
#endif
#ifdef __NR_mknod
    DENY_SYSCALL(__NR_mknod);
#endif
#ifdef __NR_mknodat
    DENY_SYSCALL(__NR_mknodat);
#endif
#ifdef __NR_rename
    DENY_SYSCALL(__NR_rename);
#endif
#ifdef __NR_renameat
    DENY_SYSCALL(__NR_renameat);
#endif
#ifdef __NR_renameat2
    DENY_SYSCALL(__NR_renameat2);
#endif
#ifdef __NR_link
    DENY_SYSCALL(__NR_link);
#endif
#ifdef __NR_linkat
    DENY_SYSCALL(__NR_linkat);
#endif
#ifdef __NR_symlink
    DENY_SYSCALL(__NR_symlink);
#endif
#ifdef __NR_symlinkat
    DENY_SYSCALL(__NR_symlinkat);
#endif
#ifdef __NR_unlink
    DENY_SYSCALL(__NR_unlink);
#endif
#ifdef __NR_unlinkat
    DENY_SYSCALL(__NR_unlinkat);
#endif
#ifdef __NR_truncate
    DENY_SYSCALL(__NR_truncate);
#endif
#ifdef __NR_ftruncate
    DENY_SYSCALL(__NR_ftruncate);
#endif
#ifdef __NR_capset
    DENY_SYSCALL(__NR_capset);
#endif
#ifdef __NR_setuid
    DENY_SYSCALL(__NR_setuid);
#endif
#ifdef __NR_setgid
    DENY_SYSCALL(__NR_setgid);
#endif
#ifdef __NR_setreuid
    DENY_SYSCALL(__NR_setreuid);
#endif
#ifdef __NR_setregid
    DENY_SYSCALL(__NR_setregid);
#endif
#ifdef __NR_setresuid
    DENY_SYSCALL(__NR_setresuid);
#endif
#ifdef __NR_setresgid
    DENY_SYSCALL(__NR_setresgid);
#endif
#ifdef __NR_prctl
    DENY_SYSCALL(__NR_prctl);
#endif
    ADD(BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_ALLOW));

    struct sock_fprog program = {
        .len = (unsigned short)index,
        .filter = filter,
    };
    if (prctl(PR_SET_NO_NEW_PRIVS, 1, 0, 0, 0) != 0) {
        return -1;
    }
    if (prctl(PR_SET_SECCOMP, SECCOMP_MODE_FILTER, &program) != 0) {
        return -1;
    }
    return 0;
}

static int blocked_result(long result) {
    return result < 0 && errno == EPERM;
}

int main(void) {
    const int slice_fd = env_fd("CTDE_SLICE_FD");
    const int ready_fd = env_fd("CTDE_READY_FD");
    const int go_fd = env_fd("CTDE_GO_FD");
    const int leak_fd = env_fd("CTDE_LEAK_FD");
    const char *sandbox_root = getenv("CTDE_SANDBOX_ROOT");
    const char *attack = getenv("CTDE_ATTACK");
    const char *host_path = getenv("CTDE_HOST_PATH");
    const char *workspace_path = getenv("CTDE_WORKSPACE_PATH");
    if (!attack) attack = "none";
    if (!host_path) host_path = "/host-only-not-provided";
    if (!workspace_path) workspace_path = "/workspace-not-provided";

    if (slice_fd < 0 || ready_fd < 0 || go_fd < 0 || !sandbox_root) {
        return 70;
    }

    int helper_pipe[2];
    if (pipe2(helper_pipe, O_CLOEXEC) != 0) {
        return 71;
    }
    int destination_fd = (int)syscall(__NR_memfd_create, "ctde-discard", MFD_CLOEXEC);
    if (destination_fd < 0) {
        return 72;
    }

    for (int fd = 3; fd < 1024; ++fd) {
        if (fd != slice_fd && fd != ready_fd && fd != go_fd &&
            fd != helper_pipe[0] && fd != helper_pipe[1] && fd != destination_fd &&
            fd != leak_fd) {
            close(fd);
        }
    }

    struct stat slice_stat;
    if (fstat(slice_fd, &slice_stat) != 0 || slice_stat.st_size != BOOK1_LENGTH) {
        return 73;
    }
    int seals = fcntl(slice_fd, F_GET_SEALS);
    int sealed = seals >= 0 &&
        (seals & (F_SEAL_WRITE | F_SEAL_GROW | F_SEAL_SHRINK | F_SEAL_SEAL)) ==
            (F_SEAL_WRITE | F_SEAL_GROW | F_SEAL_SHRINK | F_SEAL_SEAL);

    unsigned char *buffer = malloc(BOOK1_LENGTH + 1);
    if (!buffer) {
        return 74;
    }

    if (chroot(sandbox_root) != 0 || chdir("/") != 0) {
        return 75;
    }
    int supplementary_groups_cleared = 1;
    int setgroups_errno = 0;
    if (setgroups(0, NULL) != 0) {
        supplementary_groups_cleared = 0;
        setgroups_errno = errno;
    }
    if (drop_capabilities() != 0) {
        return 87;
    }
    if (prctl(PR_SET_DUMPABLE, 1, 0, 0, 0) != 0) {
        return 88;
    }
    const int uid_drop_supported = 0;

    struct stat hidden_stat;
    errno = 0;
    int workspace_visible = lstat(workspace_path, &hidden_stat) == 0;
    int workspace_stat_errno = errno;
    errno = 0;
    int host_path_visible = lstat(host_path, &hidden_stat) == 0;
    int host_path_stat_errno = errno;

    if (write(ready_fd, "R", 1) != 1) {
        return 77;
    }
    char go = 0;
    if (read(go_fd, &go, 1) != 1 || go != 'G') {
        return 78;
    }

    if (install_filter() != 0) {
        return 79;
    }
    if (write(ready_fd, "S", 1) != 1) {
        return 80;
    }
    if (read(go_fd, &go, 1) != 1 || go != 'G') {
        return 81;
    }

    int attack_denied = 1;
    int attack_success_bytes = 0;
    int attack_errno = 0;
    errno = 0;
    if (strcmp(attack, "open_path") == 0 || strcmp(attack, "greek_path") == 0) {
        long result = open(host_path, O_RDONLY | O_CLOEXEC);
        attack_errno = errno;
        attack_denied = blocked_result(result);
        if (result >= 0) close((int)result);
    } else if (strncmp(attack, "write_", 6) == 0) {
        long result = open(host_path, O_WRONLY | O_CREAT | O_CLOEXEC, 0600);
        attack_errno = errno;
        attack_denied = blocked_result(result);
        if (result >= 0) close((int)result);
    } else if (strcmp(attack, "mmap") == 0) {
        void *result = mmap(NULL, 64, PROT_READ, MAP_PRIVATE, slice_fd, 0);
        attack_errno = errno;
        attack_denied = result == MAP_FAILED && errno == EPERM;
        if (result != MAP_FAILED) munmap(result, 64);
    } else if (strcmp(attack, "sendfile") == 0) {
        off_t offset = 0;
        long result = sendfile(helper_pipe[1], slice_fd, &offset, 64);
        attack_errno = errno;
        attack_denied = blocked_result(result);
        if (result > 0) attack_success_bytes = (int)result;
    } else if (strcmp(attack, "splice") == 0) {
        long result = splice(slice_fd, NULL, helper_pipe[1], NULL, 64, 0);
        attack_errno = errno;
        attack_denied = blocked_result(result);
        if (result > 0) attack_success_bytes = (int)result;
    } else if (strcmp(attack, "copy_file_range") == 0) {
        loff_t in_offset = 0;
        loff_t out_offset = 0;
        long result = copy_file_range(slice_fd, &in_offset, destination_fd, &out_offset, 64, 0);
        attack_errno = errno;
        attack_denied = blocked_result(result);
        if (result > 0) attack_success_bytes = (int)result;
    } else if (strcmp(attack, "io_uring") == 0) {
        struct io_uring_params params;
        memset(&params, 0, sizeof(params));
        long result = syscall(__NR_io_uring_setup, 2, &params);
        attack_errno = errno;
        attack_denied = blocked_result(result);
        if (result >= 0) close((int)result);
    } else if (strcmp(attack, "child_escape") == 0) {
        long result = fork();
        attack_errno = errno;
        attack_denied = blocked_result(result);
        if (result == 0) _exit(84);
        if (result > 0) waitpid((pid_t)result, NULL, 0);
    } else if (strcmp(attack, "network") == 0) {
        long result = socket(AF_INET, SOCK_STREAM, 0);
        attack_errno = errno;
        attack_denied = blocked_result(result);
        if (result >= 0) close((int)result);
    }

    if (lseek(slice_fd, 0, SEEK_SET) < 0) {
        return 85;
    }
    size_t total = 0;
    while (total < BOOK1_LENGTH) {
        ssize_t count = read(slice_fd, buffer + total, BOOK1_LENGTH - total);
        if (count < 0) {
            return 86;
        }
        if (count == 0) break;
        total += (size_t)count;
    }
    buffer[total] = 0;

    int book1 = count_token(buffer, total, "<BOOK_01");
    int book1_close = count_token(buffer, total, "</BOOK_01>");
    int book2 = count_token(buffer, total, "<BOOK_02") +
                count_token(buffer, total, "BOOK_02_DENY_SENTINEL");
    int other_book = count_token(buffer, total, "<BOOK_03");
    int cards = count_token(buffer, total, "<CARD_");
    int paragraphs = count_token(buffer, total, "<PARA_");
    int prefix = count_token(buffer, total, "PREFIX_DENY_SENTINEL");
    int greek = count_token(buffer, total, "FIXTURE_GREEK_DENY");
    int dtd = count_token(buffer, total, "<!DOCTYPE");
    int entity = count_token(buffer, total, "<!ENTITY") + count_token(buffer, total, "&x;");
    int external_ref = count_token(buffer, total, "SYSTEM") + count_token(buffer, total, "PUBLIC");
    int namespace_ok = count_token(buffer, total, "xmlns=\"urn:ctde:synthetic\"") == 1;
    int recovery_needed = book1 == 1 && book1_close != 1;

    const char *parser_status = "pass";
    if (dtd || entity || external_ref || recovery_needed) {
        parser_status = "BLOCKED_BOUNDED_FRAGMENT_UNPARSABLE";
    } else if (book2 || other_book || book1 != 1) {
        parser_status = "INVALIDATED_PROTOTYPE_SCOPE_EXCEEDED";
    } else if (cards != 10 || paragraphs != 10 || !namespace_ok) {
        parser_status = "BLOCKED_CARD_MAPPING_INVALID";
    }

    printf("{\"sandbox_backend\":\"chroot+single-uid-map+capability-drop+seccomp\"," 
           "\"uid\":%d,\"gid\":%d,\"uid_drop_supported\":%s,\"seccomp_active\":true,"
           "\"supplementary_groups_cleared\":%s,\"setgroups_errno\":%d,"
           "\"slice_sealed\":%s,\"slice_bytes\":%zu,"
           "\"workspace_visible\":%s,\"workspace_stat_errno\":%d,"
           "\"host_path_visible\":%s,\"host_path_stat_errno\":%d,"
           "\"network_source_fetch_allowed\":false,"
           "\"attack\":\"%s\",\"attack_denied\":%s,"
           "\"attack_errno\":%d,\"attack_success_bytes\":%d,"
           "\"book1_markers\":%d,\"book2_markers\":%d,"
           "\"other_book_markers\":%d,\"card_markers\":%d,"
           "\"paragraph_markers\":%d,\"prefix_markers\":%d,"
           "\"greek_markers\":%d,\"dtd_markers\":%d,"
           "\"entity_markers\":%d,\"external_reference_markers\":%d,"
           "\"namespace_ok\":%s,\"parser_status\":\"%s\"}\n",
           (int)getuid(), (int)getgid(), uid_drop_supported ? "true" : "false",
           supplementary_groups_cleared ? "true" : "false",
           setgroups_errno, sealed ? "true" : "false", total,
           workspace_visible ? "true" : "false", workspace_stat_errno,
           host_path_visible ? "true" : "false", host_path_stat_errno,
           attack, attack_denied ? "true" : "false", attack_errno,
           attack_success_bytes, book1, book2, other_book, cards, paragraphs,
           prefix, greek, dtd, entity, external_ref,
           namespace_ok ? "true" : "false", parser_status);
    fflush(stdout);
    return 0;
}
