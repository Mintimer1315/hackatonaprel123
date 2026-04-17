import streamlit as st

# 1инциализации
if 'auth' not in st.session_state:
    st.session_state['auth'] = False
if 'user' not in st.session_state:
    st.session_state['user'] = ""
if 'challenges' not in st.session_state:
    
    st.session_state['challenges'] = {
        "Марафон Казани": ["Ильнур", "ярик"],
        "Книжная битва 5А": ["Дима"]
    }

# вход
if not st.session_state['auth']:
    st.title("📚 Reading Challenge")
    st.subheader("Регистрация участника")
    
    u_name = st.text_input("Как тебя зовут?")
    if st.button("Войти в систему"):
        if u_name:
            st.session_state['auth'] = True
            st.session_state['user'] = u_name
            st.rerun()
        else:
            st.error("Введи имя!")

#основа
else:
    st.sidebar.write(f"👤 Игрок: **{st.session_state['user']}**")
    if st.sidebar.button("Выйти"):
        st.session_state['auth'] = False
        st.rerun()

  
    t1, t2, t3,t4 = st.tabs(["🏠 Главная", "➕ Создать", "🏆 Соревнования", "🎯 Рейтинг"])

    with t1:
        st.write(f"Привет, {st.session_state['user']}! Здесь твой прогресс.")
        st.info("Выбери соревнование во вкладке 'Рейтинг', чтобы начать соревноваться!")

    with t2:
        st.subheader("Создать новое соревнование")
        c_name = st.text_input("Название (например: Битва лицеев)")
        if st.button("Опубликовать"):
            if c_name:
                
                st.session_state['challenges'][c_name] = [st.session_state['user']]
                st.success(f"Челлендж '{c_name}' создан!")
                st.balloons()
            else:
                st.error("Введи название!")

    with t3:
        st.subheader("Доступные соревнования")
      
        for name, members in st.session_state['challenges'].items():
            with st.container(border=True):
                st.write(f"**{name}**")
                st.caption(f"Участники: {', '.join(members)}")
                
                
                if st.button(f"Вступить", key=name):
                    if st.session_state['user'] not in members:
                        st.session_state['challenges'][name].append(st.session_state['user'])
                        st.success("Ты в деле!")
                        st.rerun()
                    else:
                        st.warning("Ты уже там!")
    with t4:
      st.subheader("Твой рейтинг в соревновние:", c_name)
      

