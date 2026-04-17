import streamlit as st
import os
import json
import time

DB_FILE = "competitions.json"
BOOKS_FILE = "books.json"

#загрузка
def load_data():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                content = f.read()
                if not content: return {"Первый тест": ["Алексей"]}
                return json.loads(content)
        except:
            return {"Первый тест": ["Алексей"]}
    return {"Первый тест": ["Алексей"]}

#сейв
def save_data(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

#книги_лоад
def load_books():
    if os.path.exists(BOOKS_FILE):
        try:
            with open(BOOKS_FILE, "r", encoding="utf-8") as f:
                content = f.read()
                if not content: return []
                return json.loads(content)
        except:
            return []
    return []

#книги_сейв
def save_books(data):
    with open(BOOKS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

#память
if 'challenges' not in st.session_state:
    st.session_state.challenges = load_data()
if 'book' not in st.session_state:
    st.session_state['book'] = load_books()
if 'auth' not in st.session_state:
    st.session_state['auth'] = False
if 'user' not in st.session_state:
    st.session_state['user'] = ""

#вход
if not st.session_state['auth']:
    st.title("ReadBook")
    st.subheader("Регистрация участника")
    
    u_name = st.text_input("Как тебя зовут?")
    if st.button("Войти в систему"):
        if u_name:
            st.session_state['auth'] = True
            st.session_state['user'] = u_name
            st.rerun()
        else:
            st.error("Введи имя!")

else:
#сайдбар
    st.sidebar.write(f"Участник: **{st.session_state['user']}**")
    
    my_books = [b for b in st.session_state['book'] if b['user'] == st.session_state['user']]
    total_pages = sum(b['pages'] for b in my_books)
    
    st.sidebar.metric("Всего страниц:", total_pages)
    
    if st.sidebar.button("Выйти"):
        st.session_state['auth'] = False
        st.rerun()

    t1, t2, t3, t4 = st.tabs(["🏠 Главная", "➕ Создать", "🏆 Соревнования", "🎯 Рейтинг"])

#главная
    with t1:
        st.write(f"Привет, {st.session_state['user']}! Добавляй прочитанное сюда")
        
        with st.container(border=True):
            nb = st.text_input("Название книги и автор")
            ps = st.number_input("Кол-во страниц", min_value=1, step=10)
            ot = st.text_input("Отзыв о книге (по желанию)")
            
            if st.button("Добавить прочитанную"):
                if nb and ps:
                    new_book = {"user": st.session_state['user'], "title": nb, "pages": ps, "rev": ot}
                    st.session_state['book'].append(new_book)
                    save_books(st.session_state['book']) 
                    st.toast(f"Книга добавлена!", icon="📖")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Надо заполнить название и количество страниц")

        if my_books:
            st.subheader("Твои прочитаные книги:")
            for b in my_books:
                st.write(f"📖 **{b['title']}** — {b['pages']} стр.")
                if b['rev']:
                    st.caption(f"💬 Отзыв: {b['rev']}")

#создание
    with t2:
        st.subheader("Создать новое соревнование")
        newch = st.text_input("Название (например: Битва ли24)")
        if st.button("Опубликовать"):
            if newch:
#проверка
                if newch not in st.session_state.challenges:
                    st.session_state.challenges[newch] = [st.session_state.user]
                    save_data(st.session_state.challenges)
                    
                    st.toast(f"Соревнование '{newch}' создано!",icon = "🔥")  
                    time.sleep(1)        
                    st.rerun()         
                else:
                  st.error("Такое название уже есть")
            else:
                st.error("Введи название")

#список
    with t3:
      st.subheader("🏆 доступные соревнования")
        
        #поле_поиска
      sr = st.text_input("🔍 найти челлендж", "", placeholder="введи название...")
        
      found = False
      for name, members in st.session_state['challenges'].items():
            #пров
            if sr.lower() in name.lower():
                found = True
                with st.container(border=True):
                    col1, col2 = st.columns([3, 1])
                    col1.write(f"**{name}**")
                    col1.caption(f"участники: {', '.join(members)}")
                    
                    if col2.button(f"вступить", key=f"join_{name}"):
                        if st.session_state.user not in members:
                            st.session_state.challenges[name].append(st.session_state.user)
                            save_data(st.session_state.challenges)
                            st.toast("ты в соревновании", icon="🔥")
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.warning("ты уже там")
        


#топ
    with t4:
        st.subheader("🎯 Личный статус")
        
        #метрики
        c1, c2 = st.columns(2)
        lvl = "только начал" if total_pages <50 else "новичок" if total_pages < 350 else "про" if total_pages < 1000 else "легенда"
        c1.metric("ранг", lvl)
        c2.metric("страницы", f"{total_pages} шт")

        #питомец
        with st.container(border=True):
            if total_pages <50:
                st.markdown("### 🥚 статус: спит")
                st.write("прочти хоть немного, чтобы орел вылупился")
            elif total_pages < 100:
                st.markdown("### 🐣 статус: вылупился")
                st.write("корми его страницами")
            elif total_pages < 500:
                st.markdown("### 🐥 статус: летает")
                st.write("среднячок")
            else:
                st.markdown("### 🦅 статус: орел")
                st.write("лучше некуда")

            #шкала
            bar = min(total_pages / 500.0, 1.0)
            st.progress(bar)
            st.caption(f"прогресс до орла: {int(bar*100)}%")
        
        st.subheader("Рейтинг участников соревнования")
        
        my_ch = [n for n, m in st.session_state.challenges.items() if st.session_state.user in m]
        
        if not my_ch:
            st.info("Вступи в соревнование, чтобы увидеть топ")
        else:
            selected_ch = st.selectbox("Выбери соревнование для просмотра топа:", my_ch)
            members = st.session_state.challenges[selected_ch]
            
            lb1 = []
            for member in members:
                #считаем_страницы_каждого
                p = sum(b['pages'] for b in st.session_state['book'] if b['user'] == member)
                lb1.append({"name": member, "pages": p})
            
            #сорт
            lb1 = sorted(lb1, key=lambda x: x['pages'], reverse=True)
            
            for i, user in enumerate(lb1):
                place = i + 1
                name = user['name']
                pages = user['pages']
                
                #лиги
                if pages >= 1000: league = "🏆 ЗОЛОТАЯ ЛИГА"
                elif pages >= 500: league = "🥈 СЕРЕБРЯНАЯ ЛИГА"
                else: league = "🥉 БРОНЗОВАЯ ЛИГА"
                
                with st.container(border=True):
                    c1, c2, c3 = st.columns([1, 3, 2])
                    c1.write(f"#{place}")
                    if name == st.session_state['user']:
                        c2.info(f"**{name} (ТЫ)**")
                    else:
                        c2.write(name)
                    c2.caption(league)
                    c3.write(f"**{pages} стр.**")
                    
                    
                    if place > 1 and name == st.session_state['user']:
                        target = lb1[i-1]['pages']
                        diff = target - pages + 1
                        st.info(f"До #{place-1} места осталось прочитать {diff} стр.!")

        
        st.divider()
        st.divider()
        st.subheader("📊ГЛОБАЛЬНЫЙ топ")
        
        
        lb = {}
        for b in st.session_state['book']:
            u = b['user']
            lb[u] = lb.get(u, 0) + b['pages']
        
        #сорт
        sorted_top = sorted(lb.items(), key=lambda x: x[1], reverse=True)
        
        for i, (name, p) in enumerate(sorted_top):
            place = "🥇" if i==0 else "🥈" if i==1 else "🥉" if i==2 else "📖"
            st.write(f"{place} {name}: {p} стр.")

        

        
      

