from ehr_ai_core.retrieval import enrich_text_from_list

def test_enrich_text_from_list_sucess():
    sections = ["demographics", "recent_visit", "lab_result", "allergies", "chronic_conditions"]
    to_enrich = [{"type": section} for section in sections]

    enriched_list = enrich_text_from_list(to_enrich)

    assert len(enriched_list) == len(sections)

    for text in enriched_list:
        assert isinstance(text, str)
        assert text.strip() != ""
        assert not text.startswith("type:")


def test_enrich_text_from_list_empty_result():
    to_enrich = [{"type": "_"}]

    enriched_list = enrich_text_from_list(to_enrich)

    assert enriched_list[0] == "type: _"