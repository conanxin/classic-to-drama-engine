# Classic-to-Drama Engine：Portable Runtime Public Trust Binding File-Level Atomic Plan

> 项目：Classic-to-Drama Engine  
> 阶段：Phase 2-G-R3G2  
> phase_kind：`file_level_atomic_planning_only`  
> 日期：2026-08-12  
> 最终状态：`PASS_PORTABLE_RUNTIME_PUBLIC_TRUST_BINDING_ATOMIC_PLAN`  
> 当前效力：planning only / implementation not authorized / Runtime unchanged / tests not executed  
> Profile：`CTDE-PORTABLE-DEV-1`  
> 最高可声明证据：`A1 / Development / non-certified`  
> Candidate Analysis：`BLOCKED`

## 0. 最终结论与机器合同

本 Plan 只把 R3G1 已批准的 `R3G-07-IMMUTABLE-PUBLIC-TRUST-KEY-STATUS` scope 转换为闭合、逐文件、可确定性验证的 future implementation 合同。本阶段没有创建任何 schema、trust asset、public key、private key、loader、verifier、runner、suite artifact 或 repair result，也没有运行 Runtime 或测试。

### 0.1 R3G2 entry contract

```yaml
entry_contract:
  current_status: "PASS_R3G2_PHASE_KIND_CONTRACT_RECONCILIATION"
  next_phase_id: "Phase 2-G-R3G2"
  next_phase_kind: "file_level_atomic_planning_only"
  scope_status: "resolved_for_planning"
  r3g2_planning_ready: true
  execution_authorized: false
  explicit_human_planning_authorization_received: true
  planning_authorization_scope: "create PORTABLE_RUNTIME_PUBLIC_TRUST_BINDING_PLAN.md only"
```

`execution_authorized: false` 原样保留 reconciliation 的入场字段，表示此前没有自动 execution authority；本轮用户另行提供的 `explicit_human_planning_authorization_received: true` 只授权创建 R3G2 planning artifact，不授权下面规划的 implementation。

### 0.2 R3G2 result contract

```yaml
final_status: "PASS_PORTABLE_RUNTIME_PUBLIC_TRUST_BINDING_ATOMIC_PLAN"
gap_id: "R3G-07-IMMUTABLE-PUBLIC-TRUST-KEY-STATUS"
runtime_role: "immutable public trust material / key-status registry"
phase_id: "Phase 2-G-R3G2"
phase_kind: "file_level_atomic_planning_only"

source_reconciliation_sha256: "0bcde11bee488aae7d7a1070d010ba96636437f64f583e981272f6cb77cb37e8"
source_audit_sha256: "e5cd250eeaec8921afd6658e55d140e4f897ce99860e2825aad1af14f6eab1f7"

future_mutable_existing_files_count: 0
future_creatable_files_count: 20
future_creatable_directories_count: 7
actual_runtime_callers_count: 6

implementation_sequence_node_count: 22
file_creation_phase_count: 20
dependency_node_count: 22
dependency_edge_count: 100
dependency_cycle_count: 0
test_requirement_groups_count: 21

unresolved_file_role_count: 0
unresolved_implementation_ambiguity_count: 0
scope_expansion_required_count: 0
r2_semantic_regression_count: 0

fresh_r3_replan_required: true
implementation_authorized: false
r3_execution_authorized: false
r4_execution_authorized: false
candidate_execution_authorized: false
```

### 0.3 Next-step machine contract

本 Plan 按 Role Gap Plan §7/§9 的授权，为 future implementation 定义唯一后续 phase identity。该 identity 只供下一轮明确人工授权匹配；本 Plan 不自动启动它。

```yaml
current_status: "PASS_PORTABLE_RUNTIME_PUBLIC_TRUST_BINDING_ATOMIC_PLAN"
next_phase_id: "Phase 2-G-R3G3"
next_phase_kind: "r3g07_atomic_implementation_and_deterministic_verification_only"
scope_status: "planned_waiting_for_explicit_implementation_authorization"
execution_authorized: false
implementation_authorized: false
r3g07_implementation_ready_for_authorization_review: true
```

人类标题可以写作 `R3G-07 Atomic Implementation and Deterministic Verification`，但未来命令的 machine fields 必须逐字使用上述 `next_phase_id` 与 `next_phase_kind`。在新的明确人工授权到达前，20 个 future files 和 7 个 future directories 均不得创建。

## 1. 正式依据、摘要与写前 Gate

### 1.1 正式依据

| 正式文件 | 当前只读 SHA-256 | 本 Plan 的用途 |
| --- | --- | --- |
| `R3G2_PHASE_KIND_CONTRACT_RECONCILIATION.md` | `0bcde11bee488aae7d7a1070d010ba96636437f64f583e981272f6cb77cb37e8` | canonical R3G2 machine phase kind 与命令匹配规则 |
| `PORTABLE_RUNTIME_PUBLIC_TRUST_BINDING_SCOPE_AUDIT.md` | `e5cd250eeaec8921afd6658e55d140e4f897ce99860e2825aad1af14f6eab1f7` | 0/20/7 scope、六 caller、trust model、private boundary 与 closure bindings |
| `PORTABLE_RUNTIME_ROLE_GAP_RESOLUTION_PLAN.md` | `72f116ff0b93403961a045228706f9322deea008f41718acae6178b0780b8798` | R3G-07 authority、R3G2 closed write scope 与 R3 re-entry Gate |
| `PORTABLE_RUNTIME_TRANSITIVE_CLOSURE_PLAN.md` | `f8ca07eaee1fff534e97bf4a0d037ba73a3c1838107e132f7c072b1fe05b39f5` | public-trust role gap、future closure node/classification/freeze contract |
| `PORTABLE_AUTHORIZATION_SCHEMA_V2_PLAN.md` | `32513cdb2c004ea91c7d7208eb3a40901934dc80440af048b84701facf1bdbe9` | R2 exact-bytes Registry authority、one-time/CAS/replay 与 semantic boundary |
| `PORTABLE_AUTHORIZATION_SCHEMA_V2_IMPLEMENTATION_RESULT.md` | `b47c7280880af70325a5e5c45426951567390441ad4cd61465724fbb8eabcd06` | R2 implementation PASS、16 canonical assets 与 51/51 historical evidence |
| `RUNTIME_ASSURANCE_PROFILE_DECISION.md` | `57471c85c57946f6ceb6da288301cc802533b09c137bfbe8e6e247dad57206e2` | Portable A1 / Development / non-certified claim ceiling |

### 1.2 Machine phase Gate

```yaml
expected_phase_id: "Phase 2-G-R3G2"
observed_role_gap_plan_phase_id: "Phase 2-G-R3G2"
expected_phase_kind: "file_level_atomic_planning_only"
observed_role_gap_plan_phase_kind: "file_level_atomic_planning_only"
observed_scope_audit_r3g2_phase_kind: "file_level_atomic_planning_only"
observed_reconciliation_next_phase_kind: "file_level_atomic_planning_only"
phase_contract_match: true
```

### 1.3 Scope snapshot Gate

写入本文件之前，只读复核得到：

```yaml
future_mutable_existing_files:
  expected: 0
  observed: 0
future_creatable_files:
  expected: 20
  observed_paths: 20
  existing_before: 0
future_creatable_directories:
  expected: 7
  observed_paths: 7
  existing_before: 0
actual_runtime_callers:
  expected: 6
  observed: 6
unresolved_scope_ambiguity:
  expected: 0
  observed: 0
r2_semantic_regression:
  expected: 0
  observed: 0
r3g2_ready: true
scope_snapshot_match: true
```

R3G2 唯一允许创建的 planning artifact 由 Role Gap Plan §9.2 与 R3G1 Audit §14 共同唯一确定为：

```text
PORTABLE_RUNTIME_PUBLIC_TRUST_BINDING_PLAN.md
```

该路径写前为 `ABSENT`。本阶段没有 existing mutable file。

## 2. R3G1 future scope 原样冻结

本节是 future Phase 2-G-R3G3 的 closed authority。路径集合逐项复用 R3G1 Audit §12；本 Plan 不新增第 21 个 file、不新增第 8 个 directory、不修改现有路径。

### 2.1 Mutable existing files

```yaml
mutable_existing_files: []
mutable_existing_files_count: 0
```

任何 future implementation 推导若要求修改既有 caller、`signing.py`、R2 asset、`__init__.py` 或其他 existing file，必须在首次写入前停止：

```text
BLOCKED_R3G2_EXISTING_CALLER_MUTATION_REQUIRED
```

不得把该失败转化为临时 scope expansion。

### 2.2 Creatable files

```yaml
creatable_files:
  - "runtime_capability_prototype/contracts/public_trust_material_schema_v1.yaml"
  - "runtime_capability_prototype/contracts/public_key_status_registry_schema_v1.yaml"
  - "runtime_capability_prototype/contracts/portable_public_trust_material_v1.json"
  - "runtime_capability_prototype/contracts/portable_public_key_status_registry_v1.json"
  - "runtime_capability_prototype/runtime/ctde_runtime/public_trust.py"
  - "runtime_capability_prototype/contracts/r3g07_public_trust_test_requirements.yaml"
  - "runtime_capability_prototype/contracts/r3g07_public_trust_test_manifest_schema_v1.yaml"
  - "runtime_capability_prototype/runtime/build_r3g07_public_trust_test_manifest.py"
  - "runtime_capability_prototype/runtime/verify_r3g07_public_trust.py"
  - "runtime_capability_prototype/runtime/run_r3g07_public_trust.py"
  - "runtime_capability_prototype/runtime/build_r3g07_public_trust_result.py"
  - "runtime_capability_prototype/r3g07_portable_suites/R3G07PS-20260812-001/control/r3g07_implementation_manifest.json"
  - "runtime_capability_prototype/r3g07_portable_suites/R3G07PS-20260812-001/control/r3g07_execution_plan.json"
  - "runtime_capability_prototype/r3g07_portable_suites/R3G07PS-20260812-001/control/r3g07_test_manifest.json"
  - "runtime_capability_prototype/r3g07_portable_suites/R3G07PS-20260812-001/fixtures/r3g07_synthetic_fixtures.json"
  - "runtime_capability_prototype/r3g07_portable_suites/R3G07PS-20260812-001/fixtures/r3g07_test_signing_key_ed25519_seed.hex"
  - "runtime_capability_prototype/r3g07_portable_suites/R3G07PS-20260812-001/attempts/r3g07_attempts.jsonl"
  - "runtime_capability_prototype/r3g07_portable_suites/R3G07PS-20260812-001/evidence/r3g07_public_trust_verification.json"
  - "runtime_capability_prototype/r3g07_portable_suites/R3G07PS-20260812-001/aggregate/r3g07_public_trust_results.json"
  - "PORTABLE_RUNTIME_ROLE_GAP_R3G07_REPAIR_RESULT.md"
creatable_files_count: 20
```

### 2.3 Creatable directories

```yaml
creatable_directories:
  - "runtime_capability_prototype/r3g07_portable_suites"
  - "runtime_capability_prototype/r3g07_portable_suites/R3G07PS-20260812-001"
  - "runtime_capability_prototype/r3g07_portable_suites/R3G07PS-20260812-001/control"
  - "runtime_capability_prototype/r3g07_portable_suites/R3G07PS-20260812-001/fixtures"
  - "runtime_capability_prototype/r3g07_portable_suites/R3G07PS-20260812-001/attempts"
  - "runtime_capability_prototype/r3g07_portable_suites/R3G07PS-20260812-001/evidence"
  - "runtime_capability_prototype/r3g07_portable_suites/R3G07PS-20260812-001/aggregate"
creatable_directories_count: 7
```

`contracts/`、`runtime/` 和 `runtime/ctde_runtime/` 已存在，不属于 creatable directories。

### 2.4 Read-only files

下列集合与 R3G1 Audit §12.2 完全一致。Future Plan 自身的摘要不能写入自身正文；future implementation authorization 必须从本阶段外部交付信息取得其 exact SHA-256，并在首次写入前比较。

```text
PORTABLE_RUNTIME_ROLE_GAP_RESOLUTION_PLAN.md
PORTABLE_RUNTIME_TRANSITIVE_CLOSURE_PLAN.md
RUNTIME_CAPABILITY_PROTOTYPE_RESULT.md
RUNTIME_CAPABILITY_REPAIR_PLAN.md
RUNTIME_ASSURANCE_PROFILE_DECISION.md
PORTABLE_AUTHORIZATION_SCHEMA_V2_PLAN.md
PORTABLE_AUTHORIZATION_SCHEMA_V2_IMPLEMENTATION_RESULT.md
CANDIDATE_EXECUTION_CONTRACT_REPAIR.md
PORTABLE_RUNTIME_PUBLIC_TRUST_BINDING_SCOPE_AUDIT.md
PORTABLE_RUNTIME_PUBLIC_TRUST_BINDING_PLAN.md
runtime_capability_prototype/runtime/ctde_runtime/__init__.py
runtime_capability_prototype/runtime/ctde_runtime/common.py
runtime_capability_prototype/runtime/ctde_runtime/signing.py
runtime_capability_prototype/runtime/ctde_runtime/events.py
runtime_capability_prototype/runtime/ctde_runtime/authorization_v2.py
runtime_capability_prototype/runtime/ctde_runtime/authorization_registry.py
runtime_capability_prototype/runtime/ctde_runtime/range_broker.py
runtime_capability_prototype/runtime/ctde_runtime/bounded_reader.py
runtime_capability_prototype/runtime/ctde_runtime/formal_loader.py
runtime_capability_prototype/runtime/ctde_runtime/read_audit.py
runtime_capability_prototype/runtime/run_suite.py
runtime_capability_prototype/runtime/run_r2_portable.py
runtime_capability_prototype/runtime/build_manifest.py
runtime_capability_prototype/runtime/build_r2_portable_manifest.py
runtime_capability_prototype/contracts/authorization_schema_v2.yaml
runtime_capability_prototype/contracts/authorization_registry_record_schema_v2.yaml
runtime_capability_prototype/contracts/authorization_registry_event_schema_v2.yaml
runtime_capability_prototype/contracts/capability_claims_schema_v2.yaml
runtime_capability_prototype/contracts/broker_envelope_schema_v2.yaml
runtime_capability_prototype/contracts/audit_attestation_schema_v2.yaml
runtime_capability_prototype/contracts/r2_portable_controller_terminal_schema_v1.yaml
runtime_capability_prototype/contracts/r2_portable_authorization_test_requirements.yaml
runtime_capability_prototype/r2_portable_suites/R2PS-20260811-001/control/component_inputs.json
runtime_capability_prototype/r2_portable_suites/R2PS-20260811-001/control/r2_portable_manifest.yaml
runtime_capability_prototype/r2_portable_suites/R2PS-20260811-001/aggregate/r2_portable_results.json
```

### 2.5 Current read-only baselines

| Existing read-only file | Current SHA-256 |
| --- | --- |
| `PORTABLE_RUNTIME_ROLE_GAP_RESOLUTION_PLAN.md` | `72f116ff0b93403961a045228706f9322deea008f41718acae6178b0780b8798` |
| `PORTABLE_RUNTIME_TRANSITIVE_CLOSURE_PLAN.md` | `f8ca07eaee1fff534e97bf4a0d037ba73a3c1838107e132f7c072b1fe05b39f5` |
| `RUNTIME_CAPABILITY_PROTOTYPE_RESULT.md` | `6811bcc4ef0efcaee89013648dd0bb06bbaca154625f3dc47bdfa0f295851753` |
| `RUNTIME_CAPABILITY_REPAIR_PLAN.md` | `a2c52dbaecf3956cf4a2189abe5401f269d255e8099d3345985619be25be4213` |
| `RUNTIME_ASSURANCE_PROFILE_DECISION.md` | `57471c85c57946f6ceb6da288301cc802533b09c137bfbe8e6e247dad57206e2` |
| `PORTABLE_AUTHORIZATION_SCHEMA_V2_PLAN.md` | `32513cdb2c004ea91c7d7208eb3a40901934dc80440af048b84701facf1bdbe9` |
| `PORTABLE_AUTHORIZATION_SCHEMA_V2_IMPLEMENTATION_RESULT.md` | `b47c7280880af70325a5e5c45426951567390441ad4cd61465724fbb8eabcd06` |
| `CANDIDATE_EXECUTION_CONTRACT_REPAIR.md` | `12ceb01cab4901cb2b7472b1b56f93750a43cb8c28b5f0c9ab89acf3ad4fe7bd` |
| `PORTABLE_RUNTIME_PUBLIC_TRUST_BINDING_SCOPE_AUDIT.md` | `e5cd250eeaec8921afd6658e55d140e4f897ce99860e2825aad1af14f6eab1f7` |
| `PORTABLE_RUNTIME_PUBLIC_TRUST_BINDING_PLAN.md` | exact digest must equal this stage's external handoff digest; self-digest is forbidden |
| `runtime_capability_prototype/runtime/ctde_runtime/__init__.py` | `5af22556eb42fe18c104234b803bce2a0eedc69a7c8aaba76737c39a7918a16e` |
| `runtime_capability_prototype/runtime/ctde_runtime/common.py` | `20a1d4c184753f007e4da2b11cabc3f96b1049d75aa69673ddfbe0d26344aa56` |
| `runtime_capability_prototype/runtime/ctde_runtime/signing.py` | `5c41a1601b9824715d17ae416513646575006a9207dedd26bb2036336e66cc36` |
| `runtime_capability_prototype/runtime/ctde_runtime/events.py` | `808115293ec818eedd926e4ef63869a7d5f9eeb1dca26a6902c12850b4e7fd15` |
| `runtime_capability_prototype/runtime/ctde_runtime/authorization_v2.py` | `5359cf7289e130f8a3c4228dd6d4c8b0e961ef9da716c05a78169191d571ba4d` |
| `runtime_capability_prototype/runtime/ctde_runtime/authorization_registry.py` | `e6ee8923c1c05c1ebdf04106fed659d40b8d394f6cbca4688d437dd58ee446af` |
| `runtime_capability_prototype/runtime/ctde_runtime/range_broker.py` | `ef2be994b82f10f025411e1d074cda3d0336e352f063bb9162edbcaed105958a` |
| `runtime_capability_prototype/runtime/ctde_runtime/bounded_reader.py` | `65c8f0a3af625c505fcdc05f7a754075e4829d2183931d71fa8c4dfdbf46f68c` |
| `runtime_capability_prototype/runtime/ctde_runtime/formal_loader.py` | `eb866084c8dc95c52b28118a2669314559d165e6b949cb0ff7edeb111c10e11d` |
| `runtime_capability_prototype/runtime/ctde_runtime/read_audit.py` | `b5c8a9210c4f9f295351b32e3f2a5e310ad0531720ff886a9d84385ec1ab6b4d` |
| `runtime_capability_prototype/runtime/run_suite.py` | `caf32bdb9c49ba78ee1671d41b62bc9eb8297343624ceb7afd562443a6794749` |
| `runtime_capability_prototype/runtime/run_r2_portable.py` | `ec1c86ed0f89a76b497dc9d48ff4fc092c5ff1e78d84fb3dff407a9040a4ca75` |
| `runtime_capability_prototype/runtime/build_manifest.py` | `78a206e28365cfe7d6caf677ef818ddaddb7db2b920cac535ea84d206205213d` |
| `runtime_capability_prototype/runtime/build_r2_portable_manifest.py` | `8f75e72d33d3c1cabf2bce866eac9fb44aec5775c68127576073ce510498828c` |
| `runtime_capability_prototype/contracts/authorization_schema_v2.yaml` | `f1d7c2e36e0d3072624609591eb8dfc20d0e42dce6accc8e87de730ec4478e33` |
| `runtime_capability_prototype/contracts/authorization_registry_record_schema_v2.yaml` | `4f5241697c987fbefb4531f61e85b010332b988062ee02c83ba2052e5c1c31be` |
| `runtime_capability_prototype/contracts/authorization_registry_event_schema_v2.yaml` | `16dc8fec0ab7c1ae152781f7ec177c6679ca4a52a465254f0c98a122c8a59bea` |
| `runtime_capability_prototype/contracts/capability_claims_schema_v2.yaml` | `3f872d00524c683ff93a9a8c3e02b63cc1f40da4bec72bb1289887cc0bca06bf` |
| `runtime_capability_prototype/contracts/broker_envelope_schema_v2.yaml` | `c7b8ff11745d607b1511b4f7a11c7944896b9f2f1383e0ccbadda89f0ef91010` |
| `runtime_capability_prototype/contracts/audit_attestation_schema_v2.yaml` | `9728fa6fb64ebfbc1cb260e6986f2d1947fc340445d515e27880e419d0d16da3` |
| `runtime_capability_prototype/contracts/r2_portable_controller_terminal_schema_v1.yaml` | `7b2a983750a903e43489854750d56d4f6fee31a8fb541615d8247e2bf90454ac` |
| `runtime_capability_prototype/contracts/r2_portable_authorization_test_requirements.yaml` | `0c206312075dc34123fcaef0ec81475f72197618fb7003c1764d9898dee84965` |
| `runtime_capability_prototype/r2_portable_suites/R2PS-20260811-001/control/component_inputs.json` | `ab75e95bc0cdef67fb60f6b04c9fe143e0a8e71b396c1ffe17a2473a59216b1a` |
| `runtime_capability_prototype/r2_portable_suites/R2PS-20260811-001/control/r2_portable_manifest.yaml` | `a8f712657b05eb2ea4a55719a664585c0f0754e07709f11ee2683cb130abcd76` |
| `runtime_capability_prototype/r2_portable_suites/R2PS-20260811-001/aggregate/r2_portable_results.json` | `3941449585b1d7071f703c2858a3f72bbed929ef092f496ae3b30037900c4e61` |

### 2.6 Forbidden paths

下列 future implementation policy 与 R3G1 Audit §12.3 完全一致：

```yaml
forbidden_paths:
  - path: "source"
    access: "read_and_write"
    recursive: true
  - path: "analysis_candidate"
    access: "read_and_write"
    recursive: true
  - path: "runtime_os_observability_preflight"
    access: "read_and_write"
    recursive: true
  - path: "runtime_capability_prototype/suites"
    access: "write"
    recursive: true
  - path: "runtime_capability_prototype/r2_portable_suites"
    access: "write"
    recursive: true
  - path: "runtime_capability_prototype/registry"
    access: "read_and_write"
    recursive: true
  - path: "runtime_capability_prototype/r3_portable_suites"
    access: "write"
    recursive: true
  - path: "runtime_capability_prototype/r4_portable_suites"
    access: "read_and_write"
    recursive: true
  - path: "runtime_capability_prototype/r3_hardened_suites"
    access: "read_and_write"
    recursive: true
  - path: "all workspace paths outside exact future creatable files/directories"
    access: "write"
workspace_write_policy: "default_deny"
```

最后一项是 R3G1 的 default-deny policy expression，不是新增的相对路径。

### 2.7 Frozen dependencies

```yaml
implementation_dependencies:
  - "existing signing.py KeyRecord/TrustStore/JWSCodec interfaces at exact audited digest"
  - "existing common.py canonical JSON/hash/error helpers at exact audited digest"
  - "existing cryptography Ed25519 distribution as future R3 platform boundary"
  - "human-authorized kid + raw 32-byte Ed25519 public key input; no private key project input"
  - "fixed CTDE-PORTABLE-DEV-1 / ctde-portable-runtime / UTC validity contract"
test_dependencies:
  - "manifest-enumerated no-content vectors"
  - "dedicated test-only Ed25519 seed distinct from formal public trust"
  - "existing six actual caller callables, exercised only before any source/path/FD action"
closure_binding_requirements:
  - "two schema identities"
  - "public material identity"
  - "key-status registry identity"
  - "public_trust loader identity"
  - "signing verifier identity"
  - "six caller identities and shared codec binding"
  - "Profile/trust-domain/fixed-clock semantic identity"
  - "test/private exclusion identity"
```

## 3. Future trust model：唯一最小职责

### 3.1 Public material

`portable_public_trust_material_v1.json` 是 create-once canonical JSON。它只保存 public verification material，固定：

- `schema_version=1.0.0`；
- `artifact_class=ctde_portable_public_trust_material`；
- `assurance_profile_id=CTDE-PORTABLE-DEV-1`；
- `trust_domain=ctde-portable-runtime`；
- `canonicalization_id=CTDE-PUBLIC-TRUST-JCS-1`；
- 非空、按 `kid` 排序且 `kid` 唯一的 key records；
- 每项固定 `jws_alg=EdDSA`、`key_algorithm=Ed25519`、`public_key_encoding=raw-32-byte-lowercase-hex`、64位小写 hex public bytes和decoded 32-byte digest。

禁止 private bytes、certificate、URL、network locator、embedded status、self-digest、float、duplicate key和unknown field。Exact bytes 是 JCS-compatible compact canonical JSON加单个 LF。

### 3.2 Key-status registry

`portable_public_key_status_registry_v1.json` 是 create-once canonical JSON。它固定相同 Profile/domain/canonicalization，使用 exact relative path引用 material asset，并保存 material exact-file SHA-256。每个 status record 固定：

- `kid` 与 material key set 完全相等；
- `jws_alg=EdDSA`、`key_algorithm=Ed25519`；
- `status` closed vocabulary：`active | revoked | expired | disabled`；
- `trust_domain=ctde-portable-runtime`；
- RFC 3339 UTC `not_before`／`expires_at`，且 `not_before <= expires_at`。

Unknown kid、任何 non-active status、not-yet-valid、validity expiry、domain/algorithm mismatch、material digest mismatch或无效时间都 fail closed。现有 `not_before <= now <= expires_at` 边界不改变。

### 3.3 Deterministic loader/resolver

唯一 public Runtime entrypoint：

```text
runtime_capability_prototype/runtime/ctde_runtime/public_trust.py::load_portable_public_trust
```

它必须：

1. 使用 module-relative exact constants定位两个schema和两个asset；public entrypoint不接收path、bytes、dict、`TrustStore`、environment override、URL或network input；
2. 拒绝BOM、duplicate key、float、noncanonical bytes、unknown field和schema/profile/domain mismatch；
3. 计算两个schema、两个asset exact SHA-256，验证status→material单向digest reference；
4. decode raw Ed25519 public bytes并复算raw digest；
5. 合并material/status exact key set，构造现有 `KeyRecord -> TrustStore`；
6. 返回frozen `LoadedPublicTrust`，含store、四input digests、semantic payload digest、Profile/domain、record identities和 `public_trust_freeze_identity`；
7. `LoadedPublicTrust.codec(now)`只用fixed UTC epoch生成现有 `JWSCodec`；
8. 任一unknown/unresolved/mismatch直接抛出closed blocker，不回退caller material。

### 3.4 Binding strength boundary

R3G1 已明确选择“独立 loader + 现有 DI seam”，并冻结 `future_mutable_existing_files=[]`。因此本 Plan 的 binding 是 Portable A1 approved-composition/freeze binding：

- future controller只从 `load_portable_public_trust()` 获得一个 `LoadedPublicTrust`；
- 对一个fixed clock只创建一个bound `JWSCodec`；
- 六个真实caller全部获得同一codec object与同一freeze identity；
- F09 verifier证明object identity、store record identity、freeze digest和caller file/callable digest一致；
- fresh R3把loader→codec→six callers作为configuration/dependency edges，任何alternate codec composition均为unapproved closure，必须fail closed。

本 Plan 不声称 Python 语言层面已经禁止任意第三方直接调用现有constructor或自行构造 `TrustStore`。该更强保证需要修改caller或增加新production composer，超出0/20/7 scope。如果future implementation发现 Portable A1 approved composition不足以满足正式 role，必须在写入前或首次发现时输出：

```text
BLOCKED_R3G2_EXISTING_CALLER_MUTATION_REQUIRED
```

不得以F09 test composition冒充代码级non-bypass保证；后者属于更强scope/Hardened裁决。

## 4. 六个 actual Runtime caller binding plan

| # | Exact caller path | Callable identity | Current TrustStore behavior | Future binding mechanism | New artifact dependency | Fail-closed requirement | Deterministic verification | Closure/freeze impact | Existing file modification |
| ---: | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| C01 | `runtime_capability_prototype/runtime/ctde_runtime/events.py` | `SignedEventLog.verify` | static verifier接受caller传入的`codec`并逐token调用`codec.verify` | future approved composer从F05取得single bound codec并以现有keyword seam传入；F09核对object/freeze identity | F03、F04、F05、F09、F10、F13、F18 | unknown/non-active/wrong identity在任何event semantic acceptance前拒绝 | manifest按该qualname展开positive/negative leaves；F09复算caller digest `808115...fd15` | caller file/callable + shared codec edge进入fresh R3 runtime closure | false |
| C02 | `runtime_capability_prototype/runtime/ctde_runtime/events.py` | `PortableA1EventLogV2.verify` | static verifier接受suite-local codec；历史R2 runner使用临时test key | future production/Portable只使用F05 bound codec；历史R2 suite保持原样且不迁移 | F03、F04、F05、F09、F10、F13、F18 | wrong kid/status/profile在event fields被信任前拒绝 | no-content token vectors；同时证明R2 historical runner digest不变 | 与C01共享file digest，但独立qualname/binding edge | false |
| C03 | `runtime_capability_prototype/runtime/ctde_runtime/range_broker.py` | `RangeBroker.deliver` | constructor保存任意injected `self.codec`，`deliver`在`os.open`前验证capability | approved composition实例化真实`RangeBroker`时只注入F05 single codec；F09记录identity | F03、F04、F05、F09、F10、F13、F15、F18 | trust failure必须发生在catalog lookup、registry capability consume与`os.open`之前 | no-content sentinel使任何open/registry side effect立即失败test；manifest按qualname展开 | caller digest `ef2be9...958a` + loader/config edge进入fresh closure | false |
| C04 | `runtime_capability_prototype/runtime/ctde_runtime/bounded_reader.py` | `BoundedReader.consume` | constructor保存任意`self.codec`；先验证envelope和broker attestation，之后才`fstat/pread` | approved composition只注入F05 single codec；F09验证两次JWS调用均使用同一store/freeze | F03、F04、F05、F09、F10、F13、F15、F18 | trust failure必须发生在FD stat/read、delivery consume和sandbox前 | invalid sentinel FD + no-content stubs；若FD/path action发生leaf失败 | caller digest `65c8f0...f68c` + shared codec edge进入fresh closure | false |
| C05 | `runtime_capability_prototype/runtime/ctde_runtime/formal_loader.py` | `FormalLoader.load` | constructor保存任意`self.codec`；先验证manifest JWS，成功后才处理entries/path | approved composition只注入F05 single codec；F09核对identity | F03、F04、F05、F09、F10、F13、F15、F18 | trust failure必须在`Path`/`lstat`/`os.open`前返回closed rejection | no-content signed/invalid manifest recipes；path sentinel不可触达 | caller digest `eb8660...e11d` + loader/config edge进入fresh closure | false |
| C06 | `runtime_capability_prototype/runtime/ctde_runtime/read_audit.py` | `ReadAuditAggregator._verify_logs` | constructor保存任意`self.codec`并传给`SignedEventLog.verify` | approved composition给aggregator与nested event verifier同一F05 codec；F09验证nested identity | F03、F04、F05、F09、F10、F13、F18 | missing/invalid/untrusted log在attestation生成前拒绝 | in-memory no-content event log；验证nested call使用相同codec/freeze | caller digest `b5c8a9...6b4d`、nested C01 edge与shared identity进入fresh closure | false |

```yaml
actual_runtime_callers_count: 6
caller_binding_plans_complete: 6
caller_existing_file_mutations_required: 0
unresolved_caller_binding_count: 0
```

## 5. 七个 directory 的唯一 mapping

| ID | Exact relative directory | Creation node | Purpose | Classification | Allowed children |
| --- | --- | --- | --- | --- | --- |
| D01 | `runtime_capability_prototype/r3g07_portable_suites` | D00 | R3G-07 dedicated suite namespace | test/control root; not production closure | only D02 |
| D02 | `runtime_capability_prototype/r3g07_portable_suites/R3G07PS-20260812-001` | D00 | unique frozen suite root | test/control freeze | D03–D07 only |
| D03 | `runtime_capability_prototype/r3g07_portable_suites/R3G07PS-20260812-001/control` | D00 | implementation/execution/test manifests | control freeze | F12、F13、F14 |
| D04 | `runtime_capability_prototype/r3g07_portable_suites/R3G07PS-20260812-001/fixtures` | D00 | no-content recipes and test-only seed | test-only freeze | F15、F16 |
| D05 | `runtime_capability_prototype/r3g07_portable_suites/R3G07PS-20260812-001/attempts` | D00 | actual manifest-leaf terminal ledger | test evidence | F17 |
| D06 | `runtime_capability_prototype/r3g07_portable_suites/R3G07PS-20260812-001/evidence` | D00 | independent public-trust verification payload | A1 test evidence | F18 |
| D07 | `runtime_capability_prototype/r3g07_portable_suites/R3G07PS-20260812-001/aggregate` | D00 | mechanical aggregate | test evidence | F19 |

All seven directories are created together at D00 because they are one closed nested hierarchy whose exact child allowlist must be validated before any file creation. D00 does not create a file and cannot be split without creating intermediate states that have no independent acceptance meaning.

## 6. Twenty future files：唯一 implementation mapping

### 6.1 Identity, role, classification and producer

| ID | Exact relative path | Artifact role / purpose | Classification | Creation phase | Unique producer | R2 semantic impact |
| --- | --- | --- | --- | --- | --- | --- |
| F01 | `runtime_capability_prototype/contracts/public_trust_material_schema_v1.yaml` | closed schema for immutable public key material | runtime contract / contract schema | I01 | human-authorized implementation materializer | `integration_only` |
| F02 | `runtime_capability_prototype/contracts/public_key_status_registry_schema_v1.yaml` | closed schema for material-bound key status records | runtime contract / contract schema | I02 | implementation materializer | `integration_only` |
| F03 | `runtime_capability_prototype/contracts/portable_public_trust_material_v1.json` | create-once canonical public verification material | configuration semantic asset / runtime closure member | I03 | implementation materializer using human-authorized public input | `integration_only` |
| F04 | `runtime_capability_prototype/contracts/portable_public_key_status_registry_v1.json` | create-once canonical active/revoked/expired/disabled registry | configuration semantic asset / runtime closure member | I04 | implementation materializer | `integration_only` |
| F05 | `runtime_capability_prototype/runtime/ctde_runtime/public_trust.py` | deterministic fixed-path loader/resolver and freeze identity | runtime implementation / runtime closure member | I05 | implementation materializer | `integration_only` |
| F06 | `runtime_capability_prototype/contracts/r3g07_public_trust_test_requirements.yaml` | 21 versioned requirement groups plus closed field contracts for approved control/evidence artifacts; no fixed leaf count | test/control contract / test-only freeze | I06 | implementation materializer | `none` |
| F07 | `runtime_capability_prototype/contracts/r3g07_public_trust_test_manifest_schema_v1.yaml` | closed schema for generated leaf manifest | test contract / test-only freeze | I07 | implementation materializer | `none` |
| F08 | `runtime_capability_prototype/runtime/build_r3g07_public_trust_test_manifest.py` | deterministic requirement/caller/vector leaf enumerator | build-only control | I10 | implementation materializer | `none` |
| F09 | `runtime_capability_prototype/runtime/verify_r3g07_public_trust.py` | independent asset/loader/caller/freeze verifier | verification code / test-only freeze | I11 | implementation materializer | `integration_only` |
| F10 | `runtime_capability_prototype/runtime/run_r3g07_public_trust.py` | sole atomic controller and manifest-leaf runner | test controller / test-only freeze | I12 | implementation materializer | `none` |
| F11 | `runtime_capability_prototype/runtime/build_r3g07_public_trust_result.py` | mechanical aggregate and report bytes generator | build-only control | I13 | implementation materializer | `none` |
| F12 | `runtime_capability_prototype/r3g07_portable_suites/R3G07PS-20260812-001/control/r3g07_implementation_manifest.json` | exact future bundle, read-only baselines and scope identity | control artifact / control freeze | I14 | Phase 2-G-R3G3 controller | `integration_only` |
| F13 | `runtime_capability_prototype/r3g07_portable_suites/R3G07PS-20260812-001/control/r3g07_execution_plan.json` | fixed clock/Profile/input/Plan/authorization identity | control artifact / control freeze | I15 | Phase 2-G-R3G3 controller | `integration_only` |
| F14 | `runtime_capability_prototype/r3g07_portable_suites/R3G07PS-20260812-001/control/r3g07_test_manifest.json` | actual manifest-enumerated deterministic leaves | test manifest / test-only freeze | I16 | F08; controller persists exact bytes | `none` |
| F15 | `runtime_capability_prototype/r3g07_portable_suites/R3G07PS-20260812-001/fixtures/r3g07_synthetic_fixtures.json` | no-content recipes, mutation cases and external-signed/public vectors | test fixture / test-only freeze | I09 | implementation materializer | `none` |
| F16 | `runtime_capability_prototype/r3g07_portable_suites/R3G07PS-20260812-001/fixtures/r3g07_test_signing_key_ed25519_seed.hex` | dedicated 32-byte synthetic private seed, distinct from formal trust | test secret fixture / test-only freeze | I08 | implementation materializer under test-only authority | `none` |
| F17 | `runtime_capability_prototype/r3g07_portable_suites/R3G07PS-20260812-001/attempts/r3g07_attempts.jsonl` | append-only terminal record per actual manifest leaf | test evidence | I17 | F10 only | `none` |
| F18 | `runtime_capability_prototype/r3g07_portable_suites/R3G07PS-20260812-001/evidence/r3g07_public_trust_verification.json` | independent verification and completeness evidence | A1 test evidence | I18 | F09; controller persists exact bytes | `none` |
| F19 | `runtime_capability_prototype/r3g07_portable_suites/R3G07PS-20260812-001/aggregate/r3g07_public_trust_results.json` | mechanical discovered/executed/evidence/pass terminal aggregate | aggregate / test evidence | I19 | F11; controller persists exact bytes | `none` |
| F20 | `PORTABLE_RUNTIME_ROLE_GAP_R3G07_REPAIR_RESULT.md` | external phase result and zero-scope-regression report | build-only result report; not production closure | I20 | F11; controller persists exact bytes | `none` |

No artifact has `semantic_risk`. F01–F05, F09, F12 and F13 are `integration_only` because they bind existing signed Runtime verification and R2 baselines without changing Authorization V2 fields, Registry truth, one-time CAS or replay behavior.

### 6.2 Dataflow, consumers, outputs, closure and verification

| ID | Future-artifact dependencies | Inputs | Outputs | Runtime/control consumers | Closure membership expectation | Freeze identity requirement | Deterministic verification / acceptance evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| F01 | G00 | R3G1 schema rules | closed YAML schema bytes | F05、F08、F09、F12、F14、fresh R3 | production runtime closure member | exact file SHA-256 + schema ID/version | F09 rejects open objects, private fields, wrong algorithm/encoding; F18 records digest |
| F02 | F01 | R3G1 status vocabulary/link rules | closed YAML schema bytes | F05、F08、F09、F12、F14、fresh R3 | production runtime closure member | exact digest + schema ID/version | F09 rejects unknown status, missing material digest, invalid UTC fields |
| F03 | F01 | human-authorized stable `kid` and raw 32-byte public inputs; no private input | canonical material JSON+LF | F05 directly; six callers indirectly through bound codec | production runtime closure + configuration semantic asset | file digest, semantic digest, each raw-key digest, ordered kid set | schema/canonical/raw digest checks; tamper shadow rejected; evidence F18 |
| F04 | F02、F03 | material exact digest, same kid set, fixed status/domain/UTC contract | canonical status JSON+LF | F05 directly; six callers indirectly | production runtime closure + configuration semantic asset | file digest, referenced F03 digest, per-record semantic identity | set equality/status/time/domain/material-link checks; tamper shadow rejected |
| F05 | F01–F04 | fixed module-relative schemas/assets, existing common/signing at audited digests | frozen `LoadedPublicTrust`, bound codec, freeze identity | C01–C06、F09、F10、fresh R3 | production runtime closure member | file/callable digest + four input digests + semantic payload digest | production fixed-path load repeated exact-match; temp shadow mutations; six binding leaves; F18 |
| F06 | G00 | this Plan's 21 groups and A1 claim ceiling | closed requirements YAML | F08、F09、F10、F11、F14 | test-only dependency | exact digest/version/profile | F08 enumerates every group; F09 proves no group omitted; F19 correlates |
| F07 | F06 | leaf/result/completeness field contract | closed manifest schema | F08、F09、F10、F11、F14 | test-only dependency | exact schema digest | independent schema validation of F14; unknown fields/duplicates rejected |
| F08 | F01–F07、F15 | frozen requirements, schemas/assets/loader, fixture recipes and six caller inventory | canonical F14 bytes only; no project write | F10 bootstrap; controller persists F14 | build-only dependency | file/callable digest + input digest set | two isolated builds exact-match; F09 validates leaves and coverage; evidence F18 |
| F09 | F01–F07、F15、F16 | implementation/control bytes, existing callers, F17 ledger, no-content temp shadows | canonical F18 verification payload only | F10 invokes; controller persists F18; F11 consumes | test-only verification code | exact file/callable digest | implementation manifest hash; self-described modes rejected; result must correlate F14/F17 |
| F10 | F05–F09、F15、F16 | F12/F13/F14, no-content recipes, fixed clock and dedicated seed | F17 append-only rows; invokes F09/F11 | sole future controller | test-only dependency | exact file/callable digest and authorized phase identity | only manifest leaves execute; duplicate/missing/extra terminal rejected; F18 verifies |
| F11 | F06、F07、F09、F10 | F12–F18 exact bytes | canonical F19 and F20 bytes, separately | controller persists F19 then F20 | build-only dependency | exact file/callable digest | two-build exact match; counts mechanically derived; no claim above A1 |
| F12 | D00、F01–F11、F15、F16 | Plan external digest, Audit digest, reconciliation digest copied from this Plan's frozen source block, all bundle/read-only/future scope states | canonical implementation manifest | F13、F14、F18、F19、F20、future Gate | control freeze; not production payload | exact file digest; every member path/digest/classification | F09 compares all listed files/read-only baselines/absent-to-created transitions; reconciliation file itself is not added to future read scope; F18 |
| F13 | D00、F12 | explicit future human authorization, fixed clock, Profile/domain, public-input authorization | canonical execution plan | F10、F14、F17–F20 | control freeze; not production payload | plan/audit/authorization/scope/key-input/fixed-clock identities | F09 exact-field/cross-digest check; absent authorization blocks before F14/F17 |
| F14 | D00、F01–F08、F12、F13、F15、F16 | F08 deterministic expansion inputs | canonical leaf manifest with actual N | F10、F17–F19 | test-only freeze | exact digest + schema/requirements/fixture/caller input digests | two F08 builds exact-match; F09 validates N leaves and 21-group coverage |
| F15 | D00、F03、F04、F06、F16 | no-content recipes, test-only public derivations, precomputed public vectors and tamper instructions | canonical fixture catalog | F08–F10、F14、F17 | test-only; excluded production closure | exact digest; recipe IDs; no source/path payload | F09 rejects TEI/path/business/private leakage; all recipe IDs map to F14 leaves |
| F16 | D00、F06 | dedicated 32-byte test seed authorization; never formal public input | exactly 64 lowercase hex chars + LF | F09/F10 test shadows only | test-only; explicitly excluded production/public trust identity | file digest recorded only; seed bytes never copied to evidence/report | permission/read-scope check; F09 proves F03 public key differs and F18/F19/F20 contain no seed |
| F17 | D00、F10、F13–F16 | actual F14 leaves | one terminal JSON line per leaf | F09/F11 | test-only evidence | exact byte length, last sequence, full digest, unique leaf IDs | F09 requires discovered=executed=terminal=evidence-complete=N; no duplicate/extra/unknown |
| F18 | D00、F05、F09、F12–F14、F17 | independent recomputation of assets/loader/callers/scope/counts | canonical A1 verification evidence | F11/F19/F20 | test-only A1 evidence | exact digest + all verified subject digests | producer F09 cannot write other paths; controller persists once; F11 only aggregates PASS truth |
| F19 | D00、F11–F14、F17、F18 | manifest, ledger, evidence and scope deltas | canonical mechanical aggregate | F11/F20 and external reviewer | test-only evidence | exact digest + manifest/ledger/evidence digests | all counts derived; failed/skipped/unknown/timeout zero required for PASS |
| F20 | F11–F13、F19 | final aggregate and action ledger | Markdown result without self-digest | external phase handoff; fresh R3 replan input | not production closure; graph-external result identity | external handoff SHA-256 only | F11 deterministic two-build exact match; facts must equal F19; no implementation self-authorization |

```yaml
future_file_role_mapping_complete: 20
unresolved_file_role_count: 0
unapproved_future_file_count: 0
```

### 6.3 Canonical encoding and closed artifact contracts

No 21st file is available for additional control schemas. Therefore F06 is the versioned source for the closed field contracts below, F07 is the dedicated F14 manifest schema, and F09 must independently enforce both. This allocation is part of the unique F06/F07/F09 role mapping, not an implementation-time choice.

| Artifact | Exact encoding | Required closed contract |
| --- | --- | --- |
| F01/F02/F06/F07 | UTF-8 YAML, one safe document, no custom tag/anchor/alias/merge/duplicate key/implicit timestamp/float | schema/requirements version, artifact class, Profile, closed fields and no unknown key |
| F03/F04/F12–F15/F18/F19 | compact canonical JSON with sorted keys, no float/duplicate key/BOM, exactly one trailing LF | artifact-specific required fields below; no self file digest |
| F16 | exactly 64 lowercase hexadecimal characters plus one LF | decodes to exactly 32 bytes; test-only classification and external file digest |
| F17 | UTF-8 JSONL; each line is one compact canonical JSON object plus LF | strictly increasing sequence; one unique terminal per F14 leaf; append-only until sealed |
| F20 | deterministic UTF-8 Markdown with LF line endings | exact facts mechanically rendered from F19; no self digest or hand-edited PASS |

F06 must define at least these field sets:

- **F12 implementation manifest**：artifact/version/suite/Profile/phase IDs；Plan/Audit/source digests；0/20/7 scope sets；F01–F11/F15/F16 path/digest/classification；all existing read-only baselines；16 R2 baselines；producer identities；unexpected/missing paths；no self digest。
- **F13 execution plan**：artifact/version/suite/Profile；exact Phase 2-G-R3G3 ID/kind；explicit authorization reference and digest；Plan/Audit/F12 digests；fixed UTC epoch；trust domain；human-authorized public-input identity without private bytes；read/write/forbidden sets；implementation/test status initialized but not pre-passed。
- **F15 fixture catalog**：artifact/version/suite/Profile；recipe IDs；requirement group IDs；test-shadow material/status recipes；precomputed public vectors if authorized；expected blocker/side-effect ceiling；F16 digest reference but no seed bytes；no path/source/business payload。
- **F17 attempt rows**：sequence、leaf ID、group ID、caller ID where applicable、started/terminal flags、result/blocker、evidence-complete boolean、side-effect counts、fixed clock、F14 digest、previous-row digest；no private bytes。
- **F18 verification evidence**：subject digests、schema/canonical/loader checks、21-group coverage、six-caller bindings、R2 baseline check、scope delta、private exclusion、actual N reconciliation and overall result。
- **F19 aggregate**：F12–F18 digests；manifest/discovered/executed/evidence-complete/pass/fail/skip/unknown/timeout counts；scope/R2/other-gap/private/caller counts；A1-only claim fields；fresh R3 replan required；implementation and R3 authorization false。
- **F20 result**：final status、gap/role/Profile、actual file/directory/caller counts、before/after digests、actual manifest counts、R2/scope/forbidden/TEI/Candidate/model/business ledgers、fresh R3 requirements and no automatic next execution。

F09 rejects any missing/extra field, self-digest, noncanonical encoding or cross-file mismatch. F11 cannot relax F06 contracts.

## 7. Implementation dependency graph

### 7.1 Nodes and direct dependencies

G00 is the future implementation authorization/preflight Gate. D00 is the single directory-hierarchy materialization. Each F node creates exactly the file mapped in §6. Direct dependency cardinalities are explicit so the edge count is mechanically checkable.

| Node | Direct dependencies | Edge count |
| --- | --- | ---: |
| G00 | none | 0 |
| D00 | G00 | 1 |
| F01 | G00 | 1 |
| F02 | F01 | 1 |
| F03 | F01 | 1 |
| F04 | F02, F03 | 2 |
| F05 | F01, F02, F03, F04 | 4 |
| F06 | G00 | 1 |
| F07 | F06 | 1 |
| F16 | D00, F06 | 2 |
| F15 | D00, F03, F04, F06, F16 | 5 |
| F08 | F01, F02, F03, F04, F05, F06, F07, F15 | 8 |
| F09 | F01, F02, F03, F04, F05, F06, F07, F15, F16 | 9 |
| F10 | F05, F06, F07, F08, F09, F15, F16 | 7 |
| F11 | F06, F07, F09, F10 | 4 |
| F12 | D00, F01, F02, F03, F04, F05, F06, F07, F08, F09, F10, F11, F15, F16 | 14 |
| F13 | D00, F12 | 2 |
| F14 | D00, F01, F02, F03, F04, F05, F06, F07, F08, F12, F13, F15, F16 | 13 |
| F17 | D00, F10, F13, F14, F15, F16 | 6 |
| F18 | D00, F05, F09, F12, F13, F14, F17 | 7 |
| F19 | D00, F11, F12, F13, F14, F17, F18 | 7 |
| F20 | F11, F12, F13, F19 | 4 |
| **Total** | 22 nodes | **100** |

### 7.2 Topological proof

唯一 implementation order：

```text
G00
-> D00
-> F01 -> F02 -> F03 -> F04 -> F05
-> F06 -> F07 -> F16 -> F15
-> F08 -> F09 -> F10 -> F11
-> F12 -> F13 -> F14
-> F17 -> F18 -> F19 -> F20
```

Every dependency of a node appears earlier in this order. Therefore：

```yaml
dependency_node_count: 22
dependency_edge_count: 100
dependency_cycle_count: 0
unresolved_dependency_count: 0
unique_topological_execution_order: true
```

The arrow chain is the unique authorized creation order, not a claim that each adjacent pair is the only semantic dependency; the complete 100 direct edges are the §7.1 dependency lists.

## 8. Twenty-two-node future implementation sequence

| Phase | Single objective | Exact write set | Preconditions | Independent verification before next phase | Fail-closed result |
| --- | --- | --- | --- | --- | --- |
| G00 | Prove future authority and baselines before any write | none | R3G1 PASS; this Plan PASS and external digest match; explicit Phase 2-G-R3G3 authorization; 20 files/7 dirs absent; R2 16/16 hashes; human-authorized public input; no ambiguity/regression | controller read-only preflight emits no project artifact | `BLOCKED_R3G07_IMPLEMENTATION_GATE_NOT_SATISFIED` |
| D00 | Materialize exact closed suite hierarchy | D01–D07 only | G00 PASS | exact seven paths, parent/child allowlist, no unexpected directory | `BLOCKED_R3G07_SCOPE_VIOLATION` |
| I01 | Freeze public-material schema | F01 only | G00 | closed-schema static verification and exact digest | `BLOCKED_R3G07_PUBLIC_MATERIAL_SCHEMA_INVALID` |
| I02 | Freeze key-status schema | F02 only | F01 accepted | closed status/link/time vocabulary verification | `BLOCKED_R3G07_KEY_STATUS_SCHEMA_INVALID` |
| I03 | Materialize immutable public bytes | F03 only | F01; approved public input; no private input | schema, canonical bytes, kid order/uniqueness, decoded raw digest | `BLOCKED_R3G07_PUBLIC_MATERIAL_INVALID` |
| I04 | Materialize immutable status registry | F04 only | F02/F03 | schema, exact F03 digest link, equal kid set, status/time/domain checks | `BLOCKED_R3G07_KEY_STATUS_REGISTRY_INVALID` |
| I05 | Implement fixed-path loader/freeze role | F05 only | F01–F04; common/signing digests match | AST/import/interface check; deterministic repeated load; no override inputs | `BLOCKED_R3G07_PUBLIC_TRUST_LOADER_INVALID` |
| I06 | Freeze requirement groups | F06 only | G00 | closed 21-group ID set and A1-only claim review | `BLOCKED_R3G07_TEST_REQUIREMENTS_INVALID` |
| I07 | Freeze manifest schema | F07 only | F06 | closed leaf/count/evidence schema validation | `BLOCKED_R3G07_TEST_MANIFEST_SCHEMA_INVALID` |
| I08 | Create dedicated test-only seed | F16 only | D00/F06; test-only authority | exact 64 lowercase hex+LF, permission/scope, differs from formal F03 key | `BLOCKED_R3G07_TEST_PRIVATE_BOUNDARY_INVALID` |
| I09 | Freeze no-content fixture recipes | F15 only | F03/F04/F06/F16 | canonical catalog, no TEI/path/business payload, no production private material | `BLOCKED_R3G07_FIXTURE_CATALOG_INVALID` |
| I10 | Implement deterministic leaf builder | F08 only | F01–F07/F15 | two OS-temp builds exact-match; builder has no project write | `BLOCKED_R3G07_MANIFEST_BUILDER_INVALID` |
| I11 | Implement independent verifier | F09 only | F01–F07/F15/F16 | static interface/mode inspection; implementation manifest later freezes exact bytes | `BLOCKED_R3G07_VERIFIER_INVALID` |
| I12 | Implement sole controller/runner | F10 only | F05–F09/F15/F16 | static write allowlist and no-content-only inspection | `BLOCKED_R3G07_RUNNER_INVALID` |
| I13 | Implement mechanical result generator | F11 only | F06/F07/F09/F10 | two synthetic in-memory inputs yield exact same bytes; no direct project write | `BLOCKED_R3G07_RESULT_GENERATOR_INVALID` |
| I14 | Freeze implementation bundle | F12 only | D00; F01–F11/F15/F16 accepted | F09 independently hashes all bundle/read-only/scope identities | `BLOCKED_R3G07_IMPLEMENTATION_MANIFEST_INVALID` |
| I15 | Freeze authorized execution identity | F13 only | F12; explicit authorization/fixed clock/public input identities | F09 cross-checks Plan/Audit/manifest/authorization digests | `BLOCKED_R3G07_EXECUTION_PLAN_INVALID` |
| I16 | Materialize actual test leaves | F14 only | F01–F08/F12/F13/F15/F16 | two F08 builds exact-match; F09 schema/group/leaf correlation | `BLOCKED_R3G07_TEST_MANIFEST_INVALID` |
| I17 | Execute only manifest leaves | F17 only | F10/F13–F16; all start digests match | each F14 leaf exactly one terminal row; no extra/duplicate/unknown | `BLOCKED_R3G07_ATOMIC_TEST_EXECUTION_FAILED` |
| I18 | Independently verify implementation/evidence | F18 only | F05/F09/F12–F14/F17 | F09 recomputes every subject; controller persists returned bytes once | `BLOCKED_R3G07_VERIFICATION_FAILED` |
| I19 | Mechanically aggregate actual counts | F19 only | F11–F14/F17/F18 | F11 two-build exact match; counts derived from F14/F17/F18 | `BLOCKED_R3G07_AGGREGATE_FAILED` |
| I20 | Generate phase result | F20 only | F11–F13/F19; all PASS predicates true | two-build exact match; report facts equal F19; no self-digest | `BLOCKED_PORTABLE_RUNTIME_ROLE_GAP_R3G07_REPAIR_FAILED` |

Each file creation is one phase. A failed phase leaves every later path absent and cannot authorize retry, alternate layout, other gap repair or scope expansion. Retry requires a new explicit authorization if the failure occurs after any create-once artifact was committed.

## 9. Deterministic verification contract

### 9.1 Requirement groups

F06 must define exactly these 21 requirement groups. A group is not a test count; F08 expands it into actual leaves from the frozen caller/key/status/vector inventory.

| Group | Required behavior |
| --- | --- |
| PT-01 | trusted active test-shadow key accepted by exact F05 loader code + existing `JWSCodec.verify` |
| PT-02 | unknown `kid` rejected |
| PT-03 | revoked key rejected |
| PT-04 | expired status and validity-window expiry rejected |
| PT-05 | disabled key rejected |
| PT-06 | not-yet-valid key rejected |
| PT-07 | wrong algorithm or trust domain rejected |
| PT-08 | public material exact bytes/raw-key digest tamper rejected |
| PT-09 | status registry bytes/material-digest link tamper rejected |
| PT-10 | wrong trust identity, duplicate kid or unequal material/status key set rejected |
| PT-11 | loader file/callable/input identity mismatch rejected |
| PT-12 | each of C01–C06 wrong/shared-codec binding mismatch rejected |
| PT-13 | deterministic lookup and freeze identity reproducible across repeated loads |
| PT-14 | consumer cannot provide path/bytes/dict/store/environment/network trust input to the public loader |
| PT-15 | JWS artifact `kid` cannot embed or self-select untrusted public material |
| PT-16 | test-only private seed excluded from F03/F04, production closure, evidence, aggregate and report |
| PT-17 | noncanonical JSON, duplicate JSON key, unknown field, BOM, float and wrong Profile rejected |
| PT-18 | RangeBroker/BoundedReader/FormalLoader trust failures precede source/path/FD actions |
| PT-19 | R2 16 canonical assets unchanged; Authorization V2 remains without signature/kid/public-key fields |
| PT-20 | two schemas, two assets, loader, signing and six callers independently reproduce closure identities |
| PT-21 | scope violation, unexpected file, unresolved dependency and other role-gap modification counts are zero |

### 9.2 Leaf enumeration and actual counts

F08 must enumerate leaves from F06 + F07 + actual F01–F05 identities + F15 recipes + C01–C06 inventory. It must not contain a fixed expected leaf number. F10 executes only F14 leaves. F11 mechanically derives:

```yaml
manifest_leaf_count: N
discovered: N
executed: N
evidence_complete: N
passed: N
failed: 0
skipped: 0
unknown: 0
timeout: 0
```

`N` is assigned only by the committed F14 exact bytes and independently reconciled with F17/F18. R3G2 test counts are therefore not preset.

### 9.3 Test-shadow rule

Tamper/status/private-key vectors run only in controller-owned OS temporary directories. To preserve the public loader's no-override contract, the runner copies the exact loader/support bytes into a temporary shadow package whose module-relative assets are synthetic copies generated from F15/F16. The public callable signature remains unchanged; no project file is modified. Temporary shadows:

- contain no TEI, Candidate artifact, live Registry, source path or business output;
- are destroyed after each leaf;
- never enter production/runtime closure;
- cannot be cited as formal public trust material;
- may use F16 only within test/control scope.

Production F03/F04 loading is separately verified at exact project paths. The formal public key's private counterpart is never required or stored by Runtime. If a positive formal-key JWS vector is supplied, it must be a precomputed public test vector inside F15 whose signer custody remains external; no private material may be added.

## 10. Public vs private material boundary

```yaml
runtime_public_material:
  files:
    - "runtime_capability_prototype/contracts/portable_public_trust_material_v1.json"
    - "runtime_capability_prototype/contracts/portable_public_key_status_registry_v1.json"
  private_key_dependency: false
  caller_supplied_material_allowed: false
  network_material_allowed: false

test_only_private_material:
  file: "runtime_capability_prototype/r3g07_portable_suites/R3G07PS-20260812-001/fixtures/r3g07_test_signing_key_ed25519_seed.hex"
  classification: "test_only_dependency"
  distinct_from_formal_public_trust: true
  production_closure_membership: false
  public_trust_identity_membership: false
  evidence_or_report_bytes_allowed: false
```

F16 is never a production signing key, rotation key or Runtime secret-management mechanism. R3G-07 does not implement PKI、CA、certificate chain、network key service、online rotation、HSM或production secret management。

## 11. R2 immutable semantic boundary

R2 remains：

```text
PASS_PORTABLE_AUTHORIZATION_SCHEMA_V2_IMPLEMENTED
```

Future implementation must preserve all 16 canonical R2 asset digests and these semantics：

- Authorization V2 exact bytes contain no self digest, signature, `kid` or public key；
- Registry custody exact bytes remain the sole authorization truth；
- immutable Registry identity remains separated from mutable state；
- `unconsumed -> spent | revoked | expired` and all mint/preparation/activation state transitions remain one-way CAS；
- authorization/capability/delivery replay and nonce/one-shot handles remain unchanged；
- existing typed contexts and consumer/output authorization semantics remain unchanged；
- historical R2 suite-local keys/evidence remain test-only and are not promoted into F03/F04。

```yaml
r2_assets_checked_before_planning: 16
r2_asset_digest_mismatches_before_planning: 0
r2_assets_allowed_to_modify: 0
r2_semantic_risk_artifacts: []
r2_semantic_regression_count: 0
```

If any future step requires a new Authorization V2 field, altered Registry truth/consume/replay semantics, modification of an R2 asset, or promotion of an R2 test key：

```text
BLOCKED_R2_SEMANTIC_REGRESSION_DISCOVERED
```

## 12. Fresh R3 closure/freeze contract

R3G-07 implementation PASS does not equal R3 PASS. The old R3P does not contain these 20 paths and cannot authorize the changed tree.

### 12.1 Production/runtime closure members

Fresh R3 must add and freeze：

1. F01 exact schema identity；
2. F02 exact schema identity；
3. F03 exact file/semantic/per-public-key identity；
4. F04 exact file/material-reference/per-status identity；
5. F05 exact file and `load_portable_public_trust` callable identity；
6. existing `signing.py` exact digest and `KeyRecord`/`TrustStore`/`JWSCodec.verify` identities；
7. C01–C06 exact file/qualname identities and their shared F05 codec/freeze configuration edges；
8. `CTDE-PORTABLE-DEV-1`、`ctde-portable-runtime`、fixed-clock/UTC semantics and private/test exclusion identity。

### 12.2 Control/test/build nodes

Fresh R3 graph must enumerate F06–F19 and classify each exactly as §6.1. They enter component/control freeze where applicable but never the production payload. F16 must carry an explicit negative edge proving exclusion from production/public trust. F20 is an external result input to fresh replan, not a production closure member.

Seven directories enter structural write-scope identity, not file-digest membership. All new project files must be accounted for; a new path not in this Plan forces a new scope audit/plan.

### 12.3 Required sequence after R3G-07 PASS

```text
R3G-07 implementation + manifest-enumerated deterministic verification PASS
  -> minimal embedded-role mapping for R3G-03
  -> minimal embedded-role mapping for R3G-04
  -> fresh R3 file-level replan over changed Runtime/control tree
  -> new explicit human R3 execution authorization referencing fresh Plan SHA-256
```

R3G-01、R3G-02、R3G-05、R3G-06 remain deferred/stage-scoped exactly as Role Gap Plan states. This Plan does not implement or resolve them. R3G-03/R3G-04 are not modified here; only their later required mapping sequence is preserved.

```yaml
old_r3p_execution_allowed: false
fresh_r3_replan_required: true
minimal_embedded_role_mapping_required: true
r3g01_to_r3g06_modified_by_this_plan: 0
```

## 13. Future implementation hard Gate

Before G00 may PASS, all conditions must be true simultaneously：

1. `PASS_PORTABLE_RUNTIME_PUBLIC_TRUST_BINDING_SCOPE_AUDIT` and Audit digest exactly `e5cd250e...1f7`；
2. this Plan's frozen source block records `PASS_R3G2_PHASE_KIND_CONTRACT_RECONCILIATION` and digest exactly `0bcde11b...7e8`；the future authorization may repeat that external identity, but the reconciliation file is not added to §2.4 future read authority；
3. `PASS_PORTABLE_RUNTIME_PUBLIC_TRUST_BINDING_ATOMIC_PLAN` and this Plan's external exact SHA-256 matches the future authorization；
4. future command exact `next_phase_id=Phase 2-G-R3G3`；
5. future command exact `next_phase_kind=r3g07_atomic_implementation_and_deterministic_verification_only`；
6. explicit human future implementation authorization exists and cites the Plan digest；
7. all 20 creatable files and all 7 creatable directories are absent；
8. all read-only current digests match §2.5, including all 16 R2 canonical assets；
9. approved human public input supplies stable `kid` and raw 32-byte Ed25519 public material without project private key；
10. Profile/domain/fixed clock are exactly `CTDE-PORTABLE-DEV-1` / `ctde-portable-runtime` / authorized UTC epoch；
11. unresolved scope ambiguity、unresolved dependency、R2 semantic regression and required scope expansion are all zero；
12. forbidden paths remain inaccessible under §2.6 and write policy remains default-deny；
13. no other R3G gap is included；
14. implementation still requires zero existing-file modifications。

Any failure produces `BLOCKED_R3G07_IMPLEMENTATION_GATE_NOT_SATISFIED` before D00 or I01. This Plan PASS cannot be interpreted as meeting condition 6.

## 14. PASS acceptance for future Phase 2-G-R3G3

Future F20 may report `PASS_PORTABLE_RUNTIME_ROLE_GAP_R3G07_REPAIRED` only when：

- 0 existing files modified；
- 20/20 approved files created with their exact roles；
- 7/7 approved directories created and no others；
- F03/F04/F05 implement the approved immutable trust/status/loader responsibility；
- 6/6 exact callers have approved-composition binding evidence；
- manifest actual N equals discovered/executed/evidence-complete/passed；
- failed/skipped/unknown/timeout are zero；
- R2 modifications/regressions are zero；
- other R3G gap modifications are zero；
- scope violations and forbidden-path accesses are zero；
- private/test material exclusion is proven；
- A1 / Development / non-certified is the highest claim；
- fresh R3 replan remains required and R3 remains unauthorized。

Otherwise F20 must report：

```text
BLOCKED_PORTABLE_RUNTIME_ROLE_GAP_R3G07_REPAIR_FAILED
```

## 15. R3G2 acceptance and boundary terminal

### 15.1 Acceptance predicates

```yaml
canonical_phase_kind_exact_match: true
r3g1_scope_reused_without_change: true
future_mutable_existing_files: "0/0"
future_files_uniquely_mapped: "20/20"
future_directories_uniquely_mapped: "7/7"
actual_callers_uniquely_bound: "6/6"
dependency_cycle_count: 0
unresolved_file_role_count: 0
unresolved_implementation_ambiguity_count: 0
scope_expansion_required_count: 0
r2_semantic_regression_count: 0
future_test_contract_deterministic: true
fresh_r3_replan_requirements_explicit: true

final_status: "PASS_PORTABLE_RUNTIME_PUBLIC_TRUST_BINDING_ATOMIC_PLAN"
```

### 15.2 This-stage action ledger

本阶段唯一创建：

```text
PORTABLE_RUNTIME_PUBLIC_TRUST_BINDING_PLAN.md
```

```yaml
created_files:
  - "PORTABLE_RUNTIME_PUBLIC_TRUST_BINDING_PLAN.md"
modified_existing_files: []

existing_file_modification_count: 0
runtime_modification_count: 0
r2_asset_modification_count: 0
runtime_test_count: 0
implementation_execution_count: 0
r3_execution_count: 0
r4_execution_count: 0
candidate_run_count: 0
model_call_count: 0
english_tei_content_read_count: 0
greek_tei_content_read_count: 0
business_output_count: 0

future_public_trust_schema_files_created: 0
future_public_key_assets_created: 0
future_key_status_registry_assets_created: 0
future_trust_loader_files_created: 0
future_caller_files_modified: 0
future_verifiers_created: 0
future_test_manifests_created: 0
future_test_runners_created: 0
future_implementation_results_created: 0
```

This Plan stops here. It does not automatically enter Phase 2-G-R3G3, minimal embedded-role mapping, fresh R3 replan, R3, R4 or Candidate.
