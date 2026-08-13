# Runtime OS Observability Preflight Result

Phase: `2-G-R1 — Runtime OS Observability Capability Preflight`  
Suite: `OSOP-20260811-001`  
Environment: `synthetic_non_literary_only`  
Final status: `BLOCKED_OS_OBSERVABILITY_INSUFFICIENT`  
R1 satisfied: `false`  
Allow R2: `false`

## 1. 结论

`R1 = BLOCKED_OS_OBSERVABILITY_INSUFFICIENT`。

当前环境能提供独立的 `/proc`、PID namespace、pidfd、FD snapshot 与 inotify 路径事件等局部 OS 观测；但它不能提供完整、进程归属明确、覆盖全部 descendants 和文件读取通道的 syscall/file-open trace。因此这些局部 OS 信号不能合成为 R1 所要求的 A2 audit capability，也不能证明 consumer 的完整文件访问集合。

当前环境的**端到端最高 evidence level 为 `A1`**。个别 PID／`/proc`／FD snapshot capability 有 A2 级独立证据，但 qualification-wide A2 不成立；A3 也不成立，因为本阶段没有 Runtime A1 pipeline 与完整 A2 observer 的同一 attempt 绑定。

由于 R1 未通过，本阶段明确禁止进入 R2，且未执行 R2／R3／R4。

## 2. Probe 实际枚举与结果

Probe 数量来自 `probe_manifest.json`、40 个 terminal ledger 和 runner aggregate 的真实枚举：

| 指标 | 实际值 |
| --- | ---: |
| Manifest | 40 |
| Discovered | 40 |
| Executed | 40 |
| Terminal | 40 |
| PASS | 22 |
| FAIL | 16 |
| UNKNOWN | 2 |

闭合等式：`executed = PASS + FAIL + UNKNOWN = 40`；结果为 `成立`。

`PASS` 只表示对应的窄 capability 被实际探针确认，不表示整个 R1 PASS。完整能力矩阵见 `OS_OBSERVABILITY_CAPABILITY_MATRIX.json`。

## 3. PID / process namespace

- Controller namespace PID：`2`；`/proc` 外层 PID：`959040`。
- Controller `NSpid`：`[959040, 2]`；PID namespace：`pid:[4026532287]`。
- Synthetic child `Popen.pid`（namespace PID）：`13`。
- Synthetic child 外层 PID：`959068`；starttime：`5661571`。
- PID mapping：`PASS`。映射依据为 exact nonce + `NSpid` tail + outer `PPid` + `/proc/<outer>/stat` starttime，不使用数值猜测。
- Parent-child relation：`PASS`。
- Known synthetic descendant tree：`PASS`；完整 syscall observer descendant coverage：`FAIL`。
- Lifecycle：`PASS`；pidfd supporting proof：`PASS`。
- 三次独立重复 mapping：`PASS`。

Host PID 层在 `NSpid` 中可见，但 namespace PID 不能直接当作当前挂载 `/proc/<pid>` 的索引；runner 记录了直接路径是否 absent/alias，并只使用经联合身份验证的外层 PID。

## 4. /proc 与 FD 可观测性

| 能力 | 结果 |
| --- | --- |
| `/proc/<pid>/status` | `PASS` |
| `/proc/<pid>/cmdline` | `PASS` |
| `/proc/<pid>/fd` | `PASS` |
| `/proc/<pid>/fdinfo` | `PASS` |
| FD target → device/inode | `PASS` |
| root/ns/UID/GID/caps/NoNewPrivs/seccomp | `PASS` |

Allowed synthetic file 的 held FD 正控制数：`2`。Reference synthetic file 的 instantaneous held-FD 数：`0`。

该 reference 零值只证明采样时点没有 held FD；它不能排除短暂 `open/read/close`，因此未被用作完整文件访问集合的 A2 证明。

## 5. ptrace / strace 实测

- `strace` executable：`/usr/bin/strace`；版本命令实际结果：`PASS`。
- Launch tracing：`FAIL`；return code：`1`；trace bytes：`0`。
- Attach tracing：`FAIL`；return code：`1`；trace bytes：`0`。
- `PTRACE_TRACEME`：`FAIL`；stdout/stderr：`ptrace_traceme_rc=-1 errno=1 message=Operation not permitted`。
- Direct-parent `PTRACE_ATTACH`：`FAIL`；errno：`1`。
- `fanotify_init`：`FAIL`；errno：`1` (`Operation not permitted`).
- Seccomp：`2`；NoNewPrivs：`1`；effective capabilities：`00000000a00425fb`。
- Relevant capabilities：`{"CAP_AUDIT_CONTROL": false, "CAP_BPF": false, "CAP_PERFMON": false, "CAP_SYS_ADMIN": false, "CAP_SYS_PTRACE": false}`。
- Yama `ptrace_scope`：`not_exposed`。

Launch stderr：`/usr/bin/strace: test_ptrace_get_syscall_info: PTRACE_TRACEME: Operation not permitted
/usr/bin/strace: ptrace(PTRACE_TRACEME, ...): Operation not permitted
/usr/bin/strace: PTRACE_SETOPTIONS: Operation not permitted
/usr/bin/strace: cleanup: waitpid(-1, __WALL): No child processes`  
Attach stderr：`/usr/bin/strace: test_ptrace_get_syscall_info: PTRACE_TRACEME: Operation not permitted
/usr/bin/strace: attach: ptrace(PTRACE_ATTACH, 23): Operation not permitted`

命令存在没有被当作 capability PASS；launch、attach 和原生 ptrace 都以实际 synthetic probe 结果判定。

## 6. Process-level filesystem evidence

Synthetic fixtures：

- Allowed：`runtime_os_observability_preflight/runs/OSOP-20260811-001/fixtures/allowed.synthetic`，248 bytes，non-empty。
- Reference/not-opened：`runtime_os_observability_preflight/runs/OSOP-20260811-001/fixtures/reference_not_opened.synthetic`，264 bytes，non-empty。

Consumer 逻辑（A1）只请求 allowed file。独立 OS supporting evidence 显示：

- `/proc` held-FD allowed positive：`2`。
- `/proc` held-FD reference snapshot：`0`。
- inotify allowed events：`2`，其中 open events：`1`。
- inotify reference events：`0`。

但 inotify event 不含 PID，只覆盖两个已知 watched path；`/proc/fd` 只覆盖采样时刻。由于 strace/ptrace/fanotify 均未提供完整 PID-attributed trace，无法证明 consumer tree 的**完整实际文件打开集合**，也无法把 reference 的零事件提升为完整 A2 negative proof。

## 7. Audit independence

- 局部 `/proc`／pidfd／inotify 证据由 controller/kernel 取得，不依赖 consumer 自报；因此它们是独立 supporting signals。
- 完整 syscall/file-open evidence 不可用。
- Sacrificial evidence tamper probe：`MODIFIABLE`。当前相同 execution identity 能修改 mode `0400` 的测试 evidence 文件，因此“consumer 对 observer evidence 写权限为 0”未证明。
- 结果：required OS evidence 不能证明独立于 consumer、broker 和 bounded reader；`OSOP-035..037` 均不通过。

## 8. Evidence level 与 R1 Gate

| 判断 | 结果 |
| --- | --- |
| 最高 individual capability level | `A2` |
| 最高 end-to-end qualification level | `A1` |
| Complete PID-attributed open set | `false` |
| Exact event-loss count available | `false` |
| Evidence tamper protection | `false` |
| R1 | `BLOCKED_OS_OBSERVABILITY_INSUFFICIENT` |
| Allow R2 | `false` |

关键 blocker：

- `CANDIDATE_MODEL_BUSINESS_ZERO_COUNTS_A2_UNKNOWN`
- `COMPLETE_FILE_OPEN_SET_UNPROVEN`
- `COMPLETE_OS_EVIDENCE_NOT_INDEPENDENT_OF_BOUNDED_READER`
- `COMPLETE_OS_EVIDENCE_NOT_INDEPENDENT_OF_BROKER`
- `COMPLETE_OS_EVIDENCE_NOT_INDEPENDENT_OF_CONSUMER`
- `CONSUMER_CAN_MODIFY_OBSERVER_EVIDENCE`
- `DESCENDANT_SYSCALL_TRACE_UNAVAILABLE`
- `FANOTIFY_INIT_PERMISSION_DENIED`
- `NETWORK_WRITE_CLOSED_COVERAGE_UNAVAILABLE`
- `OBSERVER_CRASH_FAIL_CLOSED_BEHAVIOR_UNQUALIFIED`
- `OBSERVER_LOSS_ACCOUNTING_UNKNOWN`
- `REAL_SOURCE_ZERO_COUNTS_A2_UNKNOWN`
- `REFERENCE_ZERO_NOT_PROCESS_ATTRIBUTED`
- `SECOND_CHANNEL_CLOSED_COVERAGE_UNAVAILABLE`
- `TRACE_MONITOR_UNAVAILABLE_PTRACE_ATTACH_DENIED`
- `TRACE_MONITOR_UNAVAILABLE_PTRACE_TRACEME_DENIED`
- `TRACE_MONITOR_UNAVAILABLE_STRACE_ATTACH_DENIED`
- `TRACE_MONITOR_UNAVAILABLE_STRACE_LAUNCH_DENIED`

## 9. 边界终检

Controller 的限定动作账本（A1）记录：English TEI read = 0、Greek TEI read = 0、Candidate Run = 0、model calls = 0、business outputs = 0、`story_structure.yaml` = 0、R2/R3/R4 = 0。

现有 Runtime Prototype 的完整树摘要：

- before：`b7f764552e6d5c3e4837544710fe18f58d5e01b6fb1ed2db07235d93764aa640`（3786 entries）
- after：`b7f764552e6d5c3e4837544710fe18f58d5e01b6fb1ed2db07235d93764aa640`（3786 entries）
- unchanged：`true`

两份依据文件 unchanged：`true`。

必须区分：由于 phase-wide complete OS observer 不可用，English/Greek、Candidate/model/business 的 **A2 independently verified counts 保持 `unknown`**，不能伪写成由 OS 证据证明的 0。这一 inability 本身触发 `OSOP-038/039` UNKNOWN，并参与 R1 BLOCKED。操作层面没有执行这些禁止动作；审计层面无法将其升级为 A2 zero proof。

## 10. 所有创建或修改文件

本阶段没有修改任何既有 Runtime／suite／Repair Plan 文件。创建文件如下（目录不单列）：

- `OS_OBSERVABILITY_CAPABILITY_MATRIX.json`
- `RUNTIME_OS_OBSERVABILITY_PREFLIGHT_RESULT.md`
- `phase_2g_r1_os_observability_preflight_BLOCKED.tar.gz`
- `runtime_os_observability_preflight/ARTIFACT_MANIFEST.json`
- `runtime_os_observability_preflight/probe_manifest.json`
- `runtime_os_observability_preflight/probes/synthetic_consumer.c`
- `runtime_os_observability_preflight/run_preflight.py`
- `runtime_os_observability_preflight/runs/OSOP-20260811-001/aggregate/evidence_index.json`
- `runtime_os_observability_preflight/runs/OSOP-20260811-001/aggregate/probe_results.json`
- `runtime_os_observability_preflight/runs/OSOP-20260811-001/bin/synthetic_consumer`
- `runtime_os_observability_preflight/runs/OSOP-20260811-001/evidence/basis_after.json`
- `runtime_os_observability_preflight/runs/OSOP-20260811-001/evidence/basis_before.json`
- `runtime_os_observability_preflight/runs/OSOP-20260811-001/evidence/boundary_controller_ledger.json`
- `runtime_os_observability_preflight/runs/OSOP-20260811-001/evidence/consumer_build.json`
- `runtime_os_observability_preflight/runs/OSOP-20260811-001/evidence/environment.json`
- `runtime_os_observability_preflight/runs/OSOP-20260811-001/evidence/evidence_tamper.json`
- `runtime_os_observability_preflight/runs/OSOP-20260811-001/evidence/fanotify.json`
- `runtime_os_observability_preflight/runs/OSOP-20260811-001/evidence/fixture_identity.json`
- `runtime_os_observability_preflight/runs/OSOP-20260811-001/evidence/process_proc_fd_probe.json`
- `runtime_os_observability_preflight/runs/OSOP-20260811-001/evidence/ptrace_attach.json`
- `runtime_os_observability_preflight/runs/OSOP-20260811-001/evidence/ptrace_traceme.json`
- `runtime_os_observability_preflight/runs/OSOP-20260811-001/evidence/repeated_pid_mapping.json`
- `runtime_os_observability_preflight/runs/OSOP-20260811-001/evidence/runtime_tree_after.json`
- `runtime_os_observability_preflight/runs/OSOP-20260811-001/evidence/runtime_tree_before.json`
- `runtime_os_observability_preflight/runs/OSOP-20260811-001/evidence/sacrificial_observer_evidence.txt`
- `runtime_os_observability_preflight/runs/OSOP-20260811-001/evidence/strace_attach.json`
- `runtime_os_observability_preflight/runs/OSOP-20260811-001/evidence/strace_launch.json`
- `runtime_os_observability_preflight/runs/OSOP-20260811-001/evidence/strace_launch.trace.22`
- `runtime_os_observability_preflight/runs/OSOP-20260811-001/evidence/strace_version.json`
- `runtime_os_observability_preflight/runs/OSOP-20260811-001/evidence/trace_backend_assessment.json`
- `runtime_os_observability_preflight/runs/OSOP-20260811-001/fixtures/allowed.synthetic`
- `runtime_os_observability_preflight/runs/OSOP-20260811-001/fixtures/reference_not_opened.synthetic`
- `runtime_os_observability_preflight/runs/OSOP-20260811-001/terminal/OSOP-001.json`
- `runtime_os_observability_preflight/runs/OSOP-20260811-001/terminal/OSOP-002.json`
- `runtime_os_observability_preflight/runs/OSOP-20260811-001/terminal/OSOP-003.json`
- `runtime_os_observability_preflight/runs/OSOP-20260811-001/terminal/OSOP-004.json`
- `runtime_os_observability_preflight/runs/OSOP-20260811-001/terminal/OSOP-005.json`
- `runtime_os_observability_preflight/runs/OSOP-20260811-001/terminal/OSOP-006.json`
- `runtime_os_observability_preflight/runs/OSOP-20260811-001/terminal/OSOP-007.json`
- `runtime_os_observability_preflight/runs/OSOP-20260811-001/terminal/OSOP-008.json`
- `runtime_os_observability_preflight/runs/OSOP-20260811-001/terminal/OSOP-009.json`
- `runtime_os_observability_preflight/runs/OSOP-20260811-001/terminal/OSOP-010.json`
- `runtime_os_observability_preflight/runs/OSOP-20260811-001/terminal/OSOP-011.json`
- `runtime_os_observability_preflight/runs/OSOP-20260811-001/terminal/OSOP-012.json`
- `runtime_os_observability_preflight/runs/OSOP-20260811-001/terminal/OSOP-013.json`
- `runtime_os_observability_preflight/runs/OSOP-20260811-001/terminal/OSOP-014.json`
- `runtime_os_observability_preflight/runs/OSOP-20260811-001/terminal/OSOP-015.json`
- `runtime_os_observability_preflight/runs/OSOP-20260811-001/terminal/OSOP-016.json`
- `runtime_os_observability_preflight/runs/OSOP-20260811-001/terminal/OSOP-017.json`
- `runtime_os_observability_preflight/runs/OSOP-20260811-001/terminal/OSOP-018.json`
- `runtime_os_observability_preflight/runs/OSOP-20260811-001/terminal/OSOP-019.json`
- `runtime_os_observability_preflight/runs/OSOP-20260811-001/terminal/OSOP-020.json`
- `runtime_os_observability_preflight/runs/OSOP-20260811-001/terminal/OSOP-021.json`
- `runtime_os_observability_preflight/runs/OSOP-20260811-001/terminal/OSOP-022.json`
- `runtime_os_observability_preflight/runs/OSOP-20260811-001/terminal/OSOP-023.json`
- `runtime_os_observability_preflight/runs/OSOP-20260811-001/terminal/OSOP-024.json`
- `runtime_os_observability_preflight/runs/OSOP-20260811-001/terminal/OSOP-025.json`
- `runtime_os_observability_preflight/runs/OSOP-20260811-001/terminal/OSOP-026.json`
- `runtime_os_observability_preflight/runs/OSOP-20260811-001/terminal/OSOP-027.json`
- `runtime_os_observability_preflight/runs/OSOP-20260811-001/terminal/OSOP-028.json`
- `runtime_os_observability_preflight/runs/OSOP-20260811-001/terminal/OSOP-029.json`
- `runtime_os_observability_preflight/runs/OSOP-20260811-001/terminal/OSOP-030.json`
- `runtime_os_observability_preflight/runs/OSOP-20260811-001/terminal/OSOP-031.json`
- `runtime_os_observability_preflight/runs/OSOP-20260811-001/terminal/OSOP-032.json`
- `runtime_os_observability_preflight/runs/OSOP-20260811-001/terminal/OSOP-033.json`
- `runtime_os_observability_preflight/runs/OSOP-20260811-001/terminal/OSOP-034.json`
- `runtime_os_observability_preflight/runs/OSOP-20260811-001/terminal/OSOP-035.json`
- `runtime_os_observability_preflight/runs/OSOP-20260811-001/terminal/OSOP-036.json`
- `runtime_os_observability_preflight/runs/OSOP-20260811-001/terminal/OSOP-037.json`
- `runtime_os_observability_preflight/runs/OSOP-20260811-001/terminal/OSOP-038.json`
- `runtime_os_observability_preflight/runs/OSOP-20260811-001/terminal/OSOP-039.json`
- `runtime_os_observability_preflight/runs/OSOP-20260811-001/terminal/OSOP-040.json`

编译器或操作系统在 workspace 外创建后立即清理的内部临时文件不作为项目 artifact 保留；本清单覆盖本阶段所有持久 workspace 文件。

本报告不授权 Candidate Run，不修改 Repair Plan，不启动 R2、R3 或 R4。
