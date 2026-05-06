import json
import re

def clean_knowledge_base():
    with open('knowledge_base.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    cleaned_data = []
    success_count = 0
    fallback_count = 0
    
    # Regex patterns
    # Look for "Triệu chứng:" or "Dấu hiệu:" (case insensitive)
    symptom_pattern = re.compile(r'(triệu chứng|dấu hiệu)[\s]*:[\s]*(.*)', re.IGNORECASE | re.DOTALL)
    
    # Pattern to remove "Bài viết của Bác sĩ XYZ..."
    seo_pattern = re.compile(r'bài viết của bác sĩ.*?(?=\.)\.', re.IGNORECASE)
    # Pattern to remove "Cùng tìm hiểu..."
    seo_pattern2 = re.compile(r'cùng( bác sĩ)?.*?tìm hiểu.*?(nhé|bài viết sau)', re.IGNORECASE)

    for item in data:
        # Lấy tên bệnh từ title hoặc trước dấu :
        content = item.get('content', '')
        disease_name = item.get('metadata', {}).get('title', '')
        if not disease_name:
            disease_name = content.split(':')[0].strip()
        
        # 1. Remove generic SEO sentences
        content = seo_pattern.sub('', content)
        content = seo_pattern2.sub('', content)
        
        # 2. Try to extract from "Triệu chứng" or "Dấu hiệu" onwards
        match = symptom_pattern.search(content)
        if match:
            # Found the symptom section!
            core_content = match.group(2).strip()
            # If the extracted part is too short, we might lose context, keep original (cleaned)
            if len(core_content) > 20:
                final_content = f"{disease_name}: Các triệu chứng bao gồm: {core_content}"
                success_count += 1
            else:
                final_content = f"{disease_name}: {content.strip()}"
                fallback_count += 1
        else:
            # Fallback to cleaned original
            final_content = f"{disease_name}: {content.strip()}"
            fallback_count += 1
            
        # Clean up any multiple spaces
        final_content = re.sub(r'\s+', ' ', final_content)
        
        cleaned_data.append({
            "content": final_content,
            "metadata": item.get('metadata', {})
        })
        
    print(f"Total items: {len(data)}")
    print(f"Items successfully extracted 'Triệu chứng/Dấu hiệu': {success_count}")
    print(f"Items using fallback (SEO cleaned): {fallback_count}")
    
    with open('clean_knowledge_base.json', 'w', encoding='utf-8') as f:
        json.dump(cleaned_data, f, ensure_ascii=False, indent=2)
        
    print("Saved to clean_knowledge_base.json")

if __name__ == "__main__":
    clean_knowledge_base()
