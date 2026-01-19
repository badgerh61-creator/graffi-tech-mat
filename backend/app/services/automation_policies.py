ALLOWED_AUTOMATION_POLICIES = {
    "auto_expire_links",
    "auto_revoke_on_project_archive",
    "auto_notify_external_system",
    "log_distribution_access",
}

def policy_violates_phase_n(policy: str) -> bool:
    forbidden = {
        "auto_extend_link_lifetime",
        "auto_make_links_permanent",
        "auto_bypass_audit",
        "auto_stream_exports",
    }
    return policy in forbidden

