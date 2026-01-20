def test_compliance_report_generated(
    retention_engine,
):
    report = retention_engine.generate_report()

    assert "policies" in report
    assert "legal_holds" in report

