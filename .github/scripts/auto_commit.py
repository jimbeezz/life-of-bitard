import requests
import random
from datetime import datetime
import os
import json

def get_online_quote():
    """Получает цитату с Quotable API"""
    try:
        response = requests.get("https://api.quotable.io/random", timeout=10)
        if response.status_code == 200:
            data = response.json()
            quote_text = data.get('content', '').strip()
            author = data.get('author', '').strip()
            
            if quote_text and author:
                return f"{quote_text} - {author}"
    except Exception as e:
        print(f"Ошибка получения цитаты: {e}")
    
    return get_fallback_quote()

def get_fallback_quote():
    """Локальные цитаты на случай недоступности API"""
    fallback_quotes = [
        "The only way to do great work is to love what you do. - Steve Jobs",
        "Stay hungry, stay foolish. - Steve Jobs",
        "The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt",
        "I have not failed. I've just found 10,000 ways that won't work. - Thomas Edison",
    ]
    return random.choice(fallback_quotes)

def check_today_activity(username, token):
    """Проверяет, были ли сегодня коммиты"""
    url = f"https://api.github.com/users/{username}/events"
    headers = {'Authorization': f'token {token}'}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            events = response.json()
            today = datetime.now().date()
            
            for event in events:
                event_date = datetime.strptime(event['created_at'], '%Y-%m-%dT%H:%M:%SZ').date()
                if event_date == today and event['type'] in ['PushEvent', 'CommitCommentEvent']:
                    return True
    except Exception as e:
        print(f"Ошибка проверки активности: {e}")
    
    return False

def update_readme(quote):
    """Обновляет README файл с цитатой"""
    readme_path = "README.md"
    
    try:
        if os.path.exists(readme_path):
            with open(readme_path, 'r', encoding='utf-8') as f:
                content = f.read()
        else:
            content = "# Daily Inspiration\n\n"
        
        new_section = f"\n## {datetime.now().strftime('%Y-%m-%d %H:%M')}\n> {quote}\n"
        
        sections = content.split('## ')
        if len(sections) > 50:
            content = '# Daily Inspiration\n\n' + '## '.join(sections[-50:])
        
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(content + new_section)
            
        print(f"✅ Добавлена цитата в README: {quote}")
        
    except Exception as e:
        print(f"❌ Ошибка обновления README: {e}")

def create_useless_commit():
    """Создает бесполезный коммит с обновлением временной метки"""
    useless_file_path = ".github/useless_activity.json"
    
    try:
        os.makedirs(os.path.dirname(useless_file_path), exist_ok=True)
        
        if os.path.exists(useless_file_path):
            with open(useless_file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        else:
            data = {"activity_log": []}
        
        new_entry = {
            "timestamp": datetime.now().isoformat(),
            "random_number": random.randint(1, 1000),
            "message": "Maintaining activity streak 🚀"
        }
        data["activity_log"].append(new_entry)
        
        if len(data["activity_log"]) > 100:
            data["activity_log"] = data["activity_log"][-50:]
        
        with open(useless_file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print("✅ Создан бесполезный коммит")
        
    except Exception as e:
        print(f"❌ Ошибка создания бесполезного коммита: {e}")

def main():
    username = os.getenv('USERNAME')
    token = os.getenv('GH_TOKEN')
    
    if not username or not token:
        print("❌ Не установлены переменные окружения")
        return
    
    if check_today_activity(username, token):
        print("⏭️ Сегодня уже были коммиты, пропускаем")
        return
    
    quote = get_online_quote()
    update_readme(quote)
    create_useless_commit()
    
    print("🎉 Файлы готовы для коммита!")

if __name__ == "__main__":
    main()
