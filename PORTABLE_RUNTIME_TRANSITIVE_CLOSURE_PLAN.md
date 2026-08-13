# Classic-to-Drama Engine：Portable Runtime Transitive Closure File-Level Atomic Scope Plan

> 项目：Classic-to-Drama Engine  
> 阶段：Phase 2-G-R3P  
> 文档类型：Portable Runtime Transitive Closure / Component Freeze 文件级原子范围计划  
> 日期：2026-08-11  
> 最终状态：`PASS_PORTABLE_R3_PLAN_ONLY`  
> 当前效力：`planning_only / runtime_unchanged / tests_not_executed / r3_not_authorized`  
> 目标 Profile：`CTDE-PORTABLE-DEV-1`  
> 未来最高可声明证据：`A1 runtime logical evidence only`  
> 认证状态：`Portable / Development / non-certified`  
> Candidate Analysis：`BLOCKED`

## 0. 计划结论、唯一布局与当前边界

### 0.1 最终结论

本计划只关闭 Phase 2-G-R3 在执行前暴露的文件级范围歧义。它选择一套唯一布局、逐一处置四个 legacy 文件、冻结未来 R3 的全部写路径，并把既有 R3 功能要求映射到明确实现文件、verifier 与 evidence 路径。

本计划不执行 R3，不生成 closure manifest，不运行任何测试，也不修改 `runtime_capability_prototype/`。

```yaml
phase: "Phase 2-G-R3P"
final_status: "PASS_PORTABLE_R3_PLAN_ONLY"

runtime_files_inspected_count: 43
mutable_existing_files_count: 0
creatable_files_count: 31
creatable_directories_count: 11
read_only_protected_files_count: 62
forbidden_path_groups_count: 9

legacy_file_dispositions:
  contracts/component_manifest.yaml: "B"
  runtime/build_manifest.py: "C"
  runtime/verify_trace.py: "C"
  runtime/run_suite.py: "C"

canonical_manifest_path: "runtime_capability_prototype/r3_portable_suites/R3PS-20260811-001/control/runtime_transitive_closure_manifest.json"
builder_path: "runtime_capability_prototype/runtime/build_r3_portable_closure.py"
verifier_path: "runtime_capability_prototype/runtime/verify_r3_portable_closure.py"
runner_path: "runtime_capability_prototype/runtime/run_r3_portable_closure.py"
evidence_root: "runtime_capability_prototype/r3_portable_suites/R3PS-20260811-001/evidence/"
final_result_report_path: "PORTABLE_RUNTIME_TRANSITIVE_CLOSURE_RESULT.md"

unresolved_path_ambiguity_count: 0
r3_execution_authorized: false
r4_execution_authorized: false
candidate_execution_authorized: false
```

唯一实现决定如下：

- **不原地修改任何现有 Runtime 或 legacy 文件**；
- 复用现有 `runtime_capability_prototype/contracts/` 与 `runtime_capability_prototype/runtime/`，不创建第二个 Runtime package；
- 新建独立的 R3 closure builder、test-manifest builder、verifier、runner 与 aggregate/report generator；
- 唯一 fresh suite ID 冻结为 `R3PS-20260811-001`；
- 唯一 suite root 冻结为 `runtime_capability_prototype/r3_portable_suites/R3PS-20260811-001/`；唯一 evidence root 是其下的 `evidence/`；
- canonical closure manifest 使用 canonical JSON，不复用旧 suite-specific YAML component manifest；
- production/runtime closure、test-only dependency、build-only dependency、platform boundary 和 excluded dependency 在同一个 canonical graph 中分区，不能互相冒充；
- R2 已完成资产全部只读；若 R3 发现必须修改任何 R2 语义或实现，R3 必须 BLOCKED；
- R4 runner、R4 E2E、Candidate 与 Odyssey source handling 均不在本计划的 R3 写范围内；任何未来 R4 builder/runner/verifier/aggregate/report/schema/policy 或其依赖都必须在 R4 执行前触发一份新路径、新授权的 fresh R3 refresh，不能以 test-only/control 标签绕过 closure。

### 0.2 本阶段唯一产物

本阶段只创建：

```text
PORTABLE_RUNTIME_TRANSITIVE_CLOSURE_PLAN.md
```

本阶段明确没有创建未来 R3 §6 所列的任何文件或目录。

### 0.3 本 Plan 的外部身份

本文件不把自身完整文件 SHA-256 写入正文。完成后的 exact-bytes SHA-256 由本阶段交付信息外部记录。未来 R3 的人工执行授权与 `r3_execution_plan.json` 必须引用该外部 SHA-256；不得从文件名、mtime 或自然语言意图推断 Plan identity。

## 1. 正式依据与执行前真实基线

### 1.1 正式依据

| 正式依据 | 本阶段只读 SHA-256 | 作用 |
| --- | --- | --- |
| `RUNTIME_CAPABILITY_PROTOTYPE_RESULT.md` | `6811bcc4ef0efcaee89013648dd0bb06bbaca154625f3dc47bdfa0f295851753` | Phase 2-G blocker、旧 12-component freeze 与 closure gap |
| `RUNTIME_CAPABILITY_REPAIR_PLAN.md` | `a2c52dbaecf3956cf4a2189abe5401f269d255e8099d3345985619be25be4213` | R3 roots、node types、closure algorithm、freeze 与 acceptance |
| `RUNTIME_ASSURANCE_PROFILE_DECISION.md` | `57471c85c57946f6ceb6da288301cc802533b09c137bfbe8e6e247dad57206e2` | Portable A1 / Hardened A3 双 Profile 与禁止 promotion |
| `PORTABLE_AUTHORIZATION_SCHEMA_V2_PLAN.md` | `32513cdb2c004ea91c7d7208eb3a40901934dc80440af048b84701facf1bdbe9` | R2 文件白名单、R3 deferred 边界与 canonical V2 语义 |
| `PORTABLE_AUTHORIZATION_SCHEMA_V2_IMPLEMENTATION_RESULT.md` | `b47c7280880af70325a5e5c45426951567390441ad4cd61465724fbb8eabcd06` | R2 实际改动、实际新增、51/51 PASS 与只读资产摘要 |
| `CANDIDATE_EXECUTION_CONTRACT_REPAIR.md` | `12ceb01cab4901cb2b7472b1b56f93750a43cb8c28b5f0c9ab89acf3ad4fe7bd` | execution snapshot、runtime component identity、Candidate/R4 隔离 |

### 1.2 Runtime Prototype 当前真实状态

本阶段没有可用 Git worktree，因此使用等价内容树快照，不伪造 Git commit/tree identity。

```yaml
runtime_root: "runtime_capability_prototype"
git_state: "NOT_A_GIT_WORKTREE"
equivalent_content_tree_snapshot_used: true

runtime_file_count: 3062
runtime_directory_count: 1218
runtime_symlink_count: 0
runtime_executable_file_count_outside_suite_and_registry: 1
runtime_executable_file: "bin/consumer_probe"
runtime_content_tree_sha256: "820afae1806d4cec398b54193574e62e1933c2e8745dfb570d00b969bd69fe43"

authorization_schema_v2_sha256: "f1d7c2e36e0d3072624609591eb8dfc20d0e42dce6accc8e87de730ec4478e33"
r2_implementation_result_sha256: "b47c7280880af70325a5e5c45426951567390441ad4cd61465724fbb8eabcd06"
r2_suite_manifest_sha256: "a8f712657b05eb2ea4a55719a664585c0f0754e07709f11ee2683cb130abcd76"
r2_suite_aggregate_sha256: "3941449585b1d7071f703c2858a3f72bbed929ef092f496ae3b30037900c4e61"
```

内容树摘要算法为：按相对于 Runtime root 的规范 POSIX path 排序，对每个普通文件计算 SHA-256，再对 `sha256 + two-space + relative_path + LF` 的排序列表计算 SHA-256。未来 R3 Gate 必须实现并记录同一算法版本；不得把当前数字手工填入未来结果代替重新枚举。

### 1.3 当前 legacy manifest 的真实失配

`contracts/component_manifest.yaml` 仍是 `RCPTS-20260811-002` 的历史 12-component manifest。其完整文件 SHA-256 为：

```text
98f808df536c84f3f989fb2a61eda7e51e2b27e1d131568f799cf43459fba033
```

其中 5 个记录摘要与当前 Runtime bytes 不同，因为 R2 已在自己的获批白名单内修改这些文件：

| 文件 | legacy manifest 摘要 | 当前摘要 |
| --- | --- | --- |
| `runtime/ctde_runtime/authorization_registry.py` | `26dc60926826db207cace0e871d15b587032d4cb3e861c111415d0819707ea82` | `e6ee8923c1c05c1ebdf04106fed659d40b8d394f6cbca4688d437dd58ee446af` |
| `runtime/ctde_runtime/range_broker.py` | `19aaaef83c92d871467a5e463581cc574b6b419f85a9a6ac9086f27868f76b26` | `ef2be994b82f10f025411e1d074cda3d0336e352f063bb9162edbcaed105958a` |
| `runtime/ctde_runtime/bounded_reader.py` | `c49bd965a40e52120207192fe082dc9737b565253dd4cfe62fc200a1a9cf1a99` | `65c8f0a3af625c505fcdc05f7a754075e4829d2183931d71fa8c4dfdbf46f68c` |
| `runtime/ctde_runtime/read_audit.py` | `735d25ff6ff41c6b77538daf1d27550d76211c20098a99a4246b5c91eb662b8b` | `b5c8a9210c4f9f295351b32e3f2a5e310ad0531720ff886a9d84385ec1ab6b4d` |
| `runtime/ctde_runtime/events.py` | `84d05a5c49bdf7e66f9cd68a3941e18b2577420479acf5389c69f1e6852322ac` | `808115293ec818eedd926e4ef63869a7d5f9eeb1dca26a6902c12850b4e7fd15` |

该失配不是修改旧 manifest 的理由。旧 manifest 和旧 suite snapshot 必须保留原字节，继续证明 `RCPTS-20260811-002` 当时冻结的历史对象；R3 使用新 identity。

## 2. Runtime Prototype 只读文件审计

### 2.1 计数口径

`runtime_files_inspected_count=43` 由两部分组成：

- 34 个 Runtime root 下、排除 suite payload/Registry mutable state 后的直接 R3 相关代码、合同、配置、native source/binary；
- 9 个为判断 legacy/R2 状态而选取的 control/aggregate evidence 文件。

本计数不包含 `source/**`、任何 TEI、任何 Candidate 业务文件，也不把 3,062 个 Runtime 文件全部声称为逐文件人工审阅。

### 2.2 直接 R3 相关文件：34 个

以下 path 均相对于 `runtime_capability_prototype/`；`exists` 在本阶段均为 `true`。

| relative_path | exists | role | current_sha256 | current classification |
| --- | --- | --- | --- | --- |
| `bin/consumer_probe` | true | `SandboxSupervisor` 实际启动的静态 ELF probe | `f1f4849e078169d14ae18c91a5469b171534479dd8255de359f588ca1b475c80` | runtime |
| `contracts/audit_attestation_schema.yaml` | true | 旧 RCPT scope/closure attestation schema | `26e5dd5fa0aaeeaded0a5b031badecc91ff166f7f2b24a20bff2a17c45673491` | legacy |
| `contracts/audit_attestation_schema_v2.yaml` | true | R2 Portable A1 audit event V2 合同 | `9728fa6fb64ebfbc1cb260e6986f2d1947fc340445d515e27880e419d0d16da3` | runtime |
| `contracts/authorization_registry_event_schema_v2.yaml` | true | V2 Registry durable event 合同 | `16dc8fec0ab7c1ae152781f7ec177c6679ca4a52a465254f0c98a122c8a59bea` | runtime |
| `contracts/authorization_registry_record_schema_v2.yaml` | true | V2 Registry identity/state 合同 | `4f5241697c987fbefb4531f61e85b010332b988062ee02c83ba2052e5c1c31be` | runtime |
| `contracts/authorization_schema.yaml` | true | 旧 V1 self-digest-mismatch schema | `f6f2940a41867c5471a1a81751112dd7c090b7e56d8ba428664140ffd0420da6` | legacy |
| `contracts/authorization_schema_v2.yaml` | true | canonical Authorization Schema V2 | `f1d7c2e36e0d3072624609591eb8dfc20d0e42dce6accc8e87de730ec4478e33` | runtime |
| `contracts/broker_envelope_schema.yaml` | true | 旧 RCPT broker envelope schema | `c6e0b45fb4632f8cece710035e55217efe74fb9d55b2313d6bd48a5b7f515be4` | legacy |
| `contracts/broker_envelope_schema_v2.yaml` | true | V2 broker authorization-binding 合同 | `c7b8ff11745d607b1511b4f7a11c7944896b9f2f1383e0ccbadda89f0ef91010` | runtime |
| `contracts/capability_claims_schema.yaml` | true | 旧 RCPT capability claims schema | `9c6f6c894c2a1de09909f85a1c4c9e53b5b67408fd944622ca6366443fee24d3` | legacy |
| `contracts/capability_claims_schema_v2.yaml` | true | R2 V2 pending/active capability binding 合同 | `3f872d00524c683ff93a9a8c3e02b63cc1f40da4bec72bb1289887cc0bca06bf` | runtime |
| `contracts/component_manifest.yaml` | true | 旧 `RCPTS-20260811-002` 的 12-component snapshot source | `98f808df536c84f3f989fb2a61eda7e51e2b27e1d131568f799cf43459fba033` | legacy |
| `contracts/r2_portable_authorization_test_requirements.yaml` | true | R2 synthetic requirements source | `0c206312075dc34123fcaef0ec81475f72197618fb7003c1764d9898dee84965` | test-only |
| `contracts/r2_portable_controller_terminal_schema_v1.yaml` | true | R2 controller terminal evidence schema | `7b2a983750a903e43489854750d56d4f6fee31a8fb541615d8247e2bf90454ac` | test-only |
| `contracts/test_policy.yaml` | true | 旧 RCPT synthetic-only test policy | `e22ecb855287bf2761765190e143947dae2781e73a681be2ba5d0f3da093cc7f` | test-only |
| `fixture_specs/synthetic_book1_fixture.yaml` | true | 旧 RCPT synthetic fixture recipe | `a4af84dce3d82604ff7e007ecd7e19ff48fda4b2257e31acaf530a953c8384e1` | test-only |
| `native/consumer_probe.c` | true | native probe build input | `f4057def41b265723538eb28aa7a9e3172536d44de5a54d276fedf3df1aad3fb` | build-only |
| `runtime/build_manifest.py` | true | 硬编码旧 suite 的 197-leaf manifest builder | `78a206e28365cfe7d6caf677ef818ddaddb7db2b920cac535ea84d206205213d` | legacy |
| `runtime/build_r2_portable_manifest.py` | true | R2 manifest/component-input builder | `8f75e72d33d3c1cabf2bce866eac9fb44aec5775c68127576073ce510498828c` | build-only |
| `runtime/run_r2_portable.py` | true | R2 51-leaf Portable authorization test runner | `ec1c86ed0f89a76b497dc9d48ff4fc092c5ff1e78d84fb3dff407a9040a4ca75` | test-only |
| `runtime/run_suite.py` | true | 旧 197-leaf RCPT runner；会重编译 probe、重写 legacy manifest | `caf32bdb9c49ba78ee1671d41b62bc9eb8297343624ceb7afd562443a6794749` | legacy |
| `runtime/verify_trace.py` | true | 旧 `strace`/A2 external access verifier | `d8732e7e788b2ababbc7dac14c09e772daab3e96287704d77022c68e2568bc9d` | legacy |
| `runtime/ctde_runtime/__init__.py` | true | Runtime package initializer/version identity | `5af22556eb42fe18c104234b803bce2a0eedc69a7c8aaba76737c39a7918a16e` | runtime |
| `runtime/ctde_runtime/authorization_registry.py` | true | V1 historical API + 独立 V2 tables/CAS lifecycle | `e6ee8923c1c05c1ebdf04106fed659d40b8d394f6cbca4688d437dd58ee446af` | runtime |
| `runtime/ctde_runtime/authorization_v2.py` | true | V2 loader/schema/semantic validator/typed contexts | `5359cf7289e130f8a3c4228dd6d4c8b0e961ef9da716c05a78169191d571ba4d` | runtime |
| `runtime/ctde_runtime/bounded_reader.py` | true | sealed delivery consume + V2 context binding | `65c8f0a3af625c505fcdc05f7a754075e4829d2183931d71fa8c4dfdbf46f68c` | runtime |
| `runtime/ctde_runtime/common.py` | true | canonical JSON/hash/YAML/atomic-write/shared errors | `20a1d4c184753f007e4da2b11cabc3f96b1049d75aa69673ddfbe0d26344aa56` | runtime |
| `runtime/ctde_runtime/events.py` | true | signed V1 event log + Portable A1 V2 event log | `808115293ec818eedd926e4ef63869a7d5f9eeb1dca26a6902c12850b4e7fd15` | runtime |
| `runtime/ctde_runtime/fixture_factory.py` | true | synthetic fixture functions；同时被 broker/audit 顶层 import 常量和类型 | `c40aef7040c808b68a7f315ec7051cdbbe7424dbc2a62e4bce6278e08743519b` | runtime |
| `runtime/ctde_runtime/formal_loader.py` | true | signed positive allowlist、path/digest/TOCTOU validator | `eb866084c8dc95c52b28118a2669314559d165e6b949cb0ff7edeb111c10e11d` | runtime |
| `runtime/ctde_runtime/range_broker.py` | true | issuer、broker、memfd delivery 与 V2 bindings | `ef2be994b82f10f025411e1d074cda3d0336e352f063bb9162edbcaed105958a` | runtime |
| `runtime/ctde_runtime/read_audit.py` | true | logical scope/closure aggregator 与 V2 correlation | `b5c8a9210c4f9f295351b32e3f2a5e310ad0531720ff886a9d84385ec1ab6b4d` | runtime |
| `runtime/ctde_runtime/sandbox.py` | true | native probe process supervisor、`/proc`/FD/logical isolation checks | `c60aca6b25e933a12e37862c55df8ae8472dca55f03b0ceb871cbcd8eaf8a9d1` | runtime |
| `runtime/ctde_runtime/signing.py` | true | Ed25519 trust store、JWS signing/verification | `5c41a1601b9824715d17ae416513646575006a9207dedd26bb2036336e66cc36` | runtime |

`fixture_factory.py` 的 current classification 是 `runtime`，不是根据文件名判为 test-only：`range_broker.py` 和 `read_audit.py` 都在模块顶层直接 import 它。未来 closure 以实际可达性优先；整个文件 bytes 必须冻结。若要将它移出 runtime closure，必须在独立上游语义修复中消除该依赖，不能由 R3 verifier 假装不可达。

### 2.3 选取的历史/R2 control evidence：9 个

| relative_path | exists | role | current_sha256 | current classification |
| --- | --- | --- | --- | --- |
| `suites/RCPTS-20260811-002/control/runtime_capability_test_manifest.yaml` | true | 历史 197-leaf frozen manifest | `42799e6f56802248a467af0f06b539a817ec7ae224dd91e974ad3157f669a7bf` | legacy |
| `suites/RCPTS-20260811-002/control/suite_component_snapshot.yaml` | true | 历史 12-component start snapshot | `5deafbae23decac17803b84fd8f942cc890db5e7bb958d5d428fc7b3e4f75447` | legacy |
| `suites/RCPTS-20260811-002/control/suite_test_policy_snapshot.yaml` | true | 历史 policy snapshot | `310994aef55e8695010f3dee0b82b2b20bf5d6e6a83fc8db328968b6b1ca3407` | legacy |
| `suites/RCPTS-20260811-002/aggregate/test_results.json` | true | 99 PASS / 98 FAIL final aggregate | `705c852c0c7c9115954b04650a71e08304536991b0e5c8568bb9eaa331c78224` | legacy |
| `suites/RCPTS-20260811-002/aggregate/external_access_audit.json` | true | `coverage_complete=false` 的旧 A2 trace audit | `a696898014ccffd7ba775bdef7385cf74fe56488e8f21e51e6f33f10bc02721e` | legacy |
| `suites/RCPTS-20260811-002/aggregate/evidence_manifest.yaml` | true | 历史 case evidence index | `8ce98ff8d8a6a87d59cd338687bab0d9d74b6b201fdc984b2659524638a1ee45` | legacy |
| `r2_portable_suites/R2PS-20260811-001/control/component_inputs.json` | true | R2 的 15-item input digest set | `ab75e95bc0cdef67fb60f6b04c9fe143e0a8e71b396c1ffe17a2473a59216b1a` | test-only |
| `r2_portable_suites/R2PS-20260811-001/control/r2_portable_manifest.yaml` | true | R2 51-leaf frozen manifest | `a8f712657b05eb2ea4a55719a664585c0f0754e07709f11ee2683cb130abcd76` | test-only |
| `r2_portable_suites/R2PS-20260811-001/aggregate/r2_portable_results.json` | true | R2 51/51 A1/non-certified aggregate | `3941449585b1d7071f703c2858a3f72bbed929ef092f496ae3b30037900c4e61` | test-only |

以上 9 个文件只用于状态与基线审计。它们不因被 R3 引用摘要而成为 production/runtime closure member；未来 R3 也不得复制它们作为自己的 evidence。

### 2.4 当前 platform boundary 候选的只读观察

本阶段没有运行 Python interpreter 或 Runtime。只对文件身份做了只读观察：

```yaml
python_interpreter_resolved_path: "/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python3.12"
python_interpreter_file_sha256: "9ed008e5a8685235361f0c53771b520ab082dd99a877ad2fd796a93fa4c0b488"
python_interpreter_link_mode: "dynamic"

pyyaml_metadata_version: "6.0.3"
pyyaml_metadata_sha256: "03c3b415ed38d09faedc49360e930769b40c58f68585e6de00e2e4916a858d34"
cryptography_metadata_version: "46.0.0"
cryptography_metadata_sha256: "3a0b43d3d3899156136570d7c1141689f21ba9f0e6ea25b05684f7f01dda3096"

native_probe_elf_class: "ELF64 x86-64"
native_probe_link_mode: "static"
native_probe_build_id_sha1: "98f031ed1cc65c32b75f9607e039e9fbb2ecacdb"
os_release: "Ubuntu 24.04.3 LTS"
kernel_release_file_sha256: "74d646cff7cef591607898008fb58038bfe6d46a66069dd7538024a95b1e9f72"
```

这些值不是未来 closure PASS 证据。未来 R3 必须从实际执行环境重新枚举 interpreter、relevant stdlib module origins、PyYAML/cryptography distribution trees、native ABI/libc/loader、kernel/proc boundary 与 compiler identity；本 Plan 不允许把以上观察值预填为通过结果。

## 3. 当前真实 Runtime entrypoint 候选

### 3.1 现状判断

当前没有独立 production CLI/orchestrator。真实 Runtime 由可调用 Python APIs 组成；当前两个高层 executable Python entrypoint 都是测试 runner：

- `runtime/run_suite.py::main`：legacy 197-leaf RCPT runner；
- `runtime/run_r2_portable.py::main`：R2 51-leaf authorization test runner。

因此未来 R3 不得伪造一个不存在的 production executable。`r3_portable_closure_policy_v1.yaml` 必须把下列**现有 callable identities**冻结为 production/runtime roots，同时把新 R3 builder、test-manifest builder、verifier、runner 与 result generator 分别冻结为 build-only 或 test-only control roots。

### 3.2 唯一 approved runtime callable root set

| capability group | path | callable identities that must exist and be frozen | direct dependency classes |
| --- | --- | --- | --- |
| Authorization V2 parse/verify | `runtime/ctde_runtime/authorization_v2.py` | `load_authorization_v2`; `validate_request_binding`; `validate_activated_projection` | `common.py`, `authorization_schema_v2.yaml`, PyYAML, datetime/re/hmac/pathlib |
| Authorization registry | `runtime/ctde_runtime/authorization_registry.py` | `AuthorizationRegistry.register_authorization_v2`; `resolve_preconsume_v2`; `consume_authorization_v2`; `revoke_authorization_v2`; `claim_mint_lease_v2`; `prepare_capability_v2`; `activate_capability_v2`; `abort_mint_eligibility_v2`; `abort_preparation_v2`; `abort_activation_v2`; `validate_context_v2` | `authorization_v2.py`, `common.py`, `events.py`, sqlite3, secrets/uuid/threading |
| Capability issuer | `runtime/ctde_runtime/range_broker.py` | `CapabilityIssuer.validate_preparation_binding_v2`; `build_pending_capability_v2`; `validate_activation_binding_v2` | Registry, V2 contexts, signing, canonical JSON |
| Range broker | `runtime/ctde_runtime/range_broker.py` | `RangeBroker.handle_request`; `validate_authorization_binding_v2`; `deliver` | Registry, events, signing, `fixture_factory.py`, `ctypes.CDLL(None)`, memfd/fcntl/os |
| Bounded reader | `runtime/ctde_runtime/bounded_reader.py` | `BoundedReader.validate_authorization_binding_v2`; `consume` | Registry, broker delivery, sandbox, signing/events, fcntl/os |
| Formal loader | `runtime/ctde_runtime/formal_loader.py` | `FormalLoader.load` | common, signed events/signing, pathlib/os |
| Logical read audit | `runtime/ctde_runtime/read_audit.py` | `ReadAuditAggregator.validate_authorization_correlation_v2`; `create_scope_attestation`; `create_closure_attestation` | events, signing, `fixture_factory.py`, V2 context |
| Logical event channel | `runtime/ctde_runtime/events.py` | `SignedEventLog.append`; `SignedEventLog.verify`; `PortableA1EventLogV2.append`; `PortableA1EventLogV2.verify` | common, signing, pathlib/json/uuid |
| Sandbox/consumer boundary | `runtime/ctde_runtime/sandbox.py` | `SandboxSupervisor.run` | common/events, `bin/consumer_probe`, subprocess, `/proc`, fixed child environment |

规则：

1. policy 中必须逐项写入完整 `module + qualname + relative path`；不能只写“registry”或“broker”。
2. builder 以 AST/symbol inventory 确认 callable 实际存在；缺失或重复 identity 直接 BLOCKED。
3. callable root 只定义 closure 起点，不代表 R3 会调用 source-reading、delivery、sandbox 或 formal-loading paths。
4. production/runtime roots 不包含 `run_suite.py`、`run_r2_portable.py`、任何 fixture spec 或 R3 runner。
5. 新 `run_r3_portable_closure.py::main` 是唯一 R3 test/control runner root，只进入 test/control freeze，不进入 production runtime closure。
6. 当前 callable root set 不是自行缩小验收域的 authority；还必须通过 §3.3 的 formal required-role inventory。
7. 未来任何 R4 executable、manifest builder、runner、verifier、aggregate/report generator、schema、policy 或它们的传递依赖，只要不在本次 freeze 中，当前 closure 对 R4 即失效。R4 执行前必须获得一份新 Plan、新 suite path 和新授权的 fresh R3 refresh；`test-only`、`control` 或 `build-only` 标签都不能绕过该规则。

### 3.3 Formal required-role inventory 与当前明确缺口

`RUNTIME_CAPABILITY_REPAIR_PLAN.md` §4.2 的 role set 是 builder 的第二类强制输入，不能由 closure policy 删除。未来 manifest 必须包含 `required_runtime_roles` 与 `required_runtime_role_gaps`；后者非空时，R3 必须 fail closed。

| formal role | 当前真实 resolution | future classification/result |
| --- | --- | --- |
| Portable Runtime/R4 suite manifest builder | legacy `runtime/build_manifest.py` 只绑定旧 RCPT；R3 test-manifest builder职责不同 | `required_runtime_role_gap`；legacy node=`excluded_dependency`，R3 test builder仅=`build_only_dependency` |
| Portable Runtime/R4 suite runner | legacy `runtime/run_suite.py` 只绑定旧 197-leaf E2E；R3 closure-test runner职责不同 | `required_runtime_role_gap`；legacy node=`excluded_dependency`，R3 runner仅=`test_only_dependency` |
| authorization/issuer/signed object/broker/reader/sandbox/formal loader/audit/signer | §3.2 的现有 callable roots | reachable nodes，按实际 runtime closure 分类 |
| native probe/build input | `bin/consumer_probe` + `native/consumer_probe.c`；现有 build recipe 未独立冻结 | future native build policy补齐 recipe/toolchain/link identity |
| parser scope | 只有 legacy `run_suite.py` 内 synthetic harness logic，没有独立 production callable/file | `required_runtime_role_gap`；不得由 R3 实现或忽略 |
| model gateway | 只有 legacy `run_suite.py` 内 synthetic harness logic，没有独立 production callable/file | `required_runtime_role_gap`；不得调用模型或由 R3 实现 |
| write monitor | 只有 legacy `run_suite.py` 内 logical synthetic harness logic，没有独立 production callable/file | `required_runtime_role_gap`；不得由 R3 实现或冒充 A2 |
| independent artifact/closure verifier | future `runtime/verify_r3_portable_closure.py` | `test_only_dependency`，`member_type=verification_code` |
| Portable Runtime/R4 aggregate/report generator | 仅有legacy `run_suite.py`内旧finalizer；R3 result generator职责不同 | `required_runtime_role_gap`；R3 result generator只以`build_only_dependency`/`member_type=control_generator`冻结 |
| schema/policy/fixture definitions | §2.2 现有contracts/config + §6 future contracts | 按实际runtime/test/build reachability分类 |
| immutable public trust material / key-status registry | 当前只有`signing.py`的in-memory types；key bytes由legacy runner临时生成，没有独立public-key/status asset | `required_runtime_role_gap`；private key只记录key ID/custody boundary，但public key必须最终冻结kid/algorithm/status/domain/validity/public-key bytes SHA-256 |

当前七个production/control role gap是**已明确的功能缺口，不是路径歧义**：Portable Runtime/R4 suite manifest builder、suite runner、aggregate/report generator，parser scope、model gateway、write monitor，以及immutable public trust material/key-status registry。本Plan不获准修复它们。未来R3可以按获批范围完成entrypoint inventory和closure materialization，但只要`required_runtime_role_gaps`非空，最终结果必须是`BLOCKED_PORTABLE_RUNTIME_TRANSITIVE_CLOSURE_FAILED`。Plan-only PASS不预言R3 execution PASS，也不把R3测试工具或private-key custody label冒充Portable Runtime/R4 public trust identity。

## 4. 四个 legacy 文件的唯一 disposition

用户给出的 A/B/C/D 定义在本计划中严格采用：

- A：R3 允许原地修改；
- B：R3 必须保持不变，新建 V2/Portable 对应文件；
- C：仅作为 legacy evidence，不进入新的 Runtime；
- D：实际不存在或与 R3 无关。

| legacy relative path | decision | immutable handling | unique corresponding path / result |
| --- | --- | --- | --- |
| `contracts/component_manifest.yaml` | **B** | 原字节保留；继续绑定旧 `RCPTS-20260811-002`，不得更新五个失配摘要 | `r3_portable_suites/R3PS-20260811-001/control/runtime_transitive_closure_manifest.json` |
| `runtime/build_manifest.py` | **C** | 原字节保留；仅证明旧 RCPT manifest control 的历史身份，不进入 Portable production Runtime | 无 Portable counterpart；新的 closure builder/test-manifest builder 是独立 R3 职责，不伪装为旧 builder V2 |
| `runtime/verify_trace.py` | **C** | 原字节保留；只属于旧 strace/A2/Hardened evidence，不进入 Portable R3 roots | 无 Portable replacement；新的 `runtime/verify_r3_portable_closure.py` 是不同职责，不伪装为 trace verifier V2 |
| `runtime/run_suite.py` | **C** | 原字节保留；仅作为旧 197-leaf E2E 历史 evidence，不进入 Portable production Runtime | 无 Portable counterpart；新的 R3 runner 只运行 closure synthetic tests，不是 R4 E2E runner |

```yaml
legacy_disposition_counts:
  A_mutable_in_place: 0
  B_keep_and_create_corresponding: 1
  C_legacy_evidence_only: 3
  D_absent_or_irrelevant: 0
legacy_disposition_unresolved: 0
```

不存在“实施时再决定”。若未来代码现状使上述任一 disposition 不能成立，正确动作是 `BLOCKED_R3_LEGACY_DISPOSITION_MISMATCH`，不是切换选项继续。

## 5. 唯一 canonical paths

所有路径均相对于项目 workspace root；suite 内 manifest member path 则相对于 `runtime_capability_prototype/`。

| Required artifact | unique canonical path |
| --- | --- |
| 1. Runtime transitive closure manifest | `runtime_capability_prototype/r3_portable_suites/R3PS-20260811-001/control/runtime_transitive_closure_manifest.json` |
| 2. Closure builder | `runtime_capability_prototype/runtime/build_r3_portable_closure.py` |
| 3. Closure verifier | `runtime_capability_prototype/runtime/verify_r3_portable_closure.py` |
| 4. Component freeze artifact | `runtime_capability_prototype/r3_portable_suites/R3PS-20260811-001/control/component_freeze.json` |
| 5a. Execution snapshot closure binding schema | `runtime_capability_prototype/contracts/execution_snapshot_closure_binding_schema_v1.yaml` |
| 5b. Execution snapshot closure binding artifact | `runtime_capability_prototype/r3_portable_suites/R3PS-20260811-001/control/execution_snapshot_closure_binding.json` |
| 6. R3 synthetic test manifest | `runtime_capability_prototype/r3_portable_suites/R3PS-20260811-001/control/r3_synthetic_test_manifest.json` |
| 7. R3 test runner | `runtime_capability_prototype/runtime/run_r3_portable_closure.py` |
| 8. R3 aggregate result | `runtime_capability_prototype/r3_portable_suites/R3PS-20260811-001/aggregate/r3_portable_closure_results.json` |
| 9. R3 evidence root | `runtime_capability_prototype/r3_portable_suites/R3PS-20260811-001/evidence/` |
| 10. R3 final result report | `PORTABLE_RUNTIME_TRANSITIVE_CLOSURE_RESULT.md` |

补充唯一测试路径：

| Test asset | unique path |
| --- | --- |
| requirements | `runtime_capability_prototype/contracts/r3_portable_closure_test_requirements.yaml` |
| pre-authorized implementation manifest | `runtime_capability_prototype/r3_portable_suites/R3PS-20260811-001/control/r3_implementation_manifest.json` |
| fixture catalog | `runtime_capability_prototype/r3_portable_suites/R3PS-20260811-001/fixtures/r3_synthetic_fixtures.json` |
| attempts ledger | `runtime_capability_prototype/r3_portable_suites/R3PS-20260811-001/attempts/r3_attempts.jsonl` |
| start evidence | `runtime_capability_prototype/r3_portable_suites/R3PS-20260811-001/evidence/start/closure_start_verification.json` |
| dynamic evidence | `runtime_capability_prototype/r3_portable_suites/R3PS-20260811-001/evidence/dynamic/dynamic_dependency_observation.json` |
| end evidence | `runtime_capability_prototype/r3_portable_suites/R3PS-20260811-001/evidence/end/closure_end_verification.json` |
| controller terminal ledger | `runtime_capability_prototype/r3_portable_suites/R3PS-20260811-001/evidence/controller_terminal/controller_terminals.jsonl` |
| evidence index | `runtime_capability_prototype/r3_portable_suites/R3PS-20260811-001/evidence/evidence_manifest.json` |
| immutable external closure registry record | `runtime_capability_prototype/r3_portable_suites/R3PS-20260811-001/control/closure_snapshot_registry_record.json` |
| aggregate/report generator | `runtime_capability_prototype/runtime/build_r3_portable_result.py` |

该布局复用现有 `contracts/` 和 `runtime/`，只有 suite evidence 需要一个新的 `r3_portable_suites/` 根。它不是第二个 Runtime implementation tree。

## 6. `r3_write_scope`

### 6.1 `mutable_existing_files`

```yaml
mutable_existing_files: []
mutable_existing_files_count: 0
```

未来 R3 不获得任何现有文件的写权限。不存在因“integration”而默认允许的小改动。

### 6.2 `creatable_files`

以下 31 个 path 是未来 R3 唯一允许创建的持久文件。除这些精确 path 外，default deny。

```text
runtime_capability_prototype/contracts/r3_portable_closure_policy_v1.yaml
runtime_capability_prototype/contracts/runtime_transitive_closure_manifest_schema_v1.yaml
runtime_capability_prototype/contracts/component_freeze_schema_v1.yaml
runtime_capability_prototype/contracts/execution_snapshot_closure_binding_schema_v1.yaml
runtime_capability_prototype/contracts/r3_portable_closure_test_requirements.yaml
runtime_capability_prototype/contracts/r3_portable_test_manifest_schema_v1.yaml
runtime_capability_prototype/contracts/r3_portable_controller_terminal_schema_v1.yaml
runtime_capability_prototype/contracts/native_component_build_policy_v1.yaml
runtime_capability_prototype/contracts/closure_snapshot_registry_record_schema_v1.yaml
runtime_capability_prototype/contracts/r3_portable_closure_control_artifact_schema_v1.yaml
runtime_capability_prototype/runtime/build_r3_portable_closure.py
runtime_capability_prototype/runtime/build_r3_portable_test_manifest.py
runtime_capability_prototype/runtime/verify_r3_portable_closure.py
runtime_capability_prototype/runtime/run_r3_portable_closure.py
runtime_capability_prototype/runtime/build_r3_portable_result.py
runtime_capability_prototype/r3_portable_suites/R3PS-20260811-001/control/r3_implementation_manifest.json
runtime_capability_prototype/r3_portable_suites/R3PS-20260811-001/control/r3_execution_plan.json
runtime_capability_prototype/r3_portable_suites/R3PS-20260811-001/control/runtime_transitive_closure_manifest.json
runtime_capability_prototype/r3_portable_suites/R3PS-20260811-001/control/r3_synthetic_test_manifest.json
runtime_capability_prototype/r3_portable_suites/R3PS-20260811-001/control/component_freeze.json
runtime_capability_prototype/r3_portable_suites/R3PS-20260811-001/control/execution_snapshot_closure_binding.json
runtime_capability_prototype/r3_portable_suites/R3PS-20260811-001/control/closure_snapshot_registry_record.json
runtime_capability_prototype/r3_portable_suites/R3PS-20260811-001/fixtures/r3_synthetic_fixtures.json
runtime_capability_prototype/r3_portable_suites/R3PS-20260811-001/attempts/r3_attempts.jsonl
runtime_capability_prototype/r3_portable_suites/R3PS-20260811-001/evidence/start/closure_start_verification.json
runtime_capability_prototype/r3_portable_suites/R3PS-20260811-001/evidence/dynamic/dynamic_dependency_observation.json
runtime_capability_prototype/r3_portable_suites/R3PS-20260811-001/evidence/end/closure_end_verification.json
runtime_capability_prototype/r3_portable_suites/R3PS-20260811-001/evidence/controller_terminal/controller_terminals.jsonl
runtime_capability_prototype/r3_portable_suites/R3PS-20260811-001/evidence/evidence_manifest.json
runtime_capability_prototype/r3_portable_suites/R3PS-20260811-001/aggregate/r3_portable_closure_results.json
PORTABLE_RUNTIME_TRANSITIVE_CLOSURE_RESULT.md
```

`attempts.jsonl` 与 `controller_terminals.jsonl` 可以由唯一 R3 controller append；它们不能由 leaf worker、Runtime module 或 verifier 直接写。其他 control/evidence/aggregate 文件为 create-once immutable artifacts。31 个文件中，前 15 个 contracts/scripts 是 pre-authorized implementation bundle，后 16 个是由唯一 controller 按 §13 stage contract 物化的 control/evidence/result artifacts。

### 6.3 `creatable_directories`

```text
runtime_capability_prototype/r3_portable_suites/
runtime_capability_prototype/r3_portable_suites/R3PS-20260811-001/
runtime_capability_prototype/r3_portable_suites/R3PS-20260811-001/control/
runtime_capability_prototype/r3_portable_suites/R3PS-20260811-001/fixtures/
runtime_capability_prototype/r3_portable_suites/R3PS-20260811-001/attempts/
runtime_capability_prototype/r3_portable_suites/R3PS-20260811-001/evidence/
runtime_capability_prototype/r3_portable_suites/R3PS-20260811-001/evidence/start/
runtime_capability_prototype/r3_portable_suites/R3PS-20260811-001/evidence/dynamic/
runtime_capability_prototype/r3_portable_suites/R3PS-20260811-001/evidence/end/
runtime_capability_prototype/r3_portable_suites/R3PS-20260811-001/evidence/controller_terminal/
runtime_capability_prototype/r3_portable_suites/R3PS-20260811-001/aggregate/
```

`contracts/`、`runtime/` 与 workspace root 已存在，不计入 creatable directory。

### 6.4 临时 synthetic shadow trees

Tamper tests 只能在 runner 创建的 OS temporary directory 中复制**manifest 已列的 closure member bytes**并做 synthetic mutation。临时目录不得：

- 位于 project workspace、`source/`、`analysis_candidate/` 或任何 suite evidence root；
- 复制整个 workspace；
- 包含 TEI、Candidate artifact、Registry live DB、private key、sealed slice 或业务输出；
- 在测试完成后被报告为 Runtime artifact。

临时目录不是持久 `creatable_files`。若 runner 无法保证仅复制 manifest member set，R3 必须 BLOCKED。

### 6.5 唯一 writer/producer authority

Path 唯一还不够；下表同时冻结每个 artifact class 的唯一 producer。除 controller 外，builder、verifier 与 leaf worker 均不得直接写 project tree。

| persistent artifact(s) | sole producer | write contract |
| --- | --- | --- |
| §6.2 前 15 个 contracts/scripts | 获得人工 R3 实施授权的 implementation materializer | 先在 OS temp 构造完整 bundle；exact path/digest 写入 implementation manifest；只允许 create-new，不允许覆盖 |
| `control/r3_implementation_manifest.json` | implementation materializer | exact bytes SHA-256 必须预先记录在人工授权；先 create-once 提交，作为 partial materialization 的恢复 authority |
| `control/r3_execution_plan.json` | `run_r3_portable_closure.py bootstrap` | 仅在 15 个 implementation file 全部匹配 implementation manifest 后 create-once |
| closure manifest | `build_r3_portable_closure.py --phase manifest` 生成 canonical bytes；`run_r3_portable_closure.py` 唯一持久写入 | phase 1只返回manifest，不生成freeze/binding，不写project tree |
| R3 test manifest + fixture catalog | `build_r3_portable_test_manifest.py` 生成；controller 持久写入 | 输入为phase-1 frozen closure manifest bytes与requirements；不固定leaf count |
| component freeze + snapshot binding | `build_r3_portable_closure.py --phase bind-control` 生成canonical bytes；controller持久写入 | phase 2以manifest + test manifest + fixture catalog exact digests为输入；不得重算/改变manifest |
| external closure registry record | controller 的独立 registry-record pass | 从已提交 closure/freeze/binding exact bytes重新 hash；closure builder不得生成或回写该 record |
| start/end verification evidence | `verify_r3_portable_closure.py` 生成只读 verification payload；controller 持久写入 | verifier不写其他路径，不修改被验对象 |
| dynamic observation、attempts、controller terminal | controller | attempts/terminal仅append；dynamic evidence create-once |
| evidence manifest、aggregate、final report | `build_r3_portable_result.py` 生成；controller依次持久写入 | generator只返回canonical bytes；final report不得手写或由closure builder生成 |

`r3_portable_closure_control_artifact_schema_v1.yaml` 是一个以 `artifact_class` 判别的 closed union schema，唯一覆盖 implementation manifest、execution plan、fixture catalog、attempt record、start/dynamic/end evidence、evidence manifest 与 aggregate；不得在实施时再为同一 artifact另起竞争 schema/layout。

### 6.6 Scope key binding

```yaml
read_only_files:
  exact_set: "the 62 existing files enumerated by §2.2 + §2.3 + §1.1 + §7.1"
  modification_allowed: false
forbidden_paths:
  exact_groups: "R3-FG-01 through R3-FG-09 in §7.3"
  default_deny_outside_creatable_scope: true
```

上述section引用是closed reference：§7.1已列出额外Source/Run文件的exact path，§2.2/§2.3/§1.1已逐项列出其余existing files，§7.3逐组列出forbidden path expression。实施时不得以复制一份不同列表制造第二authority。

## 7. Read-only protected assets 与 forbidden paths

### 7.1 62 个明确 protected files

未来 R3 必须保持以下 62 个文件内容只读：

1. §2.2 的 34 个直接 R3 相关现有文件；
2. §2.3 的 9 个历史/R2 evidence 文件；
3. §1.1 的 6 个正式依据文件；
4. 本 `PORTABLE_RUNTIME_TRANSITIVE_CLOSURE_PLAN.md`；
5. 下列8个Source Layer files；
6. 下列4个Run 001/002 historical files。

Source Layer path只通过directory-entry inventory确认存在；本阶段没有打开或hash其内容。未来R3对全部8项既no-write又no-content-read：

```text
source/metadata/checksums/checksums.sha256
source/metadata/logs/acquisition_log.jsonl
source/metadata/quality/source_quality_report.md
source/metadata/records/ody-eng-murray1919-raw-full-tei.source.yaml
source/metadata/records/ody-grc-murray1919-raw-full-tei.source.yaml
source/metadata/sources.yaml
source/original_text/grc/ody-grc-murray1919/raw/ody-grc-murray1919__raw__full.xml
source/translations/en/ody-eng-murray1919/raw/ody-eng-murray1919__raw__full.xml
```

Run 001/002 historical files：

```text
CANDIDATE_RUN_001_PLAN.md
CANDIDATE_RUN_002_PLAN.md
analysis_candidate/runs/AC-20260811-STORYSTRUCT-001/execution_report.md
analysis_candidate/runs/AC-20260811-STORYSTRUCT-001/run_manifest.yaml
```

Run 002 reserved root当前不存在；absence本身受§7.3保护，R3不得创建或占用。

这里的 read-only 不等于全部排除：现有 Runtime/R2 V2 files 可以作为 closure members 被读取、hash 和解析，但不得修改。历史 evidence 只能引用摘要，不得成为 active runtime code。

### 7.2 R2 assets 的特殊保护

以下 16 个 R2 implementation assets 是未来 R3 的 immutable upstream baseline：

```text
runtime_capability_prototype/contracts/authorization_schema_v2.yaml
runtime_capability_prototype/contracts/authorization_registry_record_schema_v2.yaml
runtime_capability_prototype/contracts/authorization_registry_event_schema_v2.yaml
runtime_capability_prototype/contracts/r2_portable_controller_terminal_schema_v1.yaml
runtime_capability_prototype/contracts/capability_claims_schema_v2.yaml
runtime_capability_prototype/contracts/broker_envelope_schema_v2.yaml
runtime_capability_prototype/contracts/audit_attestation_schema_v2.yaml
runtime_capability_prototype/runtime/ctde_runtime/authorization_v2.py
runtime_capability_prototype/contracts/r2_portable_authorization_test_requirements.yaml
runtime_capability_prototype/runtime/build_r2_portable_manifest.py
runtime_capability_prototype/runtime/run_r2_portable.py
runtime_capability_prototype/runtime/ctde_runtime/authorization_registry.py
runtime_capability_prototype/runtime/ctde_runtime/range_broker.py
runtime_capability_prototype/runtime/ctde_runtime/bounded_reader.py
runtime_capability_prototype/runtime/ctde_runtime/read_audit.py
runtime_capability_prototype/runtime/ctde_runtime/events.py
```

未来 R3 对它们只允许：

- 真实 SHA-256 复算；
- AST/import/config/schema dependency discovery；
- 作为 runtime、test-only 或 build-only node 分类；
- no-content import/load observation；
- 与 R2 result/component-input baseline 比较。

若发现真正的 R2 defect、缺失 R2 semantic contract 或必须修改上述任一文件：

```text
BLOCKED_R3_UPSTREAM_R2_DEFECT
```

R3 不得修复、patch、monkeypatch 持久文件、改变 R2 历史 PASS 或把 defect 记为 deferred。

### 7.3 九个 forbidden path groups

以下 path group 在未来 R3 中禁止创建、修改、删除、移动、复制、链接或作为 synthetic input 读取：

| Group | forbidden paths | reason |
| --- | --- | --- |
| `R3-FG-01` | `source/**` | Odyssey Source Layer；包含 English/Greek TEI 与 metadata/translations |
| `R3-FG-02` | `analysis_candidate/**` | existing Run 001、absent-but-reserved Run 002 root、future Candidate runs |
| `R3-FG-03` | `runtime_capability_prototype/suites/**` | legacy RCPTS suites/evidence immutable |
| `R3-FG-04` | `runtime_capability_prototype/r2_portable_suites/**` | completed R2 suite/evidence immutable |
| `R3-FG-05` | `runtime_capability_prototype/registry/**` | V1/R2 live or historical mutable Registry state；R3 不在此建第二 registry |
| `R3-FG-06` | `runtime_os_observability_preflight/**`、OS preflight/matrix artifacts、`runtime_capability_prototype/r3_hardened_suites/**`、任何Hardened/A2/A3 certification artifact root | Hardened artifacts全部deferred/forbidden |
| `R3-FG-07` | `runtime_capability_prototype/r4_portable_suites/**` 及任何 R4 artifact | R4 deferred；R3 不预创建 R4 |
| `R3-FG-08` | `**/story_structure.yaml`、人物/事件/主题/改编/分集/场景/对白/剧本 output roots | literary/business output forbidden |
| `R3-FG-09` | 除 §6.2/§6.3 外的所有 workspace path | closed write set / default deny |

Builder 可以对 §7.3 中的 legacy path group 读取**目录名和显式 protected file 摘要**以证明 exclusion；它不得递归扫描文件内容。`source/**` 与 `analysis_candidate/**` 完全不进入 builder traversal roots。

## 8. Future closure builder 的唯一合同

### 8.1 唯一输入

`runtime/build_r3_portable_closure.py` 只接受下列显式输入：

```yaml
prototype_root: "runtime_capability_prototype"
suite_id: "R3PS-20260811-001"
execution_plan: "r3_portable_suites/R3PS-20260811-001/control/r3_execution_plan.json"
implementation_manifest: "r3_portable_suites/R3PS-20260811-001/control/r3_implementation_manifest.json"
closure_policy: "contracts/r3_portable_closure_policy_v1.yaml"
native_build_policy: "contracts/native_component_build_policy_v1.yaml"
closure_schema: "contracts/runtime_transitive_closure_manifest_schema_v1.yaml"
approved_runtime_entrypoints: "the exact callable root set in §3.2, materialized in closure_policy"
formal_required_runtime_roles: "the non-removable role inventory in §3.3, materialized in closure_policy"
canonical_contracts:
  - "contracts/authorization_schema_v2.yaml"
  - "contracts/authorization_registry_record_schema_v2.yaml"
  - "contracts/authorization_registry_event_schema_v2.yaml"
  - "contracts/capability_claims_schema_v2.yaml"
  - "contracts/broker_envelope_schema_v2.yaml"
  - "contracts/audit_attestation_schema_v2.yaml"
configuration_inputs:
  - "contracts/r3_portable_closure_policy_v1.yaml"
  - "contracts/native_component_build_policy_v1.yaml"
```

`r3_implementation_manifest.json` 先冻结 15 个 implementation file 的 exact path/size/SHA-256、Plan external digest、suite ID 与 bundle digest；其 exact file SHA-256 必须由人工 R3 授权在任何 project-tree write 前外部记录。全部 15 个文件匹配后，controller 才创建 `r3_execution_plan.json`，冻结 Profile、Plan digest、implementation-manifest digest、suite ID、fixed `generated_at`、write/read/forbidden scope、builder/test-builder/verifier/runner/result-generator digests、R2 baselines 与 environment policy。`generated_at` 由 execution plan 供给，不读取 wall clock；相同输入才可重现 identical canonical bytes。

### 8.2 唯一 builder 两相输出合同

Closure builder不具有project-tree写权限。为避免closure manifest与test control freeze形成生成环，同一个builder具有两个closed subcommand；没有第三种mode：

1. `--phase manifest`：只从§8.1 entrypoints/policy/runtime inputs生成`runtime_transitive_closure_manifest.json` canonical bytes。Controller在两个independent temp build exact-match且verifier PASS后create-once提交manifest。
2. Test-manifest builder以已提交且digest匹配的closure manifest为输入，只在temp生成R3 test manifest与fixture catalog；controller验证后create-once提交。
3. `--phase bind-control`：读取已提交manifest、test manifest、fixture catalog和全部control exact digests，只生成`component_freeze.json`与`execution_snapshot_closure_binding.json` canonical bytes；它必须引用phase-1 manifest exact digest，不得重建或改变manifest。Controller在两个temp build exact-match且verifier PASS后create-once提交二者。

因此单向生成顺序唯一为：

```text
closure manifest -> test manifest + fixture catalog -> component freeze -> snapshot binding
```

每个phase的第二次reproducibility build只输出到另一个OS temporary directory；不得在project tree建立第二个manifest、freeze或binding。External registry record由§6.5独立registry-record pass生成，不属于builder输出。

### 8.3 明确禁止的扫描/输入行为

Builder 不得：

- 以 workspace root 作为递归扫描根；
- 递归扫描 `source/`、`analysis_candidate/`、legacy suites、R2 suites 或 Registry；
- stat/open/hash/parse/copy English 或 Greek TEI；
- 读取 `book_structure_map.yaml`；
- 根据文件扩展名把整个 workspace 无差别纳入 closure；
- 把 mtime、inode 或目录遍历顺序作为 content identity；
- 跟随未在 policy 中批准的 symlink；当前 Runtime symlink count 为 0，未来出现任何 symlink 必须显式解析或 BLOCKED；
- 执行 `run_suite.py`、`run_r2_portable.py`、`verify_trace.py`、broker source open/read、bounded delivery、sandbox probe、formal loader 或模型接口；
- 将 unknown/unresolved dependency 改成 ignored。

## 9. Closure discovery 与 classification 算法

### 9.1 静态 discovery

Builder 必须对 approved roots 执行版本化 AST discovery：

1. 解析 `import` / `from ... import`，递归解析 project-owned module；
2. 自动加入每一级 package initializer；
3. 解析 module-level constant、literal `Path`、schema/config/policy path 与 native binary path；
4. 解析 callable body 中的 project-owned function/class references；
5. 扫描 `importlib`、`__import__`、plugin/entry-point lookup、config-driven module name；
6. 扫描 `subprocess.run/Popen/call/check_*`、`os.system`、`shell=True` 与 executable argument；
7. 扫描 `ctypes.CDLL/PyDLL`、shared-library load、extension module origin；
8. 扫描 `open/read_text/read_bytes/load_yaml` 等 code/config/schema path-based load；
9. 扫描 `os.getenv/os.environ`、cwd、locale、timezone、hash seed 与其他 environment-derived semantics；
10. 扫描 native build input、compiler、flags、link mode 与 binary output identity。

静态 scanner 自身必须有 test vectors，并由 verifier 用独立 parser pass 复核。仅把当前已知四个漏项手工追加不是合格算法。

### 9.2 No-content dynamic observation

R3 runner 只允许执行 no-content closure probe：

- import approved runtime modules；
- verify callable identities；
- exercise V2 pure parse/binding paths with synthetic non-literary bytes；
- 使用 Python audit hook 或等价 A1 mechanism 记录 module import origin、code/config open、`subprocess.Popen` intent、`ctypes.dlopen` 与 executable resolution；
- 对不会在 R3 调用的 source-read/delivery/sandbox branches，使用静态解析 + explicit allowlist 解析依赖，不能以“未观察到”当作不存在；
- dynamic observation evidence 只声明 A1，不声称完整 OS open set。

所有 Python control/probe process 必须使用 execution plan中冻结的 exact interpreter，以 isolated/no-bytecode mode启动（至少 `-I -B`）；`PYTHONDONTWRITEBYTECODE=1`，任何允许的 cache/temp prefix只能指向本次 OS temporary directory。cwd、`sys.path`、locale、timezone、hash seed、user-site禁用、approved environment allowlist都必须冻结。不得在现有 `runtime/`、workspace或任何 protected tree生成 `__pycache__`、`.pyc`、coverage、tool cache或日志；发现一个即为 scope violation并fail closed。

当前只读审计已发现的必须分类项包括：

| discovered site | future required resolution |
| --- | --- |
| `range_broker.py: ctypes.CDLL(None)` | platform boundary；解析实际 process C runtime/loader identity，不能写 `system/current` |
| `sandbox.py: subprocess.Popen([probe_binary])` | project-owned runtime member `bin/consumer_probe` + external process/platform boundary |
| `sandbox.py: /proc/<pid>/*` | platform boundary；Portable 只冻结依赖，不声明 A2 coverage |
| `authorization_v2.py: load_yaml(schema_path)` | config/schema edge必须只解析到 canonical `authorization_schema_v2.yaml` |
| `run_suite.py: gcc ...` | legacy entrypoint不可达；gcc 不得因 legacy reachability进入 runtime closure |
| `verify_trace.py: strace ... /bin/true` | legacy/Hardened excluded；strace 与 `/bin/true` 不得进入 Portable runtime closure |
| native reproducibility build | gcc/compiler/linker 作为 build-only platform boundary，由 `native_component_build_policy_v1.yaml` 唯一批准；只在 temp dir输出，不覆盖 `bin/consumer_probe` |

任何 dynamic dependency 只有三种合法结果：

1. project-owned exact file 成为 closure member；
2. external dependency 成为 exact platform boundary；
3. 证明从 approved roots 不可达并成为 explicit exclusion。

其他结果一律：

```text
BLOCKED_RUNTIME_TRANSITIVE_CLOSURE_INCOMPLETE
```

### 9.3 五类唯一 classification

| classification | 规则 | freeze handling |
| --- | --- | --- |
| `runtime_closure_member` | 从 §3.2 runtime roots 经 import/call/config/schema/binary edge 实际可达的 project-owned bytes，或显式 canonical runtime contract | 进入 production/runtime payload；完整 file bytes digest |
| `test_only_dependency` | 只从 R3 test runner/test manifest/fixture/controller roots可达，production roots不可达 | 进入 control/test freeze，不进入 production runtime member set |
| `build_only_dependency` | 只影响生成/编译/验证构建，不在 Runtime execution 中加载 | 进入 build freeze；记录 source/recipe/tool/output edge |
| `platform_boundary` | interpreter、relevant stdlib、third-party distribution、libc/loader/kernel/proc、external compiler/executable | exact可复核 fingerprint；identity mismatch fail closed |
| `excluded_dependency` | 从所有 approved roots不可达且 policy 明确禁止/历史化的文件或 path group | 记录 exclusion reason与reachability proof；若实际可达即 reject |

优先级规则：**reachability 优先于文件名和作者意图**。一个叫 fixture/helper/test 的文件只要从 runtime roots import，就不能放在 test-only。`fixture_factory.py` 当前因此属于 runtime member候选；`fixture_specs/synthetic_book1_fixture.yaml` 才是 test-only。

Manifest 不允许 `unknown` member class。无法分类的 dependency 进入 `unresolved_dependencies`；该数组非空时 verifier 必须失败。

`member_type` 与 `classification` 是两个正交字段。`member_type` 使用独立 closed vocabulary（例如 `project_source`、`native_source`、`native_binary`、`contract_schema`、`runtime_policy`、`control_generator`、`verification_code`、`fixture_definition`、`public_trust_material`、`platform_boundary`）；它不能作为第六种 classification。Schema 和 verifier 必须拒绝把 `verification_code` 或 `control_generator` 写进 classification 字段。

### 9.4 Test runner/helper 的边界

以下 production/runtime 不实际依赖的控制文件不得进入 production runtime closure：

- `runtime/run_r2_portable.py`；
- `runtime/build_r2_portable_manifest.py`；
- 新 `runtime/run_r3_portable_closure.py`；
- 新 `runtime/build_r3_portable_test_manifest.py`；
- 新 `runtime/build_r3_portable_result.py`；
- R2/R3 requirements、fixtures、attempts、controller ledger；
- `runtime/verify_r3_portable_closure.py`。

它们仍由 component freeze 以 `test_only_dependency` 或 `build_only_dependency` classification冻结；verifier使用独立的 `member_type=verification_code`。若 production roots实际import它们，verifier必须输出 `BLOCKED_TEST_ONLY_DEPENDENCY_REACHABLE`，不得把它们静默升级后仍宣称classification correct。

## 10. Canonical manifest 与 component freeze

### 10.1 Manifest schema

`runtime_transitive_closure_manifest.json` 至少包含：

```yaml
manifest_schema_version: "1.0.0"
artifact_class: "ctde_portable_runtime_transitive_closure"
assurance_profile_id: "CTDE-PORTABLE-DEV-1"
highest_claimed_evidence_level: "A1"
a2_os_file_access_proof: "NOT_PROVIDED"
hardened: false
certified: false
closure_id: "CTDE-PORTABLE-RUNTIME-CLOSURE-R3PS-20260811-001"
generated_at: "<fixed value from r3_execution_plan.json>"
entrypoints: []
required_runtime_roles: []
required_runtime_role_gaps: []
members: []
dependency_edges: []
dynamic_dependency_resolution: []
platform_boundaries: []
exclusions: []
unresolved_dependencies: []
closure_algorithm: {}
closure_payload_sha256: "<digest excluding only this field>"
```

每个 entrypoint 至少记录：`entrypoint_id`、relative path、module、qualname、callable/executable kind、file SHA-256、direct dependency IDs、classification。

每个 member 至少记录：stable member ID、member type、classification、canonical relative path或external origin、size、SHA-256、origin/kind、reason、direct edges。Project path必须是 prototype-root-relative POSIX path；拒绝绝对 project path、`..`、重复 identity、case alias和symlink ambiguity。

每条 edge 稳定排序为 `(from_id, to_id, relation, locator)`；relation 使用 closed vocabulary，例如 `imports`、`loads_schema`、`loads_config`、`calls`、`executes`、`dlopens`、`builds_from`、`verifies`、`classified_by`。

### 10.2 Canonicalization 与 reproducibility

Canonical JSON 规则：

1. UTF-8，无 BOM；
2. JSON object keys Unicode code-point order；
3. arrays 先按各自 stable ID/order contract排序；
4. 禁止 float、NaN、Infinity、duplicate key和schema外字段；
5. compact separators，无多余 whitespace；
6. exact bytes以单个 LF结束；
7. `closure_payload_sha256` 的输入是删除该字段后的完整 canonical object bytes；
8. manifest exact file SHA-256 不写回 manifest，由 `component_freeze.json` 外部保存；
9. `generated_at` 为 execution plan fixed input，因此 identical inputs 可生成 identical manifest bytes。

两次独立 temp build 的 canonical payload、payload SHA-256 与完整 manifest bytes必须全部相同。只比较 node count 不构成 reproducibility。

### 10.3 Component freeze 覆盖范围

`component_freeze.json` 必须覆盖：

- 所有 `runtime_closure_member`；
- Authorization Schema V2 identity；
- Registry implementation；
- authorization loader/validator；
- capability issuer/range broker；
- bounded reader；
- formal loader；
- logical read audit、events、signing；
- semantics-affecting configuration/schema；
- package initializer/shared module；
- native binary及 source→build policy→toolchain→binary binding；
- interpreter、relevant stdlib origins、PyYAML/cryptography distribution identity；
- libc/loader/kernel/proc 等 relevant platform boundary；
- 所有实际可达public trust records的kid、algorithm、status、trust domain、validity、public-key bytes exact SHA-256；若独立public trust/key-status asset缺失则保留required-role gap并禁止PASS；
- R3 closure builder、test-manifest builder、verifier、runner、aggregate/report generator、全部R3 schemas/policies、implementation manifest、execution plan与frozen test manifest/fixture catalog，按control classification分区；
- canonical manifest exact file SHA-256 与 payload SHA-256。

Known legacy gaps `runtime/build_manifest.py`、`runtime/verify_trace.py`、`runtime/run_suite.py` 和旧 `contracts/component_manifest.yaml` 必须作为 `excluded_dependency` nodes进入 canonical graph并由 freeze记录当前 exact digest与不可达证明；它们不进入production member set。`common.py` 与 package initializer必须作为真实 runtime closure members。这样 `P2GR-R3-002` 不能被“portable”标签静默跳过，也不会把legacy code重新激活。

只冻结顶层 Python 文件、只列当前已知四个漏项、只保存 12/12 digest match 均不能 PASS。

### 10.4 External identity chain

为避免 self-digest：

```text
closure manifest
  -- exact file SHA-256 stored by --> component_freeze.json
component_freeze.json
  -- exact file SHA-256 stored by --> execution_snapshot_closure_binding.json
execution_snapshot_closure_binding.json
  -- closure/freeze/binding exact SHA-256 independently recomputed into --> closure_snapshot_registry_record.json
closure_snapshot_registry_record.json
  -- exact file SHA-256 stored by --> r3_portable_closure_results.json
r3_portable_closure_results.json
  -- exact file SHA-256 reported externally in --> PORTABLE_RUNTIME_TRANSITIVE_CLOSURE_RESULT.md delivery metadata
```

`closure_snapshot_registry_record.json` 是 suite 内但在 closure snapshot 外部的独立、create-once identity record：由 controller 的 registry-record pass从已提交 bytes重新计算，不由 closure builder提供值，不可回写，并由 verifier再次独立复算。它至少绑定 record schema identity、Profile、Plan/implementation/execution-plan identities、closure ID/payload/file digest、freeze digest、binding digest、size与controller sequence；不含自身摘要。`evidence_manifest.json`不包含自身摘要；aggregate外部保存它与registry record的exact digest。Final report不把自身摘要写入正文。

## 11. Execution snapshot closure binding

`execution_snapshot_closure_binding.json` 是 R3 的最远 integration point。它只证明 future execution snapshot **可以**绑定 closure identity；它不是 R4/Candidate execution snapshot，也不授权 source handling。

至少必须绑定：

```yaml
schema_version: "1.0.0"
artifact_class: "ctde_execution_snapshot_closure_binding"
assurance_profile_id: "CTDE-PORTABLE-DEV-1"
highest_claimed_evidence_level: "A1"
a2_os_file_access_proof: "NOT_PROVIDED"
hardened: false
certified: false

closure_id: "CTDE-PORTABLE-RUNTIME-CLOSURE-R3PS-20260811-001"
closure_payload_sha256: "<manifest payload digest>"
closure_manifest_file_sha256: "<manifest exact bytes digest>"
component_freeze_file_sha256: "<freeze exact bytes digest>"

authorization_schema_v2_sha256: "<actual>"
authorization_registry_implementation_sha256: "<actual>"
authorization_validator_sha256: "<actual>"
range_broker_sha256: "<actual>"
bounded_reader_sha256: "<actual>"
formal_loader_sha256: "<actual>"
logical_read_audit_sha256: "<actual>"
events_sha256: "<actual>"
signing_sha256: "<actual>"
public_trust_records:
  - kid: "<actual>"
    algorithm: "EdDSA/Ed25519"
    status: "<actual>"
    trust_domain: "<actual>"
    not_before: "<actual>"
    expires_at: "<actual>"
    public_key_bytes_sha256: "<actual>"
runtime_configuration_digests: []
platform_boundary_identity_sha256: "<canonical boundary payload digest>"

portable_to_hardened_promotion_allowed: false
r4_execution_authorized: false
candidate_run_authorized: false
```

未来 R4/Candidate snapshot 若引用不同 closure ID/digest、不同 member identity 或新 production file，必须在执行前拒绝。Portable binding不能追加A2或改 Profile后晋级 Hardened；Hardened必须 fresh R3-H re-materialization。

## 12. Deterministic synthetic verification 计划

### 12.1 唯一测试资产位置

§5 已冻结 requirements、manifest、runner、fixtures、attempts、start/dynamic/end evidence、controller ledger、evidence index 与 aggregate 的唯一位置。不存在第二个测试布局。

Fixture catalog 只记录 synthetic mutation recipes和expected blocker；不保存 project member副本。实际 tamper只发生在 ephemeral shadow tree。

### 12.2 测试数量规则

本 Plan 不声明固定 leaf 数。`r3_portable_closure_test_requirements.yaml` 只定义 requirement categories和vector source；`build_r3_portable_test_manifest.py` 在 R3 execution 中动态展开 frozen leaves。

设 manifest 实际 leaf count 为 `N`：

```yaml
manifest_leaf_count: N
runner_discovered: N
runner_executed: N
terminal_results: N
evidence_complete: N
passed: N
failed: 0
skipped: 0
unknown: 0
timeout: 0
duplicate_leaf_ids: 0
duplicate_attempt_ids: 0
```

`N` 只能来自 frozen test manifest 与 runner actual terminal records；不能使用本 Plan category数、旧 197 或 R2 51 代替。

### 12.3 Mandatory requirement categories

未来 requirements 至少覆盖以下类别，但 builder可以按真实 dependency/member/vector展开多个 leaf：

| Requirement category | minimum synthetic vectors |
| --- | --- |
| valid closure | valid frozen closure accepted |
| entrypoint integrity | entrypoint missing；entrypoint digest tamper |
| member integrity | dependency/member missing；digest tamper |
| canonical schema | Authorization Schema V2 tamper |
| validator identity | authorization validator mismatch |
| Registry identity | Registry implementation tamper |
| dynamic dependency | missing；changed；unresolved dynamic target |
| unknown dependency | unknown import/load/executable rejected |
| executable allowlist | unexpected executable rejected |
| runtime file allowlist | unexpected project runtime file/reachable byte rejected |
| closure payload | payload digest mismatch rejected |
| execution binding | wrong closure ID/digest rejected |
| exclusion reachability | excluded-but-reachable dependency rejected |
| classification | true test-only dependency absent from production runtime closure |
| platform boundary | interpreter/distribution/libc/kernel/native identity mismatch rejected |
| reproducibility | identical inputs reproduce identical canonical payload and exact bytes |
| path safety | `..`、absolute project path、duplicate identity、symlink ambiguity rejected |
| control-plane freeze | builder/verifier/runner/schema tamper rejected |
| environment semantics | unapproved environment-derived behavior rejected |
| start/end freeze | member change between start/end invalidates suite |

不得为取得 PASS 删除 vector、减少 manifest leaf 或把 expected rejection变成 ignored。

### 12.4 Evidence completeness

每个 leaf terminal 必须绑定：suite ID、manifest digest、attempt ID、fixture vector ID、expected/actual result、exact blocker、before/after side-effect counts、controller sequence、previous terminal digest和相关 evidence IDs。

`evidence_manifest.json` 必须从实际创建的 fixed evidence files枚举 path/size/SHA-256；禁止手写 expected list冒充实际存在。Append-only `controller_terminals.jsonl` 使用截至`END_VERIFIED` terminal的sealed prefix identity（exact byte length、last sequence、prefix SHA-256），不把随后追加的`FINALIZED` terminal伪装成manifest已覆盖。Tamper shadow payload、private key、TEI、Candidate/business output不得持久化。

## 13. Future R3 hard Gate 与 resume contract

### 13.1 Gate G0：任何 project-tree write 前

Bootstrap 不能依赖尚不存在的 controller。未来实施者必须先在 OS temporary directory准备 15-file implementation bundle与 `r3_implementation_manifest.json` canonical bytes；人工执行授权先外部记录该 manifest exact SHA-256。随后 G0 必须逐项 PASS：

1. 本 Plan 的 `final_status=PASS_PORTABLE_R3_PLAN_ONLY`；
2. 本 Plan exact file SHA-256 已由人工 R3执行授权记录；
3. 人工授权明确引用本 Plan digest、`R3PS-20260811-001`、§6 closed scope和precomputed implementation-manifest digest；
4. `mutable_existing_files=[]`，所有 §7 protected R2/legacy/正式依据基线摘要匹配；
5. 全部 31 个 creatable files与11个directories当前不存在，或严格满足§13.3 resume contract；
6. canonical Authorization Schema V2 digest等于 `f1d7c2e36e0d3072624609591eb8dfc20d0e42dce6accc8e87de730ec4478e33`；
7. R2 Implementation Result digest等于 `b47c7280880af70325a5e5c45426951567390441ad4cd61465724fbb8eabcd06`，R2结果仍为`PASS_PORTABLE_AUTHORIZATION_SCHEMA_V2_IMPLEMENTED`且Profile为Portable/A1/non-certified；
8. forbidden path groups未进入write set、traversal roots、fixture inputs、temp-copy source或cache path；
9. 四个legacy disposition为§4唯一B/C/C/C，未决项为0；
10. unresolved path ambiguity为0，没有两个竞争manifest/builder/verifier/runner/evidence/registry/result layouts；
11. current Runtime baseline由实际重新枚举，不用本Plan的`3062`或tree digest替代；
12. implementation bundle恰为§6.2前15个path，manifest中无额外、缺失、绝对、`..`或symlink path；
13. no-content/TEI prohibition能在任何Runtime/source open前机械验证；
14. 人工R3执行授权明确授权的是本Plan，不是旧Repair Plan中的自然语言目标或旧suite。

任一项失败，任何R3持久写均禁止，状态为`BLOCKED_PORTABLE_R3_EXECUTION_GATE_FAILED`；若原因是path/legacy/write scope不唯一，使用`BLOCKED_R3_SCOPE_AMBIGUOUS`。

### 13.2 Gate G1：implementation materialization 后、任何 R3 code execution 前

G0 PASS后只允许create-new提交implementation manifest与15个implementation files。随后必须再次独立检查：

1. implementation manifest exact digest等于人工授权记录；
2. 15个file path/size/SHA-256与manifest逐项一致，无第16个implementation file；
3. 除这16个create-new file与其获批目录外，Runtime/legacy/R2/source/Candidate/workspace bytes均无变化；
4. builder、test builder、verifier、runner、result generator全部可静态解析，且没有额外project-tree writer；
5. isolated/no-bytecode environment、cwd、`sys.path`、temp/cache policy可以先于import建立；
6. `r3_execution_plan.json`与其后全部suite/result artifact尚不存在；
7. Plan digest、implementation manifest digest、Profile、R2 digests、fixed time、scope与五个control program digest可完整写入唯一execution plan。

只有G1 PASS，`run_r3_portable_closure.py bootstrap`才可创建execution plan并开始controller terminal chain。该两阶段Gate消除了“尚未创建的runner必须在首次写前自证digest”的循环。

### 13.3 唯一 stage/commit/resume contract

默认是one-shot fresh execution。唯一单向stage为：

```text
IMPLEMENTATION_MATERIALIZED
  -> EXECUTION_PLAN_FROZEN
  -> CONTROL_FROZEN
  -> START_VERIFIED
  -> DYNAMIC_OBSERVED
  -> END_VERIFIED
  -> FINALIZED
```

除`IMPLEMENTATION_MATERIALIZED`外，每个stage都使用相同two-phase commit：先在approved OS temp构造完整stage artifact group并验证；每个persistent file以create-new + fsync + atomic rename提交；**stage terminal最后append并fsync**。Terminal只在全部required artifact存在且digest匹配时才有权威。`IMPLEMENTATION_MATERIALIZED`是唯一无project ledger terminal的bootstrap例外，由人工授权中预记录的implementation-manifest exact digest闭合；下一阶段bootstrap验证它后创建ledger genesis。

| stage | required newly committed artifacts |
| --- | --- |
| `IMPLEMENTATION_MATERIALIZED` | implementation manifest + 15 implementation files；authority为外部人工授权digest；无project ledger terminal |
| `EXECUTION_PLAN_FROZEN` | execution plan + terminal ledger genesis |
| `CONTROL_FROZEN` | 按§8.2单向顺序提交closure manifest、test manifest、fixture catalog、component freeze、snapshot binding、external closure registry record + terminal |
| `START_VERIFIED` | start verification evidence + terminal |
| `DYNAMIC_OBSERVED` | complete attempts ledger、dynamic observation evidence + terminal |
| `END_VERIFIED` | end verification evidence + terminal |
| `FINALIZED` | evidence manifest（绑定截至END_VERIFIED的terminal prefix）、aggregate、final report + 最后追加的`FINALIZED` terminal |

Resume只允许同一人工授权、Plan digest、implementation manifest digest、execution plan digest、Profile与suite ID：

- terminal存在但required artifact缺失/失配，或chain有gap/fork/duplicate：永久BLOCKED；
- complete artifact group存在但terminal缺失：从frozen inputs在temp独立复算全部bytes；完全一致时只append一个`ADOPT_COMPLETE_ORPHAN` terminal，不覆盖artifact；该terminal必须含`adopted_stage=<expected stage>`和`resulting_stage=<same expected stage>`，并在状态机中与该target stage的正常commit terminal完全等价，不能形成额外stage或跳级；
- deterministic stage只提交了artifact group的严格子集：已存在文件全部匹配temp重建结果时，只create缺失文件再提交terminal；任一不匹配即BLOCKED；
- implementation manifest存在而15-file bundle为严格子集：仅可从人工授权的exact bundle补齐缺失path；manifest缺失而任何implementation file已出现，或exact bundle不可恢复，永久BLOCKED；
- dynamic observation/attempt执行一旦中断、coverage不完整或terminal数不足，当前suite永久`BLOCKED_DYNAMIC_OBSERVATION_INCOMPLETE`；不得拼接第二次观察；
- start verification后任何member/control/platform identity变化，不能resume；
- aggregate存在但report缺失时，不视为finalized；若aggregate与sealed END_VERIFIED terminal prefix通过独立复算，result generator可幂等地产生唯一exact report，然后append`FINALIZED` terminal；report存在而aggregate缺失则BLOCKED；
- aggregate与report均存在但`FINALIZED` terminal缺失时，独立复算后只appendterminal；只有`FINALIZED` terminal加完整匹配artifact group才表示finalized；
- 禁止删除partial artifact、覆盖create-once artifact、截断ledger或重跑已提交dynamic attempts来伪装fresh。

若当前suite不可恢复，本Plan不授权第二个suite ID；必须重新规划并授权新的exact paths。

Finalization无环规则：evidence manifest与aggregate只保存`controller_terminals.jsonl`截至`END_VERIFIED`的prefix identity；final report保存同一prefix identity和aggregate digest；`FINALIZED` terminal再单向引用evidence-manifest/aggregate/report exact digests。追加后完整terminal-ledger exact SHA-256由本阶段外部delivery metadata与final result交付信息记录，不回写任何project artifact。Verifier必须同时验证sealed prefix、FINALIZED append和external delivery digest。

## 14. Functional requirements 到文件/evidence 的闭合映射

下表所有实现/evidence path均相对于`runtime_capability_prototype/`；只有final report是workspace-root `PORTABLE_RUNTIME_TRANSITIVE_CLOSURE_RESULT.md`。一行包含多个artifact时，该集合是closed mandatory set，不得任选其一。

### 14.1 正式 `P2GR-R3-001..008`

| requirement | implementation file(s) | independent verifier | closed canonical evidence set |
| --- | --- | --- | --- |
| `P2GR-R3-001` roots/node types/platform/public-trust boundary关闭定义 | `contracts/r3_portable_closure_policy_v1.yaml`; `contracts/runtime_transitive_closure_manifest_schema_v1.yaml`; `runtime/build_r3_portable_closure.py` | `runtime/verify_r3_portable_closure.py` | `r3_portable_suites/R3PS-20260811-001/control/runtime_transitive_closure_manifest.json`; `r3_portable_suites/R3PS-20260811-001/evidence/start/closure_start_verification.json` |
| `P2GR-R3-002` known gaps全部进入graph | closure policy; closure builder | closure verifier独立reachability/classification pass | closure manifest；start evidence；其中`common.py`/initializer为runtime members，legacy build/trace为frozen excluded nodes |
| `P2GR-R3-003` static/dynamic/code-config open一致 | closure builder; `runtime/run_r3_portable_closure.py` no-content observer | closure verifier static-vs-dynamic comparison | `r3_portable_suites/R3PS-20260811-001/evidence/dynamic/dynamic_dependency_observation.json`; `r3_portable_suites/R3PS-20260811-001/evidence/end/closure_end_verification.json` |
| `P2GR-R3-004` unknown/unresolved/symlink=0 | closure builder; closure schema | closure verifier fail-closed | closure manifest；`r3_portable_suites/R3PS-20260811-001/aggregate/r3_portable_closure_results.json` |
| `P2GR-R3-005` native source→recipe→toolchain/link→binary | `contracts/native_component_build_policy_v1.yaml`; closure builder | closure verifier independent temp rebuild/fingerprint pass | closure manifest；start evidence；end evidence |
| `P2GR-R3-006` schema/policy及R3 builder/runner/verifier/aggregate/report被冻结；Portable Runtime/R4 counterparts必须无gap | `control/r3_implementation_manifest.json`; `control/component_freeze.json`; five R3 control programs in§6.2; formal role inventory | closure verifier hashes每个control member、拒绝classification混用并要求required-role gap=0才PASS | component freeze；start evidence；end evidence；aggregate |
| `P2GR-R3-007` start/end全量digest与delta=0 | `runtime/run_r3_portable_closure.py`; closure verifier | closure verifier两次独立全量复算 | start evidence；end evidence；aggregate |
| `P2GR-R3-008` payload/file/external registry可独立复算 | closure builder; `contracts/closure_snapshot_registry_record_schema_v1.yaml`; controller registry-record pass | closure verifier不信任builder/record中的预填digest，重新hash exact bytes | `control/closure_snapshot_registry_record.json`; start evidence；end evidence；aggregate |

### 14.2 本 R3P 强制 requirement mapping

| requirement | implementation file(s) | verifier | closed canonical evidence set |
| --- | --- | --- | --- |
| entrypoints enumeration + formal role gaps | closure policy; closure builder | closure verifier | closure manifest `entrypoints/required_runtime_roles/required_runtime_role_gaps`; start evidence |
| complete transitive closure | closure builder | closure verifier graph traversal | closure manifest `members/dependency_edges`; start evidence |
| dynamic dependency closure | closure builder; R3 runner no-content observer | closure verifier static/dynamic comparison | dynamic evidence；end evidence |
| unresolved dependency = 0 | closure builder/schema | closure verifier fail-closed | closure manifest `unresolved_dependencies`; aggregate |
| canonical manifest reproducibility | closure builder two-temp-build mode | closure verifier exact-byte comparison | start evidence；`attempts/r3_attempts.jsonl`; aggregate |
| component freeze | closure builder; component-freeze schema | closure verifier start/end full hash | `control/component_freeze.json`; start evidence；end evidence |
| execution snapshot binding | binding schema; closure builder; independent registry-record pass | closure verifier closure/freeze/binding cross-check | `control/execution_snapshot_closure_binding.json`; `control/closure_snapshot_registry_record.json` |
| tamper rejection | requirements; frozen test manifest; R3 runner ephemeral shadow trees | closure verifier | fixture catalog；attempts ledger；controller terminal ledger；aggregate |
| exclusion reachability rejection | closure policy; synthetic reachable sentinel | closure verifier full graph traversal | closure manifest `exclusions`; dynamic evidence；attempts ledger；aggregate |
| test-only/build-only classification | closure policy/schema | closure verifier dual-root reachability + member-type check | closure manifest classified members；aggregate |
| native/platform/public-trust identity | native build policy; closure builder; formal role inventory | closure verifier exact fingerprint/rebuild/public-key bytes comparison | closure manifest `platform_boundaries`/public-trust nodes；start evidence；end evidence |
| R2 protected baseline + Profile binding | implementation manifest; execution plan; all control schemas | closure verifier | start evidence；external registry record；aggregate |
| A1-only evidence | control artifact schema; result generator | closure verifier rejects A2/A3/Hardened/certified claim | aggregate；workspace-root final report |
| zero scope violations | R3 runner closed write/cache ledger; result generator | closure verifier before/after tree comparison | `evidence/evidence_manifest.json`; aggregate；workspace-root final report |

不得在实施时改用legacy `component_manifest.yaml`、`build_manifest.py`、`verify_trace.py`、`run_suite.py`或旧aggregate作为active implementation/evidence。表内简称`closure manifest/start evidence/end evidence/dynamic evidence/aggregate`只指§5冻结的唯一exact path，不引入第二布局。

## 15. R3 原子边界、deferred 项与 defect 处理

### 15.1 Future R3 唯一允许的动作

- Runtime entrypoint inventory；
- automatic transitive closure computation；
- static/dynamic/config/executable/platform dependency resolution；
- canonical closure manifest；
- complete component/control freeze；
- execution snapshot closure binding readiness；
- deterministic R3 verification；
- synthetic R3 tests与A1 controller evidence；
- `PORTABLE_RUNTIME_TRANSITIVE_CLOSURE_RESULT.md`。

### 15.2 明确不得顺便做

- Authorization Schema V2 redesign；
- R2 semantic/implementation fix；
- R4 full synthetic E2E、broker source open/read、bounded delivery、parser/gateway E2E；
- actual Candidate authorization/execution；
- Odyssey source handling、Book 1/2/Greek正文或Map读取；
- literary analysis、`story_structure.yaml`、business output；
- model integration/invocation；
- ptrace/strace/fanotify/eBPF/audit修复；
- A2/A3、Hardened certification或Portable-to-Hardened promotion；
- 修改旧 suite、R2 suite、Run 001/002 或历史状态。

### 15.3 Deferred classification

| item | disposition |
| --- | --- |
| Portable source-range/broker/reader E2E | `deferred_to_R4` |
| R4-specific builder/runner/verifier/aggregate/report/schema/policy/evidence | `deferred_to_R4`；无论标为production/test/control/build，只要未在当前freeze中，R4执行前必须以新Plan、新suite path和新授权fresh R3 refresh + PASS |
| Candidate Plan/run/authorization/provenance | `blocked_after_R3_until_R4_PASS_and_new_authorization` |
| OS observer、complete file-open set、zero-bypass proof | `hardened_only` |
| R1-H、R3-H、R4-H、A3 certification | `hardened_only / fresh execution required` |

### 15.4 R2 defect rule

若 R3 static/dynamic inspection发现真正的 R2 defect，R3必须：

1. 记录 defect path、digest、reachable edge和影响；
2. 不修改 R2 asset；
3. 不重写历史 `PASS_PORTABLE_AUTHORIZATION_SCHEMA_V2_IMPLEMENTED`；
4. 不把 defect伪装成R3 exclusion或deferred；
5. 终止为 `BLOCKED_R3_UPSTREAM_R2_DEFECT`。

## 16. Future R3 final result contract

未来 `PORTABLE_RUNTIME_TRANSITIVE_CLOSURE_RESULT.md` 至少报告：

1. final status；
2. actual Runtime entrypoint count；
3. actual runtime closure member count；
4. actual dependency edge count；
5. actual dynamic dependency count；
6. unresolved dependency count；
7. platform boundary count；
8. closure ID；
9. closure payload SHA-256；
10. closure manifest exact file SHA-256；
11. external closure registry record exact SHA-256与独立复算结果；
12. required runtime role count/gap count与gap identities；
13. 所有实际新增/修改文件及前后摘要；
14. R2 asset modification count；
15. tests：discovered/executed/evidence_complete/passed/failed/skipped/unknown/timeout；
16. closure verification/component freeze/execution binding readiness；
17. deferred R4与Hardened-only项；
18. English/Greek TEI、Candidate、model、business output、R3 scope violation controller A1 counts；
19. `Portable / Development Profile / A1 only / non-certified`；
20. `a2_os_file_access_proof=NOT_PROVIDED`、`hardened=false`、`certified=false`。

只有以下全部成立才允许：

```text
PASS_PORTABLE_RUNTIME_TRANSITIVE_CLOSURE
```

- approved真实 Runtime entrypoints全部存在并被枚举；
- formal required runtime role gap count = 0；
- closure自动计算成功；
- dynamic/config/executable dependencies全部闭合；
- unresolved dependency = 0；
- component freeze覆盖完整 runtime + control classification；
- canonical manifest exact bytes可确定性复现；
- execution snapshot可绑定 closure identity；
- external closure registry identity exact bytes可由独立verifier复算；
- 所有 manifest-enumerated R3 tests实际 PASS且evidence complete；
- R2 asset modification count = 0；
- R3 scope violation count = 0。

按本阶段只读现状，七个formal role gap已知非零，因此本Plan**不授权、也不预测**立即达到上述PASS。若未来实施授权仍严格禁止补齐这些existing-Runtime defects，R3应按计划生成精确BLOCKED结果后停止；若要补齐角色，必须先另行原子范围计划与实施，随后以改变后的bytes获得fresh R3 Plan/authorization，不能在本R3内顺便修复。

否则只能：

```text
BLOCKED_PORTABLE_RUNTIME_TRANSITIVE_CLOSURE_FAILED
```

## 17. 历史状态与本阶段终检

### 17.1 历史状态不变

```yaml
phase_2g: "BLOCKED_RUNTIME_CAPABILITY_PROTOTYPE_FAILED"
phase_2g_r1: "BLOCKED_OS_OBSERVABILITY_INSUFFICIENT"
phase_2g_r1d: "ADOPT_DUAL_ASSURANCE_PROFILES"
phase_2g_r2p: "PASS_PORTABLE_R2_PLAN_ONLY"
phase_2g_r2: "PASS_PORTABLE_AUTHORIZATION_SCHEMA_V2_IMPLEMENTED"

historical_allow_r2_false_changed: false
old_suite_status_changed: false
run_001_status_changed: false
run_002_status_changed: false
candidate_analysis: "BLOCKED"
```

### 17.2 本 Plan 阶段 controller A1 action ledger

以下是本阶段 planning controller 的逻辑动作账本，不是 A2 OS-verified counts：

```yaml
created_files:
  - "PORTABLE_RUNTIME_TRANSITIVE_CLOSURE_PLAN.md"
modified_existing_files: []

runtime_modifications: 0
legacy_file_modifications: 0
r2_asset_modifications: 0
closure_manifests_created: 0
component_freeze_artifacts_created: 0
execution_snapshot_bindings_created: 0
evidence_trees_created: 0
runtime_tests_executed: 0
r3_execution_count: 0
r4_execution_count: 0
candidate_run_count: 0
model_integration_call_count: 0
english_tei_content_read_count: 0
greek_tei_content_read_count: 0
business_output_count: 0
story_structure_yaml_created: false
r3_scope_violation_count: 0

a2_os_verified_counts:
  status: "NOT_PROVIDED"
```

本阶段完成只表示 R3 文件级原子范围、legacy disposition、canonical paths、builder/freeze/test contracts和future Gate 已唯一确定。它不创建 R3 实体，不授权或执行 R3，不自动进入 R4，也不改变 Candidate blocked 状态。
