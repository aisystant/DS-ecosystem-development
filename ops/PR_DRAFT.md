# PR: docs: normalize content (terminology, links, metadata, dedup)

Branch: `claude/refactor-content-coherence-20251212`

Summary
- Normalized YAML frontmatter across `content/` (fields: `type`, `status`, `created`, `layer`, `scope`).
- Resolved broken wikilinks flagged in `content/0. Управление/0.4. Автоматические отчёты ИИ/Противоречия и несогласованности 0.4.md` by adding `aliases` and updating links where safe.
- Performed deduplication analysis and produced `ops/dedup_report.md` (2 clusters). Applied conservative, non-destructive policy (Variant C): marked non-canonical cluster members with `status: review` and `suggested_canonical` in frontmatter.
- Added helper scripts: `ops/normalize_content.py`, `ops/deduplicate_content.py`, `ops/apply_dedup_stubs.py`, `ops/mark_dedup_review.py`.

Files changed (high level)
- Many `.md` files under `content/` had frontmatter added or updated.
- `content/0. Управление/0.2. Процессы работы с хранилищем/Процессы работы с хранилищем 0.2.md` was merged/rewritten as canonical for the 0.2 section.
- Reports: `ops/dedup_report.md`, `ops/dedup_applied.md` (no exact duplicates applied).

Key reports to review
- [ops/dedup_report.md](ops/dedup_report.md) — cluster analysis and recommended canonicals.
- [content/0. Управление/0.4. Автоматические отчёты ИИ/Противоречия и несогласованности 0.4.md](content/0. Управление/0.4. Автоматические отчёты ИИ/Противоречия и несогласованности 0.4.md) — original broken-links backlog.

What I changed (notes)
- Non-destructive approach: no files were automatically archived or deleted except earlier user-approved moves/merges. The deduplication step only annotated files for review.
- Many files already had `status: stub`; `ops/mark_dedup_review.py` skipped archived/stubbed files.
- Debug scripts used during processing were removed.

Next steps / suggestions
1. Review the clusters in `ops/dedup_report.md` and confirm canonical choices.
2. Resolve `status: review` files: either merge into canonical files, convert to stubs, or keep as separate documents.
3. (Optional) Apply controlled terminology normalization after manual review of ambiguous terms.
4. When approved, we can apply stronger dedup actions (auto-archive small candidates or generate merge patches).

Metrics (quick)
- Markdown files indexed: 153
- Broken wikilink tokens from 0.4 report processed: 26 → resolved or filtered to 0 unresolved (iterative normalization + fuzzy matching).
- Dedup clusters found: 2 (sizes 42 and 40). Exact-duplicate stubs applied: 0.

Scripts (for reviewers)
- Run normalization: `python ops/normalize_content.py`
- Recompute clusters: `python ops/deduplicate_content.py`
- Mark cluster candidates (variant C): `python ops/mark_dedup_review.py`

If you want, I can open the actual PR on GitHub (create pull request) or leave this branch for review and manual merge.
