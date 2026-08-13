# Classic-to-Drama Engine：Portable Runtime Public Trust Binding Scope Audit

> 项目：Classic-to-Drama Engine  
> 阶段：Phase 2-G-R3G1  
> phase_kind：`read_only_scope_audit`  
> 日期：2026-08-12  
> 最终状态：`PASS_PORTABLE_RUNTIME_PUBLIC_TRUST_BINDING_SCOPE_AUDIT`  
> 当前效力：`scope_audit_only / runtime_unchanged / tests_not_executed / r3_not_authorized`  
> Profile：`CTDE-PORTABLE-DEV-1`  
> 最高可声明证据：`A1 / Development / non-certified`  
> Candidate Analysis：`BLOCKED`

## 0. 最终结论

本审计只回答 `R3G-07-IMMUTABLE-PUBLIC-TRUST-KEY-STATUS` 的未来原子实现范围，不实现任何 schema、asset、loader、binding、verifier、runner 或 key。

当前真实实现已经具有 Ed25519/JWS 的内存类型、签名与验证算法：`KeyRecord`、`TrustStore`、`SigningKey`、`JWSCodec`。但是所有可用 verification key 都由 legacy 或 R2 test runner 在进程内临时生成；没有独立、create-once、可复核的 public trust material、key-status registry、loader 或 freeze identity。当前高层 runner 可以自行选择 `TrustStore`，所以实际接受语义由调用者注入的可变进程内对象决定。

未来最小修复可以在不修改任何现有文件、尤其不修改 16 个 R2 immutable assets 的前提下完成：

1. 在现有 `contracts/` 中创建两个 closed schema、一个 immutable public-material asset 和一个 immutable key-status registry asset；
2. 在现有 `runtime/ctde_runtime/` package 中创建唯一 `public_trust.py` loader/resolver；
3. loader 从 exact canonical asset bytes 重建现有 `KeyRecord -> TrustStore -> JWSCodec`，并携带 material/status/schema/loader 的 freeze identity；
4. 六个真实 Runtime verifier caller 继续使用已经存在的 `codec: JWSCodec` 注入缝，不修改 caller；future atomic verifier 必须实例化这些真实 caller，并证明它们持有同一个 loader-produced codec/freeze identity；
5. 正式 Runtime 只依赖 public material。Synthetic test 的 private seed位于专用 test-only fixture，不能进入 production/runtime closure、public trust asset、component public snapshot或result evidence；
6. `authorization_schema_v2.yaml` 不增加签名字段。Authorization V2 artifact 当前且继续以 exact bytes + external Registry identity 获得 authority；R3G-07 只关闭已有 signed-object/event verification 的 public trust identity，不改变 R2 业务授权语义。

```yaml
phase: "Phase 2-G-R3G1"
phase_kind: "read_only_scope_audit"
final_status: "PASS_PORTABLE_RUNTIME_PUBLIC_TRUST_BINDING_SCOPE_AUDIT"

gap_id: "R3G-07-IMMUTABLE-PUBLIC-TRUST-KEY-STATUS"
runtime_role: "immutable public trust material / key-status registry"
primary_classification: "E.missing_freeze_identity"
secondary_classifications:
  - "C.missing_contract_or_schema_binding"
  - "B.missing_runtime_binding"
dependencies: []
blocks_r3: true

inspected_runtime_files_count: 25
trust_related_files_found_count: 13
actual_runtime_callers_count: 6
current_trust_model: "ephemeral in-memory caller-supplied TrustStore; no persistent public trust identity"
current_key_status_capability: "in-memory only: unknown/domain/status/validity checks exist; no immutable registry asset"
embedded_role_candidate: "runtime/ctde_runtime/signing.py evaluated but not selected; independent public_trust.py selected"

future_mutable_existing_files_count: 0
future_creatable_files_count: 20
future_creatable_directories_count: 7
implementation_dependencies_count: 5
closure_binding_requirements_count: 8
unresolved_scope_ambiguity_count: 0
r2_semantic_regression_count: 0

r3g2_ready: true
r3_replan_required_after_repair: true
r3_execution_authorized: false
r4_execution_authorized: false
candidate_execution_authorized: false
```

## 1. 正式合同恢复与写前基线

### 1.1 R3G-07 唯一合同

从 `PORTABLE_RUNTIME_ROLE_GAP_RESOLUTION_PLAN.md` 恢复：

```yaml
gap_id: "R3G-07-IMMUTABLE-PUBLIC-TRUST-KEY-STATUS"
runtime_role: "immutable public trust material / key-status registry"
expected_responsibility: >-
  Freeze kid, algorithm, status, trust domain, validity and exact public-key bytes
  digest for every verifier-reachable trust record; define private-key custody,
  producer authority, runtime loader/binding, and one identity shared by component
  freeze and execution snapshot.
primary_classification: "E.missing_freeze_identity"
secondary_classifications:
  - "C.missing_contract_or_schema_binding"
  - "B.missing_runtime_binding"
dependencies: []
blocks_r3_under_current_r3p: true
requires_pre_r3_repair_after_adjudication: true
scope_status_at_entry: "scope_requires_additional_audit"
repair_sequence:
  - "Phase 2-G-R3G1 read_only_scope_audit"
  - "Phase 2-G-R3G2 atomic_plan"
  - "future implementation and dedicated verification"
```

本文件完成后只把 scope 状态关闭为：

```yaml
scope_status_after_audit: "scope_resolved_for_r3g2_planning"
implementation_authorized_by_this_audit: false
```

### 1.2 正式依据摘要

| 文件 | SHA-256 | 用途 |
| --- | --- | --- |
| `PORTABLE_RUNTIME_ROLE_GAP_RESOLUTION_PLAN.md` | `72f116ff0b93403961a045228706f9322deea008f41718acae6178b0780b8798` | R3G-07 authority、R3G1 closed scope、R3 re-entry Gate |
| `PORTABLE_RUNTIME_TRANSITIVE_CLOSURE_PLAN.md` | `f8ca07eaee1fff534e97bf4a0d037ba73a3c1838107e132f7c072b1fe05b39f5` | public trust freeze、actual callable roots、closure binding |
| `PORTABLE_AUTHORIZATION_SCHEMA_V2_PLAN.md` | `32513cdb2c004ea91c7d7208eb3a40901934dc80440af048b84701facf1bdbe9` | R2 business semantics、exact-bytes Registry authority、test-key boundary |
| `PORTABLE_AUTHORIZATION_SCHEMA_V2_IMPLEMENTATION_RESULT.md` | `b47c7280880af70325a5e5c45426951567390441ad4cd61465724fbb8eabcd06` | R2 actual implementation、51/51 PASS、16-file immutable boundary |
| `RUNTIME_ASSURANCE_PROFILE_DECISION.md` | `57471c85c57946f6ceb6da288301cc802533b09c137bfbe8e6e247dad57206e2` | Portable A1/non-certified 与 Hardened A3 分离 |
| `RUNTIME_CAPABILITY_REPAIR_PLAN.md` | `a2c52dbaecf3956cf4a2189abe5401f269d255e8099d3345985619be25be4213` | public-trust node type、private-key exclusion、R3 closure contract |

### 1.3 写前状态

```yaml
audit_target_before: "ABSENT"
runtime_file_count_by_directory_enumeration: 3062
runtime_directory_count_by_directory_enumeration: 1218
runtime_symlink_count_by_directory_enumeration: 0
r2_canonical_assets_checked: 16
r2_canonical_assets_digest_mismatches: 0
```

本阶段的 closed read authority 只允许读取 R3G Plan §8.2 明列的 exact files；因此本审计没有为追求一个新 Runtime 全树摘要而读取未列入该清单的 suite/registry payload。历史 Runtime tree digest `820afae1806d4cec398b54193574e62e1933c2e8745dfb570d00b969bd69fe43` 只作为 prior reference，不冒充本阶段重新读取全部 3,062 个文件得到的 current proof。

## 2. 当前 public-trust 基线

### 2.1 13 个 trust-related 文件／对象

`trust_related_files_found_count=13` 的口径：直接实现 signer/verifier/trust behavior 的文件，加上决定其当前 identity、测试边界或 R2 不签名语义所必需的 negative evidence。它不把每个含普通 digest 字段的文件都算作 trust object。

| relative_path | role | current implementation status | SHA-256 | classification | Portable Runtime reachable | mutable trust assumption |
| --- | --- | --- | --- | --- | --- | --- |
| `runtime_capability_prototype/runtime/ctde_runtime/signing.py` | `KeyRecord`、`TrustStore`、`SigningKey`、`JWSCodec` | 算法和内存状态检查已实现；无持久 loader/identity | `5c41a1601b9824715d17ae416513646575006a9207dedd26bb2036336e66cc36` | runtime | yes | yes：任意 caller 可构造 records/store |
| `runtime_capability_prototype/runtime/ctde_runtime/events.py` | signed event producer与两个 event verifier | signer/codec均由 caller 注入 | `808115293ec818eedd926e4ef63869a7d5f9eeb1dca26a6902c12850b4e7fd15` | runtime / R2 immutable | yes | yes：接受任意 injected codec |
| `runtime_capability_prototype/runtime/ctde_runtime/range_broker.py` | capability、broker attestation、envelope signer/verifier | legacy signed-object path使用 injected codec；V2 pure binding不验证authorization signature | `ef2be994b82f10f025411e1d074cda3d0336e352f063bb9162edbcaed105958a` | runtime / R2 immutable | yes | yes：constructor接受任意 codec/signer |
| `runtime_capability_prototype/runtime/ctde_runtime/bounded_reader.py` | envelope与broker-attestation verifier | `consume`通过 `self.codec.verify`解析两个JWS | `65c8f0a3af625c505fcdc05f7a754075e4829d2183931d71fa8c4dfdbf46f68c` | runtime / R2 immutable | yes | yes：constructor接受任意 codec |
| `runtime_capability_prototype/runtime/ctde_runtime/formal_loader.py` | signed formal-manifest verifier | `load`先验证JWS，再处理entries | `eb866084c8dc95c52b28118a2669314559d165e6b949cb0ff7edeb111c10e11d` | runtime | yes | yes：constructor接受任意 codec |
| `runtime_capability_prototype/runtime/ctde_runtime/read_audit.py` | signed component logs verifier、audit signer | `_verify_logs`把同一 codec交给 `SignedEventLog.verify` | `b5c8a9210c4f9f295351b32e3f2a5e310ad0531720ff886a9d84385ec1ab6b4d` | runtime / R2 immutable | yes | yes：constructor接受任意 codec/signer |
| `runtime_capability_prototype/runtime/run_suite.py` | legacy key generator、trust-store assembler、suite-local key snapshot producer | 每次run临时生成active/revoked/expired/production/unknown keys | `caf32bdb9c49ba78ee1671d41b62bc9eb8297343624ceb7afd562443a6794749` | legacy | no production reachability | yes：per-run随机identity |
| `runtime_capability_prototype/runtime/run_r2_portable.py` | R2 test A1 signer、controller signer和self-verifier | 两套Ed25519 private keys每次suite临时生成 | `ec1c86ed0f89a76b497dc9d48ff4fc092c5ff1e78d84fb3dff407a9040a4ca75` | test-only / R2 immutable | no production reachability | yes：per-run随机identity |
| `runtime_capability_prototype/runtime/build_manifest.py` | legacy KID/status/profile negative vector enumeration | 枚举unknown/revoked/expired/cross-root vectors；不提供trust asset | `78a206e28365cfe7d6caf677ef818ddaddb7db2b920cac535ea84d206205213d` | legacy build-only | no | no runtime identity |
| `runtime_capability_prototype/contracts/r2_portable_controller_terminal_schema_v1.yaml` | R2 test controller key/signature contract | 固定test key ID/algorithm；不含public bytes/status registry | `7b2a983750a903e43489854750d56d4f6fee31a8fb541615d8247e2bf90454ac` | test-only / R2 immutable | no | key ID fixed、material不固定 |
| `runtime_capability_prototype/contracts/authorization_schema_v2.yaml` | canonical Authorization V2 business contract | artifact含issuer approval reference/digest，但没有JWS、kid或verification key字段 | `f1d7c2e36e0d3072624609591eb8dfc20d0e42dce6accc8e87de730ec4478e33` | runtime contract / R2 immutable | yes | no embedded key；不得由R3G-07新增签名语义 |
| `runtime_capability_prototype/r2_portable_suites/R2PS-20260811-001/control/component_inputs.json` | R2 frozen input evidence | 冻结15项，但未列 `signing.py` 或独立trust asset | `ab75e95bc0cdef67fb60f6b04c9fe143e0a8e71b396c1ffe17a2473a59216b1a` | historical test-only | no | 证明R2不声称transitive trust closure |
| `runtime_capability_prototype/r2_portable_suites/R2PS-20260811-001/aggregate/r2_portable_results.json` | R2 controller public-key evidence | 保存本次suite临时controller public key hex；没有status/loader/future authority | `3941449585b1d7071f703c2858a3f72bbed929ef092f496ae3b30037900c4e61` | historical test-only | no | suite-local identity，不可复用为Runtime trust root |

### 2.2 当前内存 trust model

`signing.py` 的真实行为：

- `KeyRecord` 保存 `kid`、Ed25519 public key对象、`status`、integer `not_before`/`expires_at`与`trust_domain`；
- `TrustStore` 以 caller-provided list构造字典；没有schema、canonical bytes、duplicate-kid rejection、asset digest或producer identity；
- `TrustStore.get_active(kid, now)` 拒绝 unknown kid、trust-domain mismatch、任何非 `active` status和validity window外记录；
- `JWSCodec.verify`先要求header `alg=EdDSA`、exact `typ`、profile version与string `kid`，随后调用 `get_active`并用Ed25519 public key验证signature；
- current validity判断为 `not_before <= now <= expires_at`；R3G-07不能静默改变这个signed-key validity边界。

因此当前已经有**进程内 key-status decision**，但没有**immutable key-status registry identity**。现有状态表现为：

```yaml
unknown_kid: "rejected in memory"
trust_domain_mismatch: "rejected in memory"
status_active: "accepted only inside validity window"
status_revoked: "rejected because status != active"
status_expired: "legacy test models expiry by past validity window; any explicit non-active value is also rejected"
status_disabled: "not a current schema value; would be rejected only generically because status != active"
persistent_registry: false
registry_schema: false
registry_digest_identity: false
deterministic_loader: false
```

### 2.3 当前 key material 来源

| context | public material source | private material source | persistence | disposition |
| --- | --- | --- | --- | --- |
| legacy `run_suite.py` | `SigningKey.generate(...).record(...)` in memory | generated per suite in memory | public fields写入legacy suite snapshot；private不持久化 | legacy only |
| R2 A1 runtime events | one generated `R2P-A1-TEST-KEY` record | generated per suite in memory | public key不进入canonical Runtime asset | test-only |
| R2 controller ledger | `Ed25519PrivateKey.generate().public_key()` | generated per suite in memory | public hex只进入R2 aggregate | test-only |
| actual production/Portable callable roots | caller must inject `JWSCodec` | no formal acquisition path | none | gap |

当前 key material 不是hard-coded public key、config-supplied registry或external file；它是 `generated_per_test / generated_per_legacy_suite`。JWS artifact只携带 `kid`，不携带public key。实际consumer不会从artifact自动信任key，但higher-level caller可以自行选择任意`TrustStore`，这仍不满足immutable public trust role。

## 3. 当前 verification chain

### 3.1 Authorization V2 artifact chain

当前 Portable Authorization V2 本身没有签名验证链：

```text
authorization_v2 exact YAML bytes
  -> authorization_v2.load_authorization_v2
  -> schema + semantic validation
  -> AuthorizationRegistry.register_authorization_v2
  -> Registry-custody exact bytes BLOB + external SHA-256/size/identity
  -> typed contexts + one-time CAS state machine
```

`authorization_schema_v2.yaml` 没有 `signature`、`kid`、verification key或embedded public key字段。其 `issuer.approval_evidence_ref/sha256` 是业务批准证据引用，不是一个由当前Runtime执行的JWS verification contract。

结论：

```yaml
authorization_artifact_signature_verification_exists: false
authorization_artifact_embeds_key: false
authorization_consumer_selects_signature_key: false
r2_semantic_defect_discovered: false
```

为 Authorization V2 新增强制签名会改变R2 business semantics，属于 `R2_semantic_risk=true`；本R3G-07布局明确禁止该修改。

### 3.2 Signed-object/event chain

当前真实JWS chain为：

```text
signed capability / broker envelope / audit-event / formal-manifest JWS
  -> protected header kid
  -> actual caller invokes JWSCodec.verify
  -> JWSCodec.trust_store.get_active(kid, now)
  -> in-memory KeyRecord
  -> trust-domain + status + validity decision
  -> Ed25519PublicKey.verify(signature, signing_input)
  -> caller-specific typ / issuer / audience / TTL / correlation checks
```

Key resolution authority当前是被注入codec中的in-memory `TrustStore`。没有registry signature verification；也没有trust material file、status file或loader signature。未来R3G-07采用exact-bytes digest/freeze，而不是为local static assets再引入递归签名authority。

## 4. 六个真实 Runtime caller binding

`actual_runtime_callers_count=6` 只统计R3P approved Runtime callable roots中直接或确定性间接调用 `JWSCodec.verify` 的callable；legacy/test runner另列，不进入production caller count。

| caller path | callable | current key-resolution behavior | future binding requirement | existing file modification required | exact reason |
| --- | --- | --- | --- | --- | --- |
| `runtime_capability_prototype/runtime/ctde_runtime/events.py` | `SignedEventLog.verify` | 接收caller传入的`codec`并逐token调用`codec.verify` | atomic verifier必须传入同一个loader-produced bound codec并核对freeze identity | false | 现有参数就是最小DI seam；修改会触碰R2 asset且无必要 |
| `runtime_capability_prototype/runtime/ctde_runtime/events.py` | `PortableA1EventLogV2.verify` | 接收caller传入的`codec`；R2 runner当前传入suite-localcodec | future production/Portable使用bound codec；R2 historical runner保持test-only不变 | false | 不重写R2 test identity或历史PASS |
| `runtime_capability_prototype/runtime/ctde_runtime/range_broker.py` | `RangeBroker.deliver` | constructor保存`self.codec`，在任何object open前验证capability JWS | future composer只能注入loader-produced bound codec；atomic negative vectors必须证明trust failure发生在open前 | false | constructor已有exact binding seam；文件是R2 immutable asset |
| `runtime_capability_prototype/runtime/ctde_runtime/bounded_reader.py` | `BoundedReader.consume` | constructor保存`self.codec`，验证envelope与broker attestation | future composer注入同一bound codec；atomic vectors必须在FD读取前fail closed | false | constructor已有exact binding seam；文件是R2 immutable asset |
| `runtime_capability_prototype/runtime/ctde_runtime/formal_loader.py` | `FormalLoader.load` | constructor保存`self.codec`，在任何formal entry open前验证manifest | future composer注入同一bound codec；negative vectors必须在path handling前拒绝 | false | constructor已有exact binding seam；独立role无需改loader业务逻辑 |
| `runtime_capability_prototype/runtime/ctde_runtime/read_audit.py` | `ReadAuditAggregator._verify_logs` | constructor保存`self.codec`并传给`SignedEventLog.verify` | aggregator与event verifier必须共享同一bound codec/freeze identity | false | constructor已有exact binding seam；文件是R2 immutable asset |

间接caller `RangeBroker.handle_request`、`ReadAuditAggregator.create_scope_attestation`和`create_closure_attestation`继续由上述direct callable闭合，不重复计数。

非production caller disposition：

| path / callable | classification | disposition |
| --- | --- | --- |
| `runtime/run_suite.py::SuiteRuntime.__init__` | legacy | 保持per-suite ephemeral keys；不得作为future Runtime binding |
| `runtime/run_suite.py::CaseHarness._execute_profile_case` | legacy | 只保留历史profile-vector evidence |
| `runtime/run_r2_portable.py::main` | test-only / R2 historical | 不改写；R2 event key继续与future Runtime trust隔离 |
| `runtime/run_r2_portable.py::ControllerLedger.verify_all` | test-only / R2 historical | 独立controller self-verification；不进入production trust role |

## 5. Future trust model 的唯一最小职责

### 5.1 Public material asset

`portable_public_trust_material_v1.json` 是create-once canonical JSON，至少包含：

```yaml
schema_version: "1.0.0"
artifact_class: "ctde_portable_public_trust_material"
assurance_profile_id: "CTDE-PORTABLE-DEV-1"
trust_domain: "ctde-portable-runtime"
canonicalization_id: "CTDE-PUBLIC-TRUST-JCS-1"
keys:
  - kid: "<approved stable ID>"
    jws_alg: "EdDSA"
    key_algorithm: "Ed25519"
    public_key_encoding: "raw-32-byte-lowercase-hex"
    public_key_hex: "<64 lowercase hex>"
    public_key_bytes_sha256: "<SHA-256 of decoded 32 raw bytes>"
```

Closed rules：object keys closed；`keys` non-empty、按`kid`排序、kid唯一；禁止private key、certificate、URL、network locator、embedded status、self digest、float与unknown field。Exact bytes为RFC 8785/JCS-compatible canonical JSON加一个LF；loader必须拒绝非canonical exact bytes。

### 5.2 Key-status registry asset

`portable_public_key_status_registry_v1.json` 是create-once canonical JSON，至少包含：

```yaml
schema_version: "1.0.0"
artifact_class: "ctde_portable_public_key_status_registry"
assurance_profile_id: "CTDE-PORTABLE-DEV-1"
trust_domain: "ctde-portable-runtime"
canonicalization_id: "CTDE-PUBLIC-TRUST-JCS-1"
trust_material_relative_path: "contracts/portable_public_trust_material_v1.json"
trust_material_file_sha256: "<exact material-file bytes SHA-256>"
records:
  - kid: "<exact matching material kid>"
    jws_alg: "EdDSA"
    key_algorithm: "Ed25519"
    status: "active | revoked | expired | disabled"
    trust_domain: "ctde-portable-runtime"
    not_before: "<RFC 3339 UTC Z>"
    expires_at: "<RFC 3339 UTC Z>"
```

Closed rules：records按kid排序且唯一；material/status kid集合必须完全相等；algorithm/domain必须逐record相等；`not_before <= expires_at`；loader将时间确定性转换为UTC epoch并保留现有`not_before <= now <= expires_at`验证边界。Unknown kid、non-active status、domain mismatch、algorithm mismatch、material digest mismatch、invalid time或asset/schema mismatch均fail closed。

`disabled` 是future registry schema的明确状态，不改变现有业务授权语义；它只把当前“任何非active都拒绝”的内存行为变为closed vocabulary。

### 5.3 Deterministic lookup与freeze identity

唯一Runtime入口：

```text
runtime/ctde_runtime/public_trust.py::load_portable_public_trust
```

职责：

1. 只从module-relative exact常量路径读取两个schema和两个assets；production入口不接受caller-supplied asset path、environment override、URL或network source；
2. safe parse JSON、拒绝duplicate key/BOM/float/noncanonical bytes/schema外字段；
3. 独立计算两个schema/两个asset exact SHA-256；验证status asset对material exact digest的单向引用；
4. decode raw Ed25519 public bytes，复算raw-byte digest；
5. 合并material+status records，构造现有 `KeyRecord` list和 `TrustStore`；
6. 返回immutable `LoadedPublicTrust`，包含 `TrustStore`、四个input digests、canonical semantic payload digest、Profile/trust domain与record identities；
7. `LoadedPublicTrust.codec(now)`返回现有 `JWSCodec`，同时暴露不可变 `public_trust_freeze_identity`供atomic verifier、component freeze和execution snapshot交叉验证；
8. 任一unknown、duplicate、mismatch或unresolved dependency直接fail closed。

### 5.4 Producer、更新和self-digest分责

- 两个schema、两个assets和loader均由future R3G-07 implementation materializer在获得R3G2人工授权后create-new；不得由Runtime、caller、test runner或R3 builder运行时改写。
- 正式public key内容由人工implementation authorization提供一个或多个`kid + raw 32-byte Ed25519 public key`；private key不作为project input。若没有获批public material，future implementation必须BLOCKED，不得现场生成并自授信。
- material asset不含status digest；status asset单向绑定material exact file digest；二者各自exact file digest由implementation manifest和future component freeze外部保存，避免self-digest。
- v1 assets immutable。未来rotation/revocation若改变bytes，必须创建新的versioned asset paths、更新loader常量并执行fresh R3G scope/plan/repair和fresh R3 replan；不得原地修改v1后继续使用旧closure identity。
- 当前R3G-07不建立PKI、CA、online key server、automatic rotation、HSM或network trust service。

## 6. Private-key boundary

```yaml
formal_runtime_private_key_dependency: false
formal_runtime_reads_private_key: false
private_key_in_public_trust_assets: false
private_key_in_production_runtime_closure: false
```

正式Runtime是verification consumer，只读取public assets。对应signing authority/private custody位于project Runtime之外；R3G-07不规定其存储产品、HSM或online acquisition，不把private signer availability作为public verification closure的隐含输入。

未来atomic synthetic tests使用：

```text
runtime_capability_prototype/r3g07_portable_suites/R3G07PS-20260812-001/fixtures/r3g07_test_signing_key_ed25519_seed.hex
```

该文件必须：test-only、仅一个32-byte Ed25519 seed的小写hex、与formal Runtime public material不同、权限和读取范围只供R3G-07 runner、不得进入production/runtime member set、不得复制到evidence/aggregate/report。它只进入test/control freeze，result只报告kid与file digest，不报告seed bytes。

## 7. Embedded-role 判断

候选：把asset loading直接加入 `runtime/ctde_runtime/signing.py`。

判定：`evaluated_not_selected`。

原因：

- `signing.py` 已经是稳定的crypto/type核心，同时被legacy与R2 test直接使用；加入filesystem/schema/config职责会扩大共享模块影响面；
- 独立 `public_trust.py` 可以复用现有 `KeyRecord/TrustStore/JWSCodec` 而不改动任何existing file；
- 独立loader形成清晰 `public_trust_material` role identity、可单独冻结并由fresh R3作为approved callable root枚举；
- 六个actual callers已有codec injection seam，无需把loader嵌入任何R2 asset。

```yaml
embedded_role_candidate:
  path: "runtime_capability_prototype/runtime/ctde_runtime/signing.py"
  status: "evaluated_not_selected"
selected_role_layout: "independent runtime/ctde_runtime/public_trust.py loader over existing signing primitives"
other_gap_status_changed: false
```

## 8. Future mutable existing files

```yaml
future_mutable_existing_files: []
future_mutable_existing_files_count: 0
```

不修改existing caller的原因是六个caller已经有精确codec DI seam。Future dedicated verifier通过实例化真实caller并检查其codec对象/identity来证明binding，而不是把binding逻辑复制进caller。

```yaml
r2_semantic_risk_files: []
r2_semantic_risk: false
r2_semantic_regression_count: 0
```

## 9. Future creatable files

下列20个path当前全部`ABSENT`，是R3G2必须原样使用的唯一推荐布局。R3G2可以增加摘要、producer和Gate细节，但不得另起竞争路径。

| # | exact relative path | purpose / artifact type | classification | future closure expectation |
| ---: | --- | --- | --- | --- |
| 1 | `runtime_capability_prototype/contracts/public_trust_material_schema_v1.yaml` | public material closed schema | runtime contract | runtime closure member |
| 2 | `runtime_capability_prototype/contracts/public_key_status_registry_schema_v1.yaml` | key-status closed schema | runtime contract | runtime closure member |
| 3 | `runtime_capability_prototype/contracts/portable_public_trust_material_v1.json` | immutable public material asset | configuration semantic asset | runtime closure member + semantic asset |
| 4 | `runtime_capability_prototype/contracts/portable_public_key_status_registry_v1.json` | immutable key-status registry | configuration semantic asset | runtime closure member + semantic asset |
| 5 | `runtime_capability_prototype/runtime/ctde_runtime/public_trust.py` | loader/resolver/freeze identity | runtime implementation | runtime closure member |
| 6 | `runtime_capability_prototype/contracts/r3g07_public_trust_test_requirements.yaml` | versioned atomic requirement source | test contract | test-only freeze |
| 7 | `runtime_capability_prototype/contracts/r3g07_public_trust_test_manifest_schema_v1.yaml` | frozen manifest schema | test contract | test-only freeze |
| 8 | `runtime_capability_prototype/runtime/build_r3g07_public_trust_test_manifest.py` | deterministic leaf enumerator | build-only control | build-only freeze |
| 9 | `runtime_capability_prototype/runtime/verify_r3g07_public_trust.py` | independent asset/loader/caller verifier | verification code | test-only freeze |
| 10 | `runtime_capability_prototype/runtime/run_r3g07_public_trust.py` | sole atomic controller/runner | test controller | test-only freeze |
| 11 | `runtime_capability_prototype/runtime/build_r3g07_public_trust_result.py` | mechanical aggregate/report generator | build-only control | build-only freeze |
| 12 | `runtime_capability_prototype/r3g07_portable_suites/R3G07PS-20260812-001/control/r3g07_implementation_manifest.json` | exact implementation bundle identity | control artifact | control freeze |
| 13 | `runtime_capability_prototype/r3g07_portable_suites/R3G07PS-20260812-001/control/r3g07_execution_plan.json` | fixed clock/Profile/scope/key-input identity | control artifact | control freeze |
| 14 | `runtime_capability_prototype/r3g07_portable_suites/R3G07PS-20260812-001/control/r3g07_test_manifest.json` | actual enumerated tests | test manifest | test-only freeze |
| 15 | `runtime_capability_prototype/r3g07_portable_suites/R3G07PS-20260812-001/fixtures/r3g07_synthetic_fixtures.json` | no-content vector recipes | test fixture | test-only; excluded from production closure |
| 16 | `runtime_capability_prototype/r3g07_portable_suites/R3G07PS-20260812-001/fixtures/r3g07_test_signing_key_ed25519_seed.hex` | dedicated synthetic private seed | test secret fixture | test-only; explicitly excluded from production closure/public freeze |
| 17 | `runtime_capability_prototype/r3g07_portable_suites/R3G07PS-20260812-001/attempts/r3g07_attempts.jsonl` | actual attempt terminal ledger | test evidence | test-only evidence |
| 18 | `runtime_capability_prototype/r3g07_portable_suites/R3G07PS-20260812-001/evidence/r3g07_public_trust_verification.json` | independent verification evidence | A1 test evidence | test-only evidence |
| 19 | `runtime_capability_prototype/r3g07_portable_suites/R3G07PS-20260812-001/aggregate/r3g07_public_trust_results.json` | mechanical counts/result | aggregate | test-only evidence |
| 20 | `PORTABLE_RUNTIME_ROLE_GAP_R3G07_REPAIR_RESULT.md` | future external phase result | result report | build-only/report; not production closure |

```yaml
future_creatable_files_count: 20
scope_unresolved_files: []
scope_unresolved_count: 0
```

### 9.1 Future creatable directories

```yaml
future_creatable_directories:
  - "runtime_capability_prototype/r3g07_portable_suites"
  - "runtime_capability_prototype/r3g07_portable_suites/R3G07PS-20260812-001"
  - "runtime_capability_prototype/r3g07_portable_suites/R3G07PS-20260812-001/control"
  - "runtime_capability_prototype/r3g07_portable_suites/R3G07PS-20260812-001/fixtures"
  - "runtime_capability_prototype/r3g07_portable_suites/R3G07PS-20260812-001/attempts"
  - "runtime_capability_prototype/r3g07_portable_suites/R3G07PS-20260812-001/evidence"
  - "runtime_capability_prototype/r3g07_portable_suites/R3G07PS-20260812-001/aggregate"
future_creatable_directories_count: 7
```

`contracts/`、`runtime/`和`runtime/ctde_runtime/`已存在，不计入creatable directories。

## 10. Deterministic atomic verification scope

测试数量不得在R3G1/R3G2中固定。`r3g07_public_trust_test_requirements.yaml`定义category；manifest builder根据frozen requirements、actual assets和六个caller展开leaf；runner只执行manifest leaves。

Mandatory categories：

- valid active test-only signature accepted byexisting `JWSCodec.verify`；
- unknown kid、revoked、expired、disabled、not-yet-valid、domain mismatch、algorithm mismatch全部fail closed；
- public material bytes tamper、raw-key digest mismatch、status bytes tamper、status→material digest mismatch拒绝；
- duplicate kid、material/status set mismatch、noncanonical JSON、duplicate key、unknown field、wrong Profile拒绝；
- six actual caller bindings全部持有同一loader-produced codec/freeze identity；
- RangeBroker/BoundedReader/FormalLoader trust failure在任何source/FD/formal path操作之前发生；仅使用no-content stubs，不执行source path；
- production material与test key双向隔离；test private seed从production closure、public asset、evidence和report排除；
- R2 16 assets digest保持不变，Authorization V2 artifact继续无signature/kid字段；
- component freeze输入能够独立复算material/status/schema/loader/caller identities；
- scope violation、unexpected file、unknown dependency为0。

Aggregate闭包：

```yaml
manifest_leaf_count: N
runner_discovered: N
runner_executed: N
evidence_complete: N
passed: N
failed: 0
skipped: 0
unknown: 0
timeout: 0
```

`N`只来自future frozen manifest和actual terminal ledger。

## 11. Freeze / closure binding

### 11.1 八项 mandatory binding

`closure_binding_requirements_count=8`：

1. `public_trust_material_schema_v1.yaml` exact file digest；
2. `public_key_status_registry_schema_v1.yaml` exact file digest；
3. `portable_public_trust_material_v1.json` exact digest、canonical semantic payload digest和每个raw public-key bytes digest；
4. `portable_public_key_status_registry_v1.json` exact digest、material-file digest reference与每个status/validity/domain identity；
5. `public_trust.py` exact digest及`load_portable_public_trust` callable identity；
6. `signing.py` exact digest及 `KeyRecord/TrustStore/JWSCodec.verify` identity；
7. 六个actual Runtime caller file/callable digests与“同一LoadedPublicTrust identity”binding evidence；
8. Profile、trust domain、fixed-clock/config identity和test/private exclusions。

### 11.2 Classification

| identity | classification |
| --- | --- |
| two schemas | `runtime_closure_member` / `contract_schema` |
| public material + status registry | `runtime_closure_member` and `configuration_semantic_asset` |
| `public_trust.py`、`signing.py`、six caller files | `runtime_closure_member` |
| requirements/manifest/builder/verifier/runner/result generator | `test_only_dependency` or `build_only_dependency` |
| test fixture catalog、private seed、attempt/evidence/aggregate | `test_only_dependency`; never production/runtime member |
| Ed25519/cryptography distribution and interpreter | existing R3 `platform_boundary` |

Fresh R3 policy必须把 `load_portable_public_trust`加入approved callable roots，并增加material/status/schema config edges。Fresh component freeze与execution snapshot必须扩展R3P的`public_trust_records`，逐record保存：`kid`、`jws_alg`、`key_algorithm`、`status`、`trust_domain`、`not_before`、`expires_at`、raw-public-key digest，以及material/status/loader exact identities。

## 12. R3G2 输入合同

### 12.1 Exact future scope

```yaml
r3g07_future_scope:
  mutable_existing_files: []
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
  creatable_directories:
    - "runtime_capability_prototype/r3g07_portable_suites"
    - "runtime_capability_prototype/r3g07_portable_suites/R3G07PS-20260812-001"
    - "runtime_capability_prototype/r3g07_portable_suites/R3G07PS-20260812-001/control"
    - "runtime_capability_prototype/r3g07_portable_suites/R3G07PS-20260812-001/fixtures"
    - "runtime_capability_prototype/r3g07_portable_suites/R3G07PS-20260812-001/attempts"
    - "runtime_capability_prototype/r3g07_portable_suites/R3G07PS-20260812-001/evidence"
    - "runtime_capability_prototype/r3g07_portable_suites/R3G07PS-20260812-001/aggregate"
```

### 12.2 Future read-only files

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

### 12.3 Future forbidden paths

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

### 12.4 Dependencies

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

## 13. R2 semantic regression review

检查结果：

- `authorization_schema_v2.yaml`保持原字节；不增加signature/kid/public-key字段；
- Registry exact-bytes identity、typed contexts、CAS、nonce、expiry、revocation与consumer/output semantics均不变；
- signed Runtime A1 event verification使用新public trust loader不会改变authorization artifact业务字段；
- R2 suite的临时test keys、controller public key和51/51历史evidence不迁移、不重标、不进入formal Runtime trust；
- `signing.py`也保持只读；未来loader在其上组合，不更改当前JWS validity behavior。

```yaml
r2_semantic_risk: false
r2_semantic_defect_discovered: false
r2_semantic_regression_count: 0
r2_asset_modification_count: 0
```

若R3G2或future implementation发现必须给Authorization V2新增签名业务语义、修改任一R2 asset或让R2 test key成为formal trust root，必须：

```text
BLOCKED_R2_REGRESSION_DISCOVERED
```

## 14. R3G2 readiness 与后续 Gate

本审计已经唯一决定：architecture、20个files、7个directories、0个mutable existing files、六个caller、two-asset digest chain、private boundary、tests和closure binding。不存在TBD path或竞争layout。

```yaml
unresolved_scope_ambiguity_count: 0
r3g2_ready: true
r3g2_next_document: "PORTABLE_RUNTIME_PUBLIC_TRUST_BINDING_PLAN.md"
r3g2_phase_kind: "file_level_atomic_planning_only"
r3g2_execution_authorized: false
```

即使未来R3G-07 repair PASS，仍必须：

1. 完成minimal embedded-role mapping for R3G-03/R3G-04；
2. 依据改变后的Runtime tree执行fresh R3 file-level replan；
3. fresh replan显式处置全部七个formal role identities；
4. 获得引用fresh plan exact SHA-256的人工R3执行授权；
5. 不执行旧R3P。

```yaml
r3_replan_required: true
r3_execution_authorized: false
r4_execution_authorized: false
candidate_analysis: "BLOCKED"
```

## 15. 本阶段边界终检

本阶段唯一创建：

```text
PORTABLE_RUNTIME_PUBLIC_TRUST_BINDING_SCOPE_AUDIT.md
```

Controller A1 action ledger：

```yaml
created_files:
  - "PORTABLE_RUNTIME_PUBLIC_TRUST_BINDING_SCOPE_AUDIT.md"
modified_existing_files: []

runtime_modifications: 0
r2_asset_modifications: 0
runtime_tests_executed: 0
r3_execution_count: 0
r4_execution_count: 0
candidate_run_count: 0
model_call_count: 0
english_tei_content_read_count: 0
greek_tei_content_read_count: 0
business_output_count: 0
story_structure_yaml_created: false

public_trust_schema_files_created: 0
public_key_assets_created: 0
key_status_registry_assets_created: 0
trust_loader_files_created: 0
caller_bindings_modified: 0
verifiers_created: 0
test_manifests_created: 0
test_runners_created: 0
implementation_results_created: 0

a2_os_verified_counts:
  status: "NOT_PROVIDED"
```

本审计完成后停止。不得自动进入R3G2、implementation、R3、R4或Candidate。
