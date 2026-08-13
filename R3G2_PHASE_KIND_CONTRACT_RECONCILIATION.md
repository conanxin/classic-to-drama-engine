# Classic-to-Drama Engine：R3G2 Phase-Kind Contract Reconciliation

> 项目：Classic-to-Drama Engine  
> 工作包：R3G2 Phase-Kind Contract Reconciliation  
> 日期：2026-08-12  
> 文档性质：contract clarification / reconciliation only  
> 最终状态：`PASS_R3G2_PHASE_KIND_CONTRACT_RECONCILIATION`  
> Runtime／测试／R3G2／R3／R4／Candidate execution：未执行

## 0. 最终结论

四份正式依据已经足以唯一确定 Phase 2-G-R3G2 的 machine-contract phase kind：

```yaml
current_status: "PASS_R3G2_PHASE_KIND_CONTRACT_RECONCILIATION"
next_phase_id: "Phase 2-G-R3G2"
next_phase_kind: "file_level_atomic_planning_only"
canonical_phase_kind: "file_level_atomic_planning_only"
scope_status: "resolved_for_planning"
source_scope_status_after_audit: "scope_resolved_for_r3g2_planning"
execution_authorized: false
r3g2_planning_ready: true

atomic_plan_classification: "B.human-readable_shorthand_only"
formal_alias_declared: false
deprecated_label: false
conflicting_formal_machine_value_in_source: false

unresolved_contract_ambiguity_count: 0
source_document_amendment_required: false
```

`file_level_atomic_planning_only` 是唯一 canonical machine value。`atomic_plan` 只在 repair-sequence 的人类可读描述字符串中出现；它不是正式 alias，也不是可写入 `phase_kind` 或 `next_phase_kind` 的替代值。

此前的 `BLOCKED_R3G2_PHASE_CONTRACT_MISMATCH` 是正确的：上一轮命令把 prose shorthand `atomic_plan` 放入 machine field `next_phase_kind`，与两份正式文件中的 exact machine value 不匹配。本 reconciliation 只澄清读取规则，不修改任何历史文件，也不把二者声明为正式 alias。

本文件完成后，R3G2 仍未获得执行授权。下一轮必须使用本文件 §6 的 exact next-step contract，并获得新的明确人工授权。

## 1. 正式依据与写前基线

### 1.1 只读正式依据

| 正式文件 | 本轮只读 SHA-256 | 合同作用 |
| --- | --- | --- |
| `PORTABLE_RUNTIME_ROLE_GAP_RESOLUTION_PLAN.md` | `72f116ff0b93403961a045228706f9322deea008f41718acae6178b0780b8798` | gap-specific phase、phase_kind、R3G1/R3G2 scope 与 re-entry Gate |
| `PORTABLE_RUNTIME_PUBLIC_TRUST_BINDING_SCOPE_AUDIT.md` | `e5cd250eeaec8921afd6658e55d140e4f897ce99860e2825aad1af14f6eab1f7` | R3G1 handoff、R3G2 readiness、phase_kind 与 execution authorization |
| `PORTABLE_RUNTIME_TRANSITIVE_CLOSURE_PLAN.md` | `f8ca07eaee1fff534e97bf4a0d037ba73a3c1838107e132f7c072b1fe05b39f5` | 上游 R3 planning-only／execution-not-authorized 边界和 R3G-07 role gap |
| `RUNTIME_ASSURANCE_PROFILE_DECISION.md` | `57471c85c57946f6ceb6da288301cc802533b09c137bfbe8e6e247dad57206e2` | Portable A1 / Development / non-certified Profile 与非执行边界 |

### 1.2 写前状态

```yaml
reconciliation_target: "R3G2_PHASE_KIND_CONTRACT_RECONCILIATION.md"
target_state_before: "ABSENT"
existing_files_authorized_for_modification: []
other_files_authorized_for_creation: []
```

本轮只允许创建本文件。其自身最终 exact-bytes SHA-256 由交付信息外部报告，避免 self-digest。

## 2. 全部 R3G2 phase-kind 相关证据

以下记录区分：

- **A — machine-contract field**：显式结构化字段，可用于命令 Gate；
- **B — human-readable label/prose**：标题、顺序说明或普通描述，不可自动提升为 machine value；
- **C — boundary/support evidence**：决定 scope、readiness 或 authorization，但不定义 R3G2 phase_kind；
- **D — negative evidence**：正式文件没有提供 R3G2 phase-kind override。

| # | 正式文件与 section | exact field / wording | 类型 | 合同含义 |
| ---: | --- | --- | --- | --- |
| 1 | `PORTABLE_RUNTIME_ROLE_GAP_RESOLUTION_PLAN.md` §3.7 | `gap_id: "R3G-07-IMMUTABLE-PUBLIC-TRUST-KEY-STATUS"` | A | 当前 gap identity。 |
| 2 | 同文件 §3.7 | `scope_status: "scope_requires_additional_audit"` | A | R3G1 之前的历史 entry scope；不是 R3G2 当前 handoff status。 |
| 3 | 同文件 §3.7 | `repair_phase: "Phase 2-G-R3G1, then Phase 2-G-R3G2"` | B | 只规定 phase 顺序，没有定义 phase_kind。 |
| 4 | 同文件 §7“唯一 repair sequence” | `Phase 2-G-R3G2  file-level atomic implementation plan` | B | 人类可读 phase label／职责描述。 |
| 5 | 同文件 §8.2 | `phase: "Phase 2-G-R3G1"`；`phase_kind: "read_only_scope_audit"` | A | 证明 R3G1 的 machine field 使用 exact snake-case vocabulary；不定义 R3G2。 |
| 6 | 同文件 §8 结尾 | `R3G1完成后停止，不自动进入R3G2。` | C | R3G1 不产生自动 R3G2 authorization。 |
| 7 | 同文件 §9 标题 | `Phase 2-G-R3G2：Public Trust Binding File-Level Atomic Plan` | B | 允许的人类可读 phase label。 |
| 8 | 同文件 §9.2 | `phase: "Phase 2-G-R3G2"` | A | canonical machine phase ID。 |
| 9 | 同文件 §9.2 | `phase_kind: "file_level_atomic_planning_only"` | A | gap-specific canonical machine phase_kind。 |
| 10 | 同文件 §9.2 | `mutable_existing_files: []`；唯一 `creatable_files` 为 `PORTABLE_RUNTIME_PUBLIC_TRUST_BINDING_PLAN.md` | A | R3G2 planning-only scope；本 reconciliation 不授权创建该文件。 |
| 11 | 同文件 §9.2 结尾 | `R3G2完成后停止，不自动执行implementation。` | C | 即使未来 R3G2 PASS，也不自动授权 implementation。 |
| 12 | 同文件 §11 `R3_REENTRY_GATE` | `R3G2 atomic plan PASS` | B | acceptance prose shorthand；不是 machine phase_kind 字段。 |
| 13 | 同文件 §11 `R3_REENTRY_GATE` | `r3_execution_authorized: false` | A/C | R3 保持未授权。 |
| 14 | `PORTABLE_RUNTIME_PUBLIC_TRUST_BINDING_SCOPE_AUDIT.md` 文档头与 §0 | `phase: "Phase 2-G-R3G1"`；`phase_kind: "read_only_scope_audit"`；`final_status: "PASS_PORTABLE_RUNTIME_PUBLIC_TRUST_BINDING_SCOPE_AUDIT"` | A | R3G1 已完成且只是 scope audit。 |
| 15 | 同文件 §1.1 | `scope_status_at_entry: "scope_requires_additional_audit"` | A | R3G1 entry status。 |
| 16 | 同文件 §1.1 `repair_sequence` | `"Phase 2-G-R3G2 atomic_plan"` | B | `atomic_plan` 位于一个描述字符串中；没有独立 `phase_kind` key。 |
| 17 | 同文件 §1.1 | `scope_status_after_audit: "scope_resolved_for_r3g2_planning"` | A | scope audit handoff 已闭合到 R3G2 planning。 |
| 18 | 同文件 §1.1 | `implementation_authorized_by_this_audit: false` | A/C | R3G1 不授权 implementation。 |
| 19 | 同文件 §14 | `r3g2_ready: true` | A | scope 层面具备规划条件。 |
| 20 | 同文件 §14 | `r3g2_next_document: "PORTABLE_RUNTIME_PUBLIC_TRUST_BINDING_PLAN.md"` | A | 未来 R3G2 的唯一 artifact path；本轮不得创建。 |
| 21 | 同文件 §14 | `r3g2_phase_kind: "file_level_atomic_planning_only"` | A | scope-audit handoff 再次确认 canonical machine phase_kind。 |
| 22 | 同文件 §14 | `r3g2_execution_authorized: false` | A | readiness 不等于 authorization。 |
| 23 | 同文件 §14 | `r3_execution_authorized: false`；`r4_execution_authorized: false`；`candidate_analysis: "BLOCKED"` | A/C | 下游执行全部保持未授权或阻断。 |
| 24 | 同文件 §15 结尾 | `不得自动进入R3G2、implementation、R3、R4或Candidate。` | C | R3G1 PASS 不产生自动跃迁。 |
| 25 | `PORTABLE_RUNTIME_TRANSITIVE_CLOSURE_PLAN.md` §0.1 | `final_status: "PASS_PORTABLE_R3_PLAN_ONLY"`；`r3_execution_authorized: false`；`r4_execution_authorized: false`；`candidate_execution_authorized: false` | C | 上游 R3P 是 planning-only，不能授权 R3G2 或后续执行。 |
| 26 | 同文件 §3.3 | `immutable public trust material / key-status registry` 为 `required_runtime_role_gap` | C | 确认 R3G-07 的上游必要性，但不提供 R3G2 phase_kind。 |
| 27 | 同文件全文 | 没有 `Phase 2-G-R3G2`、`r3g2_phase_kind` 或 `next_phase_kind` machine field | D | 不存在能覆盖 gap-specific R3G2 machine fields 的上游值。 |
| 28 | `RUNTIME_ASSURANCE_PROFILE_DECISION.md` §0 | `decision: "ADOPT_DUAL_ASSURANCE_PROFILES"`；`r2_execution_authorized_by_this_adr: false` | C | 只设定 Profile 和非执行边界，不定义 R3G2 phase_kind。 |
| 29 | 同文件 §8.2 | R3=`NOT_EXECUTED`、R4-P=`NOT_PLANNED / NOT_EXECUTED`、Candidate=`CURRENTLY_BLOCKED` | C | 下游状态保持不变。 |
| 30 | 同文件全文 | 没有 `Phase 2-G-R3G2`、`r3g2_phase_kind` 或 `next_phase_kind` machine field | D | 不存在 Profile ADR override。 |

四份正式文件均没有现成的 `next_phase_kind` 字段。未来命令中的 `next_phase_kind` 必须从两个一致的 gap-specific machine fields——Role Gap Plan §9.2 的 `phase_kind` 与 R3G1 Audit §14 的 `r3g2_phase_kind`——原样传递，不能从标题或 repair-sequence prose 推导。

## 3. Canonical phase_kind 判定

### 3.1 优先级应用

| 优先级 | 证据 | 结果 |
| ---: | --- | --- |
| 1. 显式 machine field | Role Gap Plan §9.2：`phase_kind: file_level_atomic_planning_only` | 直接命中 canonical value。 |
| 2. gap-specific contract | §9 明确针对 Phase 2-G-R3G2 / R3G-07 | 支持相同值。 |
| 3. scope-audit handoff | R3G1 Audit §14：`r3g2_phase_kind: file_level_atomic_planning_only` | 独立重复相同值。 |
| 4. general prose label | `atomic_plan`、`File-Level Atomic Plan`、`file-level atomic implementation plan` | 仅用于可读标题，不得覆盖前三层。 |

两项最高优先级、互相独立的 gap-specific machine fields exact-match；没有任何正式 machine field给出第二个值。因此：

```yaml
canonical_phase_kind: "file_level_atomic_planning_only"
canonical_phase_kind_evidence_count: 2
competing_machine_phase_kind_count: 0
unresolved_canonical_phase_kind_count: 0
```

不需要猜测，也不需要生成第三种名称。

## 4. `atomic_plan` 的正式性质

四个候选分类的判定如下：

| 候选 | 判定 | 理由 |
| --- | --- | --- |
| A. 正式 alias | 否 | 没有 `alias`、`aliases`、`equivalent_phase_kinds` 或等价规则。 |
| B. human-readable shorthand only | **是** | 它只出现在 Audit §1.1 的 repair-sequence 字符串；同一 Audit §14 给出不同且明确的 machine field。 |
| C. deprecated label | 否 | 正式文件没有 deprecation 标记；它仍可用于可读 phase label。 |
| D. conflicting formal value | 否（就源文件中的用法而言） | 它未占据 formal machine field，因此不是源合同中的第二个 machine value；只有把它错误写入 machine field 时才形成命令匹配冲突。 |

```yaml
atomic_plan:
  classification: "B.human-readable_shorthand_only"
  allowed_in_human_title: true
  allowed_in_repair_sequence_prose: true
  allowed_as_phase_kind: false
  allowed_as_next_phase_kind: false
  formal_alias_of_file_level_atomic_planning_only: false
```

## 5. 为什么不需要修改源合同

Role Gap Plan §9.2 与 R3G1 Audit §14 的 machine fields 已经一致，并且位于最高优先级的 gap-specific contract 与 scope-audit handoff 中。歧义来自上一轮命令把低优先级 prose shorthand 当作 machine value，而不是两个正式 machine fields 互相冲突。

因此新的 clarification artifact 足以建立未来命令匹配规则：

```yaml
source_document_amendment_required: false
source_documents_modified: []
canonical_machine_fields_changed: false
historical_labels_deleted_or_rewritten: false
```

如果未来要让 `atomic_plan` 成为正式 alias，必须另行获得修改治理合同的授权，并在 machine-readable contract 中显式声明；本 reconciliation 没有进行该修改。

## 6. Future command matching rule

### 6.1 必须匹配的 machine contract

未来申请启动 R3G2 planning 的命令必须同时提供：

```yaml
current_status: "PASS_R3G2_PHASE_KIND_CONTRACT_RECONCILIATION"
next_phase_id: "Phase 2-G-R3G2"
next_phase_kind: "file_level_atomic_planning_only"
scope_status: "resolved_for_planning"
execution_authorized: false
r3g2_planning_ready: true
```

该 block 是**下一次授权请求的入场合同**，不是本轮对 R3G2 的执行授权。下一轮还必须提供新的明确人工授权，之后才能按 Role Gap Plan §9.2 只创建 `PORTABLE_RUNTIME_PUBLIC_TRUST_BINDING_PLAN.md`。

### 6.2 人类标题与 machine value 分离

允许的人类标题：

```text
Public Trust Binding Atomic Plan
```

必须使用的 machine field：

```yaml
next_phase_kind: "file_level_atomic_planning_only"
```

匹配规则：

```yaml
human_phase_label_controls_authorization: false
machine_phase_kind_requires_exact_match: true
case_sensitive: true
whitespace_normalization_allowed: false
shorthand_expansion_allowed: false
implicit_alias_resolution_allowed: false
```

以下未来命令必须 fail closed：

```yaml
rejected_next_phase_kind_values:
  - "atomic_plan"
  - "file-level atomic planning only"
  - "file_level_atomic_plan"
  - "atomic_planning_only"
failure_status: "BLOCKED_R3G2_PHASE_CONTRACT_MISMATCH"
```

### 6.3 Readiness 与 authorization 分离

```yaml
r3g2_planning_ready: true
execution_authorized: false
implementation_authorized: false
r3_execution_authorized: false
r4_execution_authorized: false
candidate_execution_authorized: false
```

`r3g2_planning_ready=true` 只表示 phase-kind、scope handoff 与唯一目标文件路径已经闭合；它不产生 planning execution authority。没有下一轮新的明确人工授权时，不得创建 R3G2 Plan。

## 7. Reconciliation acceptance

```yaml
formal_phase_kind_evidence_recovered: true
machine_fields_distinguished_from_prose_labels: true
canonical_phase_kind_unique: true
atomic_plan_nature_resolved: true
guessing_required: false
unresolved_contract_ambiguity_count: 0
source_document_amendment_required: false
existing_formal_basis_files_modified: 0

final_status: "PASS_R3G2_PHASE_KIND_CONTRACT_RECONCILIATION"
```

本 PASS 只解除 phase-kind interpretation mismatch。它不创建、批准或执行 R3G2 atomic plan，也不改变 R3G-07、R3P、R2、R3、R4 或 Candidate 的历史状态。

## 8. 边界终检

本轮唯一授权新增文件：

```text
R3G2_PHASE_KIND_CONTRACT_RECONCILIATION.md
```

Controller A1 action ledger：

```yaml
created_files:
  - "R3G2_PHASE_KIND_CONTRACT_RECONCILIATION.md"
modified_existing_files: []

existing_file_modification_count: 0
runtime_modification_count: 0
r2_asset_modification_count: 0
runtime_test_count: 0
r3g2_execution_count: 0
implementation_execution_count: 0
r3_execution_count: 0
r4_execution_count: 0
candidate_run_count: 0
model_call_count: 0
english_tei_content_read_count: 0
greek_tei_content_read_count: 0
business_output_count: 0

r3g2_plan_files_created: 0
runtime_trust_assets_created: 0
runtime_public_keys_created: 0
private_keys_created: 0
```

本 reconciliation 完成后停止。不得自动进入 Phase 2-G-R3G2。
