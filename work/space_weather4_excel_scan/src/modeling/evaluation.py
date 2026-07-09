from __future__ import annotations


def candidate_filter(row: dict) -> bool:
    return not reject_reasons(row, strict=True)


def near_miss_filter(row: dict) -> bool:
    reasons = reject_reasons(row, strict=False)
    return not reasons


def reject_reasons(row: dict, strict: bool = True) -> list[str]:
    reasons: list[str] = []
    try:
        q = float(row.get("fdr_q_value") or 1)
        corr = abs(float(row.get("correlation") or 0))
        neg = abs(float(row.get("negative_control_correlation") or 0))
        n = int(float(row.get("n_samples") or 0))
    except Exception:
        return ["fail_parse"]
    auc = row.get("AUC")
    auc_ok = True
    if auc not in {"", None}:
        try:
            auc_ok = max(float(auc), 1 - float(auc)) > (0.55 if strict else 0.53)
        except Exception:
            auc_ok = False
    reverse = abs(float(row.get("best_reverse_lag_score") or 0))
    precursor_minus_reverse = float(row.get("precursor_minus_reverse_score") or 0)
    if row.get("lag_direction") != "external_precedes_target":
        reasons.append("fail_lag_direction")
    if row.get("feature_adjustment") == "raw":
        reasons.append("fail_raw_feature")
    if str(row.get("negative_control_pass")).lower() != "true":
        reasons.append("fail_negative_control")
    if q >= (0.1 if strict else 0.2):
        reasons.append("fail_fdr")
    if strict and corr <= neg:
        reasons.append("fail_effect_size")
    if not strict and corr <= 0.05 and (auc in {"", None} or not auc_ok):
        reasons.append("fail_effect_size")
    if not auc_ok:
        reasons.append("fail_auc")
    if strict and precursor_minus_reverse <= 0:
        reasons.append("fail_reverse_lag")
    if n < 365:
        reasons.append("fail_n_samples")
    return reasons
