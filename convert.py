import mammoth


with open("BA_ViMedAI_v2.docx", "rb") as docx_file:
    result = mammoth.convert_to_markdown(docx_file)
    with open("BA_ViMedAI_v2.md", "w", encoding="utf-8") as f:
        f.write(result.value)
