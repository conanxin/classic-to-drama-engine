# Classic-to-Drama Engine：R3G3 G00 Implementation Authorization Contract

> 项目：Classic-to-Drama Engine  
> 合同 ID：`CTDE-R3G3-IMPLEMENTATION-AUTHORIZATION-1`  
> 合同性质：G00 implementation authorization input machine contract definition  
> 日期：2026-08-13  
> 最终状态：`PASS_R3G3_IMPLEMENTATION_AUTHORIZATION_CONTRACT_DEFINED`  
> Profile：Portable / Development / A1 only / non-certified  
> 当前效力：contract definition only；implementation、Runtime、tests、R3、R4、Candidate 均未执行

## 0. 最终判定

本文件补齐 `PORTABLE_RUNTIME_PUBLIC_TRUST_BINDING_PLAN.md` 中 G00 与 F13 已要求、但此前没有唯一 machine representation 的 implementation authorization input contract。它不修改 Plan、Scope Audit、Runtime、R2 或任何既有文件，也不授权 Phase 2-G-R3G3 execution。

```yaml
final_status: "PASS_R3G3_IMPLEMENTATION_AUTHORIZATION_CONTRACT_DEFINED"
contract_id: "CTDE-R3G3-IMPLEMENTATION-AUTHORIZATION-1"
contract_kind: "r3g3_g00_implementation_authorization_input_machine_contract"
gap_id: "R3G-07-IMMUTABLE-PUBLIC-TRUST-KEY-STATUS"

authorization_artifact_representation_defined: true
closed_field_set_defined: true
canonical_serialization_defined: true
authorization_digest_defined: true
self_digest_rule_defined: true
fixed_utc_epoch_contract_defined: true
kid_lexical_contract_defined: true
public_key_authorization_representation_defined: true
human_approval_semantics_defined: true
f13_binding_method_defined: true

unresolved_authorization_contract_ambiguity_count: 0
r2_semantic_regression_count: 0
scope_expansion_required_count: 0

execution_authorized: false
implementation_authorized: false
```

## 1. 正式依据与冻结身份

### 1.1 正式依据

| 正式文件 | 只读 SHA-256 | 合同作用 |
| --- | --- | --- |
| `PORTABLE_RUNTIME_PUBLIC_TRUST_BINDING_PLAN.md` | `fbd689f287be47aa5aa9cc3ebb256c9b7512101be073d92b1d27ae65ce0c577a` | R3G3 machine phase、G00、F13、0/20/7 scope、public/private boundary |
| `PORTABLE_RUNTIME_PUBLIC_TRUST_BINDING_SCOPE_AUDIT.md` | `e5cd250eeaec8921afd6658e55d140e4f897ce99860e2825aad1af14f6eab1f7` | public material、status、producer authority、32-byte Ed25519 与 private exclusion |
| `R3G2_PHASE_KIND_CONTRACT_RECONCILIATION.md` | `0bcde11bee488aae7d7a1070d010ba96636437f64f583e981272f6cb77cb37e8` | machine-field exact-match discipline |
| `PORTABLE_RUNTIME_ROLE_GAP_RESOLUTION_PLAN.md` | `72f116ff0b93403961a045228706f9322deea008f41718acae6178b0780b8798` | R3G-07 authority、R3G3 boundary 与 R3 re-entry prohibition |
| `PORTABLE_RUNTIME_TRANSITIVE_CLOSURE_PLAN.md` | `f8ca07eaee1fff534e97bf4a0d037ba73a3c1838107e132f7c072b1fe05b39f5` | canonical JSON、exact-byte freeze 与 fixed-time project conventions |
| `PORTABLE_AUTHORIZATION_SCHEMA_V2_PLAN.md` | `32513cdb2c004ea91c7d7208eb3a40901934dc80440af048b84701facf1bdbe9` | exact-byte/self-digest separation；只复用编码惯例，不挪用业务授权语义 |
| `PORTABLE_AUTHORIZATION_SCHEMA_V2_IMPLEMENTATION_RESULT.md` | `b47c7280880af70325a5e5c45426951567390441ad4cd61465724fbb8eabcd06` | R2 PASS 与 immutable semantic boundary |
| `RUNTIME_ASSURANCE_PROFILE_DECISION.md` | `57471c85c57946f6ceb6da288301cc802533b09c137bfbe8e6e247dad57206e2` | Portable / Development / A1 / non-certified ceiling |

### 1.2 Plan 与 Scope Audit exact identity

```yaml
plan_path: "PORTABLE_RUNTIME_PUBLIC_TRUST_BINDING_PLAN.md"
plan_sha256: "fbd689f287be47aa5aa9cc3ebb256c9b7512101be073d92b1d27ae65ce0c577a"
scope_audit_path: "PORTABLE_RUNTIME_PUBLIC_TRUST_BINDING_SCOPE_AUDIT.md"
scope_audit_sha256: "e5cd250eeaec8921afd6658e55d140e4f897ce99860e2825aad1af14f6eab1f7"
plan_digest_algorithm: "SHA-256 over exact file bytes"
plan_digest_match_at_contract_definition: true
scope_audit_digest_match_at_contract_definition: true
```

本合同自身的 exact SHA-256 不写入自身。未来人工授权必须从本阶段外部交付信息取得本文件摘要，并在 authorization artifact 的 `authorization_contract_sha256` 中逐字引用。

## 2. 合同边界与非扩展规则

本合同定义的是 **R3G3 control-plane authorization input**，不是 `authorization_artifact_v2`，不进入 Authorization Schema V2 Registry，不产生 one-time consume、nonce、replay、mint、preparation 或 activation 业务语义。

本合同文件也不加入 R3G1 已冻结的 20 个 future files、7 个 directories 或 future Runtime closure。Future G00 不读取本文件；它只接收由新的人工作用明确批准的 canonical authorization artifact bytes，并比较其中的 `authorization_contract_path` 与外部交付摘要。因此：

```yaml
r3g07_future_file_count_changed: false
r3g07_future_directory_count_changed: false
r3g07_read_only_scope_changed: false
r2_authorization_business_semantics_changed: false
runtime_closure_membership_for_this_contract: false
```

## 3. Implementation Authorization Artifact

### 3.1 Logical identity 与 representation

唯一 logical artifact contract：

```yaml
artifact_logical_name: "R3G3 Implementation Authorization Artifact"
schema_id: "urn:ctde:contract:r3g3-implementation-authorization:1"
schema_version: "1.0.0"
artifact_class: "ctde_r3g3_implementation_authorization"
representation: "external exact canonical JSON bytes"
project_file_required: false
project_path_allowed: false
```

Artifact 由未来人工授权动作在 project tree 外提供。它可以作为授权消息中的 exact payload 传递，但 Markdown fence、消息前后说明、平台 message ID 和 transport metadata 均不属于 artifact bytes。未来 controller 只能从明确授权动作取得 exact bytes；不得从环境变量、网络、Runtime asset、R2 Registry 或未批准 workspace file 自行发现 authority。

### 3.2 Closed top-level field set

Artifact 顶层必须恰好包含以下 19 个字段；全部 required，unknown field 一律拒绝：

| Field | Type | Exact contract |
| --- | --- | --- |
| `schema_id` | string | const `urn:ctde:contract:r3g3-implementation-authorization:1` |
| `schema_version` | string | const `1.0.0` |
| `artifact_class` | string | const `ctde_r3g3_implementation_authorization` |
| `implementation_authorization_id` | string | §4.2 lexical contract；人工提供 |
| `authorization_contract_path` | string | const `R3G3_IMPLEMENTATION_AUTHORIZATION_CONTRACT.md` |
| `authorization_contract_sha256` | string | 本合同 external exact-file SHA-256；64 lowercase hex；人工授权引用外部交付值 |
| `gap_id` | string | const `R3G-07-IMMUTABLE-PUBLIC-TRUST-KEY-STATUS` |
| `phase_id` | string | const `Phase 2-G-R3G3` |
| `phase_kind` | string | const `r3g07_atomic_implementation_and_deterministic_verification_only` |
| `suite_id` | string | const `R3G07PS-20260812-001` |
| `assurance_profile_id` | string | const `CTDE-PORTABLE-DEV-1` |
| `trust_domain` | string | const `ctde-portable-runtime` |
| `plan_path` | string | const `PORTABLE_RUNTIME_PUBLIC_TRUST_BINDING_PLAN.md` |
| `plan_sha256` | string | const `fbd689f287be47aa5aa9cc3ebb256c9b7512101be073d92b1d27ae65ce0c577a` |
| `scope_audit_path` | string | const `PORTABLE_RUNTIME_PUBLIC_TRUST_BINDING_SCOPE_AUDIT.md` |
| `scope_audit_sha256` | string | const `e5cd250eeaec8921afd6658e55d140e4f897ce99860e2825aad1af14f6eab1f7` |
| `authorized_scope_sha256` | string | const `989ae9e64a055b9313d537aeffc67714c4ed47277992206fe3197131e5e24d53`；§7 |
| `public_trust_record` | closed object | §4–§5 exact 9-field record |
| `fixed_utc_epoch_seconds` | integer | §6 exact contract；人工提供 |

```yaml
authorization_artifact_top_level_field_count: 19
```

Artifact 不包含 `implementation_authorization_sha256`、`approved`、signature、private key、R2 authorization ID、Registry row、wall-clock timestamp、self size或任何执行结果。

### 3.3 Canonical serialization

Exact artifact bytes 使用 `CTDE-R3G3-AUTH-JCS-1`：

1. 一个 JSON object；UTF-8；无 BOM；
2. 只允许 object、string、integer；本 schema 不允许 null、boolean、array 或 float；
3. object keys 按 RFC 8785/JCS 的 Unicode code-point order排序；
4. compact separators：`,` 与 `:` 后无空格，无缩进；
5. string 使用 JSON 标准转义；不得进行 transport-specific escaping；
6. 禁止 duplicate key、NaN、Infinity、负零、unknown field和非最短数字表示；
7. canonical JSON object bytes后恰好一个 LF (`0x0a`)；不得有 CR、额外空行或尾随空格；
8. parser 必须先验证输入已是上述 exact canonical bytes，不得以 parse 后重新序列化来接受非canonical输入。

## 4. Identity Lexical Contracts

### 4.1 `kid_lexical_contract`

```yaml
kid_lexical_contract:
  field_name: "kid"
  type: "JSON string"
  minimum_length: 1
  maximum_length: 128
  allowed_character_set: "ASCII only"
  regex: "^[A-Za-z0-9][A-Za-z0-9._:/-]{0,127}$"
  case_policy: "case-sensitive exact string"
  normalization_policy: "none; ASCII input must already be canonical"
  leading_whitespace_allowed: false
  trailing_whitespace_allowed: false
  internal_whitespace_allowed: false
  unicode_allowed: false
  human_naming_allowed: true
  public_key_digest_derivation_required: false
  runtime_rewriting_allowed: false
  canonical_representation: "one JSON string value in public_trust_record"
```

此规则复用项目已经实施的通用 immutable ID lexical shape，但不把 `kid` 变成 Authorization Schema V2 字段，也不改变 R2 语义。`kid` 由人命名和批准；Runtime 不得 lower-case、upper-case、Unicode-normalize、trim、alias 或从公钥 digest 自动生成。

### 4.2 `implementation_authorization_id`

`implementation_authorization_id` 使用与 §4.1 相同的 1–128 ASCII lexical rule和case-sensitive exact equality，但它与 `kid` 是不同 identity domain，值相同也不能互换语义。它由人工提供，用作 F13 的 authorization reference。

## 5. Ed25519 Public Trust Record

### 5.1 Closed record

`public_trust_record` 必须恰好包含以下 9 个字段：

| Field | Type | Exact contract |
| --- | --- | --- |
| `kid` | string | §4.1 |
| `jws_alg` | string | const `EdDSA` |
| `key_algorithm` | string | const `Ed25519` |
| `public_key_encoding` | string | const `raw-32-byte-lowercase-hex` |
| `public_key_hex` | string | regex `^[0-9a-f]{64}$`；decoded bytes length exactly 32 |
| `public_key_bytes_sha256` | string | regex `^[0-9a-f]{64}$`；SHA-256 over decoded raw 32 bytes |
| `status` | string | const `active` for this minimal formal Runtime trust record |
| `not_before` | string | exact valid RFC 3339 UTC whole-second `YYYY-MM-DDTHH:MM:SSZ` |
| `expires_at` | string | same format；strictly later than `not_before` |

Unknown field、second record、empty record或duplicate JSON key全部拒绝。R3G3 v1 只授权一个 formal public trust record；这满足 Audit 的“一个或多个”non-empty contract中的最小集合。增加第二个formal key必须先获得新的contract/scope authorization，不得在当前 artifact 中临时扩展数组。

### 5.2 Public-key representation

```yaml
key_algorithm: "Ed25519"
decoded_raw_key_length_bytes: 32
authorization_field_name: "public_key_hex"
authorization_encoding: "64 lowercase hexadecimal characters"
prefix_allowed: false
pem_allowed: false
base64_allowed: false
line_break_inside_value_allowed: false
public_key_bytes_digest_field: "public_key_bytes_sha256"
public_key_bytes_digest_algorithm: "SHA-256 over decoded raw 32 bytes"
```

`public_key_bytes_sha256` 不对 hex文本、JSON string、完整record或asset文件求摘要。Validator必须先严格hex-decode `public_key_hex`，验证长度为32，再对raw bytes求SHA-256并exact compare。

### 5.3 `kid` ↔ public key ↔ status identity

唯一 public-input identity 为：

```text
public_trust_record_sha256 =
  SHA-256(CTDE-R3G3-AUTH-JCS-1 canonical bytes of public_trust_record alone)
```

“record alone”采用与artifact相同的compact JCS object encoding并以单个LF结束。该record同时绑定 `kid`、raw public-key digest、algorithm、`active` status、trust domain的artifact外层常量以及validity window。未来 F13 保存 `public_trust_record_sha256`；F03/F04 materialize 后还必须分别保存其exact-file digests，不能用本record digest替代asset identity。

F03 material record和F04 status record必须使用完全相同的 `kid`。F04 必须单向引用F03 exact-file SHA-256。任何kid mismatch、raw-key digest mismatch、status不是active、validity mismatch或material/status key-set不相等均fail closed。

## 6. Fixed UTC Epoch Contract

```yaml
fixed_utc_epoch_contract:
  field_name: "fixed_utc_epoch_seconds"
  machine_type: "JSON integer"
  unit: "Unix seconds"
  epoch_origin: "1970-01-01T00:00:00Z"
  timezone: "UTC"
  whole_second_required: true
  fractional_value_allowed: false
  minimum: 0
  maximum: 253402300799
  wall_clock_fallback_allowed: false
  environment_override_allowed: false
  human_value_required: true
```

该值是本次 R3G3 deterministic trust/key-validity evaluation time，不是 business authorization issuance time、Registry registration time、trust asset creation time或证明现实世界时间的证据。它必须满足：

```text
epoch(not_before) <= fixed_utc_epoch_seconds <= epoch(expires_at)
```

RFC 3339 conversion使用公历、UTC、整秒，无leap-second `:60`。未来 authorization artifact与F13必须逐字保存同一JSON integer；`JWSCodec.now`直接使用这个integer。Runtime、loader、runner不得以wall clock、mtime、message time或系统locale替代。

## 7. Authorized Implementation Scope Identity

### 7.1 Canonical scope payload

`authorized_scope_sha256` 使用 `CTDE-R3G07-SCOPE-JCS-1`。Payload是一个closed JSON object，恰好包含：

```text
creatable_directories
creatable_files
forbidden_paths
mutable_existing_files
read_only_files
workspace_write_policy
```

构造规则：

1. `mutable_existing_files`逐字取Plan §2.1，当前为空数组；
2. `creatable_files`逐字取Plan §2.2并保持Plan顺序，当前20项；
3. `creatable_directories`逐字取Plan §2.3并保持Plan顺序，当前7项；
4. `read_only_files`逐字取Plan §2.4并保持Plan顺序，当前35项；本合同文件不得加入；
5. `forbidden_paths`逐项取Plan §2.6并保持Plan顺序；每项只包含Plan实际给出的`path`、`access`及存在时的`recursive`；
6. `workspace_write_policy`逐字为`default_deny`；
7. 使用compact JCS object encoding、UTF-8、无BOM、末尾单个LF；
8. 对全部exact bytes计算SHA-256。

定义结果：

```yaml
authorized_scope_canonicalization_id: "CTDE-R3G07-SCOPE-JCS-1"
authorized_scope_sha256: "989ae9e64a055b9313d537aeffc67714c4ed47277992206fe3197131e5e24d53"
mutable_existing_files_count: 0
creatable_files_count: 20
creatable_directories_count: 7
read_only_files_count: 35
forbidden_path_policy_item_count: 10
```

Plan digest还外部绑定implementation sequence、22-node/100-edge/0-cycle graph、6 callers和21 requirement groups；scope digest不能替代Plan digest。

## 8. Authorization Digest Construction

### 8.1 Exact construction

```yaml
implementation_authorization_digest:
  external_field_name: "implementation_authorization_sha256"
  algorithm: "SHA-256"
  digest_input: "the complete exact CTDE-R3G3-AUTH-JCS-1 artifact bytes, including the single terminal LF"
  field_ordering: "RFC 8785/JCS object-key order"
  self_digest_in_artifact: false
  parsed_object_reserialization_accepted_as_identity: false
```

Digest payload包含§3.2全部19个字段，因此确定性绑定：contract identity、phase、gap、suite、Profile、trust domain、Plan、Scope Audit、authorized scope、`kid`、public key/raw digest、status/validity和fixed UTC epoch。

Artifact 禁止包含 `implementation_authorization_sha256`。Digest 由未来人工授权动作外部提供并批准，由G00从收到的exact bytes独立复算，由F13保存；这消除self-digest cycle。

### 8.2 Three distinct digests

以下digest不可互换：

| Digest | Input | Consumer |
| --- | --- | --- |
| `implementation_authorization_sha256` | 完整authorization artifact exact bytes | human approval、G00、F13、F18、F20 |
| `public_trust_record_sha256` | nested `public_trust_record` canonical bytes+LF | F13、F03/F04 cross-binding、freeze evidence |
| `public_key_bytes_sha256` | decoded raw 32-byte Ed25519 public key | F03、F04、F05、future R3 closure |

## 9. Human Approval Semantics

Artifact 内容是待批准的deterministic proposal；即使其字段全部有效，也不自行证明批准。特别是artifact内不存在、也不得增加 `approved: true`。

只有新的明确人工授权动作才能使该次G00看到 `implementation_authorized=true`。该动作必须同时逐字引用：

1. `implementation_authorization_id`；
2. `implementation_authorization_sha256`；
3. `authorization_contract_path`及其external exact SHA-256；
4. `plan_path`和exact `plan_sha256`；
5. exact `phase_id`和`phase_kind`；
6. `kid`；
7. `public_key_bytes_sha256`；
8. `public_trust_record_sha256`；
9. `fixed_utc_epoch_seconds`；
10. 明确语义：只授权该digest绑定的R3G-07 implementation和manifest-enumerated deterministic verification，不授权其他R3G gap、R3、R4、Candidate或business output。

Human action引用的任一值与artifact或复算值不一致，G00必须拒绝。批准不可从artifact字段、历史聊天摘要、phase标题、自然语言logical target或先前失败尝试推导。新合同PASS本身不产生implementation authority。

## 10. F13 Compatibility

Future F13 `r3g07_execution_plan.json` 可以并必须从本合同确定性冻结：

| F13 responsibility | Frozen source |
| --- | --- |
| authorization reference | `implementation_authorization_ref` = exact artifact `implementation_authorization_id` |
| authorization digest | `implementation_authorization_sha256` = exact artifact bytes SHA-256 |
| authorization contract | `authorization_contract_path` + external exact digest |
| Plan identity | artifact `plan_path` + `plan_sha256` |
| Audit identity | artifact `scope_audit_path` + `scope_audit_sha256` |
| F12 identity | future `r3g07_implementation_manifest.json` exact SHA-256；在I14后由F13加入，不进入pre-write authorization artifact |
| phase | artifact exact `phase_id` + `phase_kind` |
| Profile/domain | artifact `assurance_profile_id` + `trust_domain` |
| fixed clock | artifact `fixed_utc_epoch_seconds` integer |
| public input | artifact full `public_trust_record` + recomputed `public_trust_record_sha256` |
| read/write/forbidden scope | Plan exact sets + artifact `authorized_scope_sha256` |
| execution state | initialized/not-pre-passed；不能由authorization artifact预先声明PASS |

F13必须是Plan要求的compact canonical JSON+LF、无self digest。F09以后交叉验证上述值；本阶段不创建或执行F13。

## 11. Formal Runtime / Test Private Material Boundary

```yaml
formal_runtime_public_material_source: "human-approved public_trust_record"
formal_runtime_private_key_dependency: false
formal_private_key_is_r3g3_input: false
formal_private_key_project_storage_allowed: false
runtime_loader_reads_private_material: false
```

未来 deterministic verification需要签名时，只允许：

1. F15中由project外部signer提供的precomputed formal-key signed public vector；对应private key仍不进入project；或
2. Plan批准的F16 independent test-only Ed25519 seed/key，用于test shadow。

F16派生public key必须与formal `public_key_hex`不同。F16不得成为formal Runtime trust root、caller Runtime dependency、production closure member或public trust identity，也不得复制到F03/F04/F18/F19/F20。当前阶段不生成任何key。

## 12. R3G3_IMPLEMENTATION_AUTHORIZATION_INPUT_TEMPLATE

模板分为“待人工填充的artifact payload”和“外部人工批准动作”两部分。模板不是authorization artifact，不是canonical bytes，也不表示approved。

### 12.1 Artifact payload template

```json
{
  "schema_id": "urn:ctde:contract:r3g3-implementation-authorization:1",
  "schema_version": "1.0.0",
  "artifact_class": "ctde_r3g3_implementation_authorization",
  "implementation_authorization_id": "<REQUIRES_HUMAN_VALUE>",
  "authorization_contract_path": "R3G3_IMPLEMENTATION_AUTHORIZATION_CONTRACT.md",
  "authorization_contract_sha256": "<REQUIRES_HUMAN_VALUE>",
  "gap_id": "R3G-07-IMMUTABLE-PUBLIC-TRUST-KEY-STATUS",
  "phase_id": "Phase 2-G-R3G3",
  "phase_kind": "r3g07_atomic_implementation_and_deterministic_verification_only",
  "suite_id": "R3G07PS-20260812-001",
  "assurance_profile_id": "CTDE-PORTABLE-DEV-1",
  "trust_domain": "ctde-portable-runtime",
  "plan_path": "PORTABLE_RUNTIME_PUBLIC_TRUST_BINDING_PLAN.md",
  "plan_sha256": "fbd689f287be47aa5aa9cc3ebb256c9b7512101be073d92b1d27ae65ce0c577a",
  "scope_audit_path": "PORTABLE_RUNTIME_PUBLIC_TRUST_BINDING_SCOPE_AUDIT.md",
  "scope_audit_sha256": "e5cd250eeaec8921afd6658e55d140e4f897ce99860e2825aad1af14f6eab1f7",
  "authorized_scope_sha256": "989ae9e64a055b9313d537aeffc67714c4ed47277992206fe3197131e5e24d53",
  "public_trust_record": {
    "kid": "<REQUIRES_HUMAN_VALUE>",
    "jws_alg": "EdDSA",
    "key_algorithm": "Ed25519",
    "public_key_encoding": "raw-32-byte-lowercase-hex",
    "public_key_hex": "<REQUIRES_HUMAN_VALUE>",
    "public_key_bytes_sha256": "<REQUIRES_HUMAN_VALUE>",
    "status": "active",
    "not_before": "<REQUIRES_HUMAN_VALUE>",
    "expires_at": "<REQUIRES_HUMAN_VALUE>"
  },
  "fixed_utc_epoch_seconds": "<REQUIRES_HUMAN_VALUE>"
}
```

注意：模板为了可读性使用缩进，且placeholder把integer位置表示为string；填值后必须把 `fixed_utc_epoch_seconds` 写成无引号JSON integer，删除所有placeholder并按§3.3重建单行canonical bytes+LF。

### 12.2 External human approval template

```yaml
R3G3_IMPLEMENTATION_AUTHORIZATION_APPROVAL:
  implementation_authorization_ref: "<REQUIRES_HUMAN_VALUE>"
  implementation_authorization_sha256: "<REQUIRES_HUMAN_VALUE>"
  authorization_contract_path: "R3G3_IMPLEMENTATION_AUTHORIZATION_CONTRACT.md"
  authorization_contract_sha256: "<REQUIRES_HUMAN_VALUE>"
  plan_path: "PORTABLE_RUNTIME_PUBLIC_TRUST_BINDING_PLAN.md"
  plan_sha256: "fbd689f287be47aa5aa9cc3ebb256c9b7512101be073d92b1d27ae65ce0c577a"
  phase_id: "Phase 2-G-R3G3"
  phase_kind: "r3g07_atomic_implementation_and_deterministic_verification_only"
  kid: "<REQUIRES_HUMAN_VALUE>"
  public_key_bytes_sha256: "<REQUIRES_HUMAN_VALUE>"
  public_trust_record_sha256: "<REQUIRES_HUMAN_VALUE>"
  fixed_utc_epoch_seconds: <REQUIRES_HUMAN_VALUE>
  approval_scope: "R3G-07 implementation and manifest-enumerated deterministic verification only"
  implementation_authorized: true
```

该external block只有在用户以新的明确人工动作提交、且同时提供exact canonical artifact bytes时才生效。复制模板、contract PASS或填入`implementation_authorized: true`但没有明确人工批准，均不生效。

## 13. Future Contract Validator Requirements

未来G00/F09 validator必须至少：

1. 拒绝missing/extra/duplicate字段，确认top-level恰好19项、record恰好9项；
2. 验证schema ID/version/artifact class；
3. exact-match gap、phase、suite、Profile、trust domain；
4. exact-matchPlan path/SHA与Scope Audit path/SHA；
5. 从Plan exact scope复算 `authorized_scope_sha256`；
6. 按§4验证authorization ID与kid lexical contract；
7. 验证public key仅64 lowercase hex、无prefix/PEM/base64/line break，decode后恰好32 bytes；
8. 复算并exact-match `public_key_bytes_sha256`；
9. 验证single active record、RFC3339 UTC validity、`not_before < expires_at`；
10. 验证 `fixed_utc_epoch_seconds` 是非boolean JSON integer、在`0..253402300799`且落入inclusive validity window；
11. exact-byte验证UTF-8/JCS/LF canonicalization；两个独立in-memory rebuild必须byte-identical；
12. 复算完整 `implementation_authorization_sha256`与nested `public_trust_record_sha256`；
13. 验证human approval逐字引用artifact ID、artifact digest、contract digest、Plan digest、kid、public-key digest、record digest和fixed epoch；
14. 在human approval缺失、摘要失配或自然语言scope变宽时fail closed；
15. 验证artifact/private boundary：无private bytes、certificate、URL、network locator或R2 business authorization字段；
16. 验证20 files/7 directories仍全部ABSENT、34 existing read-only baseline entries匹配、R2 16/16摘要匹配后，才允许Plan G00继续；
17. 不把validator PASS解释为Runtime test PASS、R3G3 PASS或R3 authority。

测试leaf数量由future manifest实际枚举；本合同不定义测试数量，也不执行validator。

## 14. PASS Acceptance 与 Next-Step Contract

### 14.1 Contract-definition acceptance

```yaml
authorization_artifact_representation: "unique"
closed_field_set: "19/19"
canonical_serialization: "CTDE-R3G3-AUTH-JCS-1"
digest_algorithm: "SHA-256 over exact canonical artifact bytes including terminal LF"
complete_digest_payload: true
self_digest_cycle: false
fixed_utc_epoch_field_unit_type: "fixed_utc_epoch_seconds / Unix seconds / JSON integer"
kid_lexical_contract: "unique"
public_key_representation: "raw-32-byte-lowercase-hex"
human_approval_semantics: "external exact-digest approval"
f13_binding_method: "unique"
unresolved_authorization_contract_ambiguity_count: 0
r2_semantic_regression_count: 0
scope_expansion_required_count: 0
final_status: "PASS_R3G3_IMPLEMENTATION_AUTHORIZATION_CONTRACT_DEFINED"
```

### 14.2 Formal project status remains unchanged

```yaml
formal_current_status: "PASS_PORTABLE_RUNTIME_PUBLIC_TRUST_BINDING_ATOMIC_PLAN"
formal_next_phase_id: "Phase 2-G-R3G3"
formal_next_phase_kind: "r3g07_atomic_implementation_and_deterministic_verification_only"
scope_status: "planned_waiting_for_explicit_implementation_authorization"
execution_authorized: false
implementation_authorized: false
authorization_input_contract_ready: true
human_values_required:
  - "implementation_authorization_id"
  - "authorization_contract_sha256 from this stage external handoff"
  - "kid"
  - "public_key_hex"
  - "public_key_bytes_sha256"
  - "not_before"
  - "expires_at"
  - "fixed_utc_epoch_seconds"
  - "public_trust_record_sha256"
  - "implementation_authorization_sha256"
  - "explicit human approval action matching all exact identities"
```

下一步只能由人工提供完整canonical artifact bytes、external digests和明确批准动作。本合同不自动进入G00、R3G3 implementation、minimal embedded-role mapping或fresh R3 replan。

## 15. 本阶段边界终检

本阶段唯一创建：

```text
R3G3_IMPLEMENTATION_AUTHORIZATION_CONTRACT.md
```

```yaml
created_files:
  - "R3G3_IMPLEMENTATION_AUTHORIZATION_CONTRACT.md"
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

public_trust_asset_created_count: 0
public_key_file_created_count: 0
private_key_created_count: 0
r3g07_future_file_created_count: 0
r3g07_future_directory_created_count: 0
```

本文件到此停止。Contract definition PASS不等于implementation authorization或R3G3 PASS。
