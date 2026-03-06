#!/usr/bin/env python3
"""Shared helpers for the business-structure-designer skill."""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

try:
    import yaml
except Exception:  # pragma: no cover
    yaml = None


SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
REFERENCES_DIR = SKILL_DIR / "references"

REFERENCE_TEMPLATE_FILES = {
    "business_master": "business-master.json",
    "stage_map": "stage-map.json",
    "mechanism_map": "mechanism-map.json",
    "evidence_table": "evidence-table.json",
}


def load_input(path: Path) -> dict[str, Any]:
    raw = path.read_text(encoding="utf-8")
    if path.suffix.lower() in {".yaml", ".yml"}:
        if yaml is None:
            raise RuntimeError("PyYAML is required for YAML input files")
        data = yaml.safe_load(raw)
    else:
        data = json.loads(raw)
    if not isinstance(data, dict):
        raise ValueError("Input payload must be an object")
    return normalize_config(data)


def normalize_config(data: dict[str, Any]) -> dict[str, Any]:
    result = dict(data)
    result.setdefault("business_name", "未命名业务系统")
    result.setdefault("business_goal", "将业务拆成可迁移的数据结构与落地方案。")
    result["primary_users"] = ensure_str_list(result.get("primary_users"), ["业务负责人"])
    result["primary_objects"] = ensure_str_list(result.get("primary_objects"), ["业务对象"])
    result["stages"] = ensure_str_list(result.get("stages"), ["待定义阶段"])
    result["service_lines"] = ensure_str_list(result.get("service_lines"), [])
    result["dashboard_questions"] = ensure_str_list(result.get("dashboard_questions"), [])
    result["constraints"] = ensure_str_list(result.get("constraints"), [])
    result["legacy_assets"] = ensure_str_list(result.get("legacy_assets"), [])
    result["notes"] = str(result.get("notes", "")).strip()
    result["data_sources"] = normalize_sources(result.get("data_sources"))
    return result


def ensure_str_list(value: Any, default: list[str]) -> list[str]:
    if not value:
        return list(default)
    if isinstance(value, list):
        cleaned = [str(item).strip() for item in value if str(item).strip()]
        return cleaned or list(default)
    return [str(value).strip()]


def normalize_sources(value: Any) -> list[dict[str, str]]:
    if not value:
        return []
    sources: list[dict[str, str]] = []
    if isinstance(value, list):
        for item in value:
            if isinstance(item, dict):
                sources.append(
                    {
                        "name": str(item.get("name", "")).strip() or "未命名来源",
                        "type": str(item.get("type", "")).strip() or "unknown",
                        "role": str(item.get("role", "")).strip() or "supporting_source",
                        "notes": str(item.get("notes", "")).strip(),
                    }
                )
            elif str(item).strip():
                sources.append(
                    {"name": str(item).strip(), "type": "unknown", "role": "supporting_source", "notes": ""}
                )
    return sources


def load_reference_template(name: str) -> dict[str, Any]:
    path = REFERENCES_DIR / REFERENCE_TEMPLATE_FILES[name]
    return json.loads(path.read_text(encoding="utf-8"))


def customize_templates(config: dict[str, Any]) -> dict[str, dict[str, Any]]:
    business_master = load_reference_template("business_master")
    stage_map = load_reference_template("stage_map")
    mechanism_map = load_reference_template("mechanism_map")
    evidence_table = load_reference_template("evidence_table")

    business_master["table_name"] = f"{config['business_name']}-业务主表"
    business_master["notes"] = append_note(
        business_master.get("notes", ""),
        f"该模板针对 {config['business_name']} 生成，主对象包括：{join_items(config['primary_objects'])}。",
    )
    business_master["dashboard_metrics"] = dedupe_list(
        list(business_master.get("dashboard_metrics", [])) + config["dashboard_questions"]
    )

    stage_map["table_name"] = f"{config['business_name']}-阶段场景表"
    stage_map["notes"] = append_note(stage_map.get("notes", ""), f"默认阶段：{join_items(config['stages'])}。")
    stage_map["seed_records"] = [
        {"阶段名称": stage, "阶段ID": f"stage-{index + 1:02d}"} for index, stage in enumerate(config["stages"])
    ]

    mechanism_map["table_name"] = f"{config['business_name']}-实现机制表"
    mechanism_map["notes"] = append_note(
        mechanism_map.get("notes", ""),
        "建议把平台能力、脚本能力、自动化规则、权限机制和外部集成都单独建模。",
    )

    evidence_table["table_name"] = f"{config['business_name']}-证据案例表"
    evidence_table["notes"] = append_note(
        evidence_table.get("notes", ""),
        f"建议接入的历史资产：{join_items(config['legacy_assets']) or '暂无'}。",
    )

    return {
        "business-master.json": business_master,
        "stage-map.json": stage_map,
        "mechanism-map.json": mechanism_map,
        "evidence-table.json": evidence_table,
    }


def append_note(existing: str, extra: str) -> str:
    existing = str(existing).strip()
    extra = str(extra).strip()
    if not existing:
        return extra
    if not extra:
        return existing
    return f"{existing}\n{extra}"


def dedupe_list(items: list[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for item in items:
        value = str(item).strip()
        if not value or value in seen:
            continue
        seen.add(value)
        ordered.append(value)
    return ordered


def join_items(items: list[str]) -> str:
    return "、".join(item for item in items if item)


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def copy_reference_dashboard(output_dir: Path) -> None:
    dashboard_dir = output_dir / "dashboard"
    dashboard_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(REFERENCES_DIR / "dashboard-ia.md", dashboard_dir / "dashboard-ia.md")


def render_business_system(config: dict[str, Any]) -> str:
    return f"""# {config['business_name']}

## 目标

{config['business_goal']}

## 核心使用者

{bullet_list(config['primary_users'])}

## 主对象

{bullet_list(config['primary_objects'])}

## 阶段链路

{numbered_list(config['stages'])}

## 服务/产品层级

{bullet_list(config['service_lines']) or '- 暂未提供'}

## 数据来源

{source_list(config['data_sources'])}

## 仪表盘问题

{bullet_list(config['dashboard_questions']) or '- 暂未提供'}
"""


def render_rationale(config: dict[str, Any]) -> str:
    return f"""# 数据结构论证

## 为什么这样拆

- 主表只承接决策对象：{join_items(config['primary_objects'])}
- 阶段表承担导航轴：{join_items(config['stages'])}
- 机制表承接“如何做成”
- 证据表承接案例、附件、逐字稿和 SOP

## 业务约束

{bullet_list(config['constraints']) or '- 暂无额外约束'}

## 事实源与镜像

{source_list(config['data_sources'])}

## 方法论依据

- 参考 `references/business-structure-method.md`
- 参考 `references/crm-vs-strategy-library.md`
- 参考 `references/new-business-modeling-checklist.md`
"""


def render_source_mapping(config: dict[str, Any]) -> str:
    if not config["data_sources"]:
        return "# Source Mapping\n\n- 当前未提供数据来源。"
    lines = ["# Source Mapping", "", "| 来源 | 类型 | 角色 | 说明 |", "| --- | --- | --- | --- |"]
    for item in config["data_sources"]:
        lines.append(f"| {item['name']} | {item['type']} | {item['role']} | {item['notes'] or '-'} |")
    return "\n".join(lines)


def render_checklist(config: dict[str, Any]) -> str:
    return f"""# Implementation Checklist

## 访谈与定义

- 明确业务目标：{config['business_goal']}
- 确认主要使用者：{join_items(config['primary_users'])}
- 锁定核心对象：{join_items(config['primary_objects'])}

## 结构落地

- 建立业务主表
- 建立阶段/场景表
- 建立实现机制表
- 建立证据/案例表

## 运营与呈现

- 对齐仪表盘问题：{join_items(config['dashboard_questions']) or '待补充'}
- 识别事实源和镜像边界
- 输出 GitHub 可读设计包
"""


def render_current_state(config: dict[str, Any]) -> str:
    return f"""# Current State Inventory

## 现有数据来源

{source_list(config['data_sources'])}

## 历史资产

{bullet_list(config['legacy_assets']) or '- 暂无历史资产'}

## 现状备注

{config['notes'] or '暂无补充备注。'}
"""


def render_legacy_mapping(config: dict[str, Any]) -> str:
    lines = ["# Legacy To New Mapping", ""]
    if not config["legacy_assets"] and not config["data_sources"]:
        lines.append("- 当前没有提供需要映射的历史资产。")
        return "\n".join(lines)
    lines.append("| 历史来源 | 新结构建议 | 备注 |")
    lines.append("| --- | --- | --- |")
    for asset in config["legacy_assets"]:
        lines.append(f"| {asset} | 证据表 / 事实源表 | 根据内容决定是否进入主表或镜像层 |")
    for source in config["data_sources"]:
        lines.append(f"| {source['name']} | {source['role']} | {source['notes'] or '-'} |")
    return "\n".join(lines)


def render_export_readme(config: dict[str, Any], source_dir: Path) -> str:
    return f"""# {config['business_name']} Design Bundle

This export was generated by `business-structure-designer`.

## Included Files

{bullet_list(sorted(path.relative_to(source_dir).as_posix() for path in source_dir.rglob('*') if path.is_file()))}

## Business Goal

{config['business_goal']}
"""


def bullet_list(items: list[str]) -> str:
    cleaned = [str(item).strip() for item in items if str(item).strip()]
    return "\n".join(f"- {item}" for item in cleaned)


def numbered_list(items: list[str]) -> str:
    cleaned = [str(item).strip() for item in items if str(item).strip()]
    return "\n".join(f"{index}. {item}" for index, item in enumerate(cleaned, start=1))


def source_list(items: list[dict[str, str]]) -> str:
    if not items:
        return "- 暂无数据来源"
    lines = []
    for item in items:
        suffix = f"：{item['notes']}" if item["notes"] else ""
        lines.append(f"- {item['name']} ({item['type']} / {item['role']}){suffix}")
    return "\n".join(lines)
