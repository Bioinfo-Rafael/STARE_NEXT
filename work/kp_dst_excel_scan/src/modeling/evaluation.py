from __future__ import annotations


def candidate_filter(row: dict) -> bool:
    try:
        q = float(row.get("fdr_q_value") or 1)
        corr = abs(float(row.get("correlation") or 0))
        neg = abs(float(row.get("negative_control_correlation") or 0))
        n = int(float(row.get("n_samples") or 0))
    except Exception:
        return False
    auc = row.get("AUC")
    auc_ok = True
    if auc not in {"", None}:
        try:
            auc_ok = max(float(auc), 1 - float(auc)) > 0.55
        except Exception:
            auc_ok = False
    return (
        row.get("lag_direction") == "external_precedes_target"
        and row.get("feature_adjustment") != "raw"
        and str(row.get("negative_control_pass")).lower() == "true"
        and q < 0.1
        and corr > neg
        and auc_ok
        and n >= 365
    )
