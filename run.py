import telebot
from telebot import types
import datetime

API_TOKEN = '7444859157:AAFo2yC6vxHZ1PG5HYd3JYnlJMALFRcvsXw'
bot = telebot.TeleBot(API_TOKEN)

# Храним состояния и данные пользователей
user_states = {}
user_data = {}

# Информация по услугам — заполните описания в этой структуре
service_info = {
    "dentistry": {
        "Терапевтическая стоматология": "Терапевтическая стоматология: \n\nДиагностика, лечение и профилактика заболеваний зубов и дёсен. Основное внимание уделяется лечению кариеса, лечению пульпита, лечению периодонтита и других воспалительных процессов. Проводятся процедуры по чистке зубов, реставрации зубов, пломбированию зубов.",      # TODO: добавьте описание услуги
        "Хирургическая стоматология": "Хирургическая стоматология: \n\nОперативное и плановое вмешательство для лечения заболеваний и патологий зубочелюстной системы. Включает в себя удаление зубов, имплантацию, коррекцию врожденных и приобретенных дефектов, лечение травм и инфекций. Основная цель хирургической стоматологии - восстановление функциональности и эстетики ротовой полости, а также улучшение качества жизни пациента.",
        "Имплантация зубов": "Имплантация зубов:  \n\nСовременный метод восстановления утраченных зубов, который включает в себя установку искусственного корня (импланта) в челюстную кость. Имплант служит основой для последующего крепления коронки, мостовидного протеза или съёмного протеза. Этот метод позволяет восстановить функциональность и эстетику зубного ряда, обеспечивая долговечность и надежность результата. Имплантация зубов помогает улучшить качество жизни пациента, возвращая комфорт при жевании и уверенность в улыбке.",
        "Ортопедическая стоматология": "Ортопедическая стоматология:\n\nОсновная цель ортопедической стоматологии в Ялте - восстановление жевательной функции, улучшение эстетики улыбки и повышение качества жизни пациента. Включает в себя изготовление и установку коронок, виниров, мостовидных протезов, а также съёмных и несъёмных зубных протезов.",
        "Ортодонтическая стоматология": "Ортодонтическая стоматология:\n\nГлавной задачей ортодонтии является исправление неправильного прикуса и выравнивание зубов для улучшения функции жевания, речи и эстетики улыбки. Лечение может включать использование брекетов, элайнеров, капп и других ортодонтических аппаратов, которые помогают перемещать зубы в правильное положение.",
        "Детская стоматология": "Детская стоматология:\n\nУход за зубами детей от младенчества до подросткового возраста. Основной акцент детской стоматологии приходится на профилактику и лечение заболеваний полости рта у детей, а также обучение правильной гигиене полости рта. Врачи-стоматологи, работающие в этой области, имеют специальные навыки для работы с детьми и создания комфортной атмосферы во время визитов. Лечение может включать профилактические осмотры, пломбирование кариеса, герметизацию фиссур и ортодонтические консультации.",
        "Рентген зубов": "Рентген зубов:\n\nСнимки зубов на немецком томографе Sirona Orthophos XG 3D",
    },
    "cosmetology": {
        "Удаление новообразований": "",          # TODO: добавьте описание услуги
        "Лазерная эпиляция": "",
        "Лазерное омоложение и отбеливание": "",
        "Космецевтические уходы": "",
        "Дерматологические пилинги": "",
        "Безоперационный лифтинг нитями": "",
        "Ботулинотерапия": "",
        "Мезотерапия": "",
        "Контурная пластика": "",
        "Биоревитализация": "",
    }
}

# Кнопка "Главное меню"
main_menu_button = types.InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")

# Функция для отправки главного меню
def send_main_menu(chat_id):
    user_states[chat_id] = None
    user_data[chat_id] = {}
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📆  Онлайн запись на консультацию ", callback_data="book"))
    markup.add(types.InlineKeyboardButton("🔥  Акции ", callback_data="promo"))
    markup.add(types.InlineKeyboardButton("📲  Соцсети ", callback_data="socials"))
    markup.add(types.InlineKeyboardButton("📋  Список услуг ", callback_data="services"))
    markup.add(types.InlineKeyboardButton("☎️  Контакты ", callback_data="contacts"))
    bot.send_message(
        chat_id,
        "❤️ Добро пожаловать в Family Clinic ! Мы — команда профессионалов с многолетним опытом...\n\nЧто вас интересует?",
        reply_markup=markup
    )

# === Хендлер /start ===
@bot.message_handler(commands=['start'])
def handle_start(message):
    send_main_menu(message.chat.id)

# === Обработка callbackQuery ===
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    chat_id = call.message.chat.id
    data = call.data

    # Главное меню
    if data == "main_menu":
        send_main_menu(chat_id)
        return

    if data == "promo":
        markup = types.InlineKeyboardMarkup()
        markup.add(main_menu_button)
        bot.send_message(chat_id, "Действующие акции: ...", reply_markup=markup)

    elif data == "socials":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Telegram", url="https://t.me/family_clinic_pro"))
        markup.add(types.InlineKeyboardButton("ВКонтакте", url="https://vk.com/cosmetyalta?from=search"))
        markup.add(main_menu_button)
        bot.send_message(chat_id, "Мы будем рады видеть Вас в социальных сетях!", reply_markup=markup)

    elif data == "contacts":
        markup = types.InlineKeyboardMarkup()
        markup.add(main_menu_button)
        bot.send_message(
            chat_id,
            "Клиника работает ежедневно с 09:00 до 19:00\n"
            "Адрес: г. Ялта, ул. Боткинская, 13А\n"
            "Телефон: 📞 +7 (978) 756-50-20",
            reply_markup=markup
        )

    # === Список услуг: выбор раздела ===
    elif data == "services":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🦷 Стоматология", callback_data="services|dentistry"))
        markup.add(types.InlineKeyboardButton("✨ Косметология и дерматология", callback_data="services|cosmetology"))
        markup.add(main_menu_button)
        bot.send_message(chat_id, "Выберите раздел услуг:", reply_markup=markup)

    # === Список услуг: выбор конкретного направления ===
    elif data.startswith("services|"):
        _, section = data.split("|", 1)
        items = list(service_info.get(section, {}).keys())
        if not items:
            markup = types.InlineKeyboardMarkup()
            markup.add(main_menu_button)
            bot.send_message(chat_id, "Информация по этому разделу пока отсутствует.", reply_markup=markup)
            return

        markup = types.InlineKeyboardMarkup(row_width=1)
        for idx, name in enumerate(items):
            markup.add(types.InlineKeyboardButton(name, callback_data=f"service|{section}|{idx}"))
        markup.add(main_menu_button)
        bot.send_message(chat_id, "Выберите услугу:", reply_markup=markup)

    # === Список услуг: показ информации по выбранной услуге ===
    elif data.startswith("service|"):
        _, section, idx_str = data.split("|", 2)
        try:
            idx = int(idx_str)
            items = list(service_info.get(section, {}).items())
            name, info = items[idx]
        except (ValueError, IndexError):
            markup = types.InlineKeyboardMarkup()
            markup.add(main_menu_button)
            bot.send_message(chat_id, "Ошибка выбора услуги. Попробуйте ещё раз.", reply_markup=markup)
            return

        markup = types.InlineKeyboardMarkup()
        markup.add(main_menu_button)
        if info:
            bot.send_message(chat_id, info, reply_markup=markup)
        else:
            bot.send_message(chat_id, f"Описание услуги «{name}» пока не добавлено. Скоро будет доступно.", reply_markup=markup)

    # === Начало потока записи на консультацию ===
    elif data == "book":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Консультация хирурга", callback_data="consult|surgeon"))
        markup.add(types.InlineKeyboardButton("Консультация ортопеда", callback_data="consult|orthopedist"))
        markup.add(types.InlineKeyboardButton("Консультация косметолога-дерматолога", callback_data="consult|cosmetolog"))
        markup.add(main_menu_button)
        bot.send_message(chat_id, "Выберите тип консультации:", reply_markup=markup)

    # Выбор типа консультации -> список врачей
    elif data.startswith("consult|"):
        _, typ = data.split("|", 1)
        user_data[chat_id]['consult_type'] = typ
        user_states[chat_id] = 'choosing_doctor'
        markup = types.InlineKeyboardMarkup()
        if typ in ['surgeon', 'orthopedist']:
            doctors = ["Серобян", "Кальчук", "Фасхутдинов"]
        else:
            doctors = ["Копчук", "Жидких", "Бикбова"]
        for doc in doctors:
            markup.add(types.InlineKeyboardButton(doc, callback_data=f"select_doc|{doc}"))
        markup.add(main_menu_button)
        bot.send_message(chat_id, "Выберите врача:", reply_markup=markup)

    # Выбор врача -> выбор даты
    elif data.startswith("select_doc|"):
        _, doc = data.split("|", 1)
        user_data[chat_id]['doctor'] = doc
        user_states[chat_id] = 'choosing_date'
        markup = types.InlineKeyboardMarkup(row_width=4)
        today = datetime.date.today()
        for i in range(7):
            d = today + datetime.timedelta(days=i)
            txt = d.strftime("%d.%m.%Y")
            markup.add(types.InlineKeyboardButton(txt, callback_data=f"date|{txt}"))
        markup.add(main_menu_button)
        bot.send_message(chat_id, "Выберите дату консультации:", reply_markup=markup)

    # Выбор даты -> выбор времени
    elif data.startswith("date|"):
        _, dt = data.split("|", 1)
        user_data[chat_id]['date'] = dt
        user_states[chat_id] = 'choosing_time'
        markup = types.InlineKeyboardMarkup(row_width=4)
        for h in range(9, 19):
            t = f"{h:02d}:00"
            markup.add(types.InlineKeyboardButton(t, callback_data=f"time|{t}"))
        markup.add(main_menu_button)
        bot.send_message(chat_id, "Выберите время:", reply_markup=markup)

    # Выбор времени -> запрос ФИО
    elif data.startswith("time|"):
        _, tm = data.split("|", 1)
        user_data[chat_id]['time'] = tm
        user_states[chat_id] = 'await_name'
        markup = types.InlineKeyboardMarkup()
        markup.add(main_menu_button)
        bot.send_message(chat_id, "Пожалуйста, введите ваше ФИО:", reply_markup=markup)

# === Обработка текстовых ответов ===
@bot.message_handler(func=lambda m: user_states.get(m.chat.id) == 'await_name')
def handle_name(message):
    chat_id = message.chat.id
    user_data[chat_id]['name'] = message.text
    user_states[chat_id] = 'await_dob'
    markup = types.InlineKeyboardMarkup()
    markup.add(main_menu_button)
    bot.send_message(chat_id, "Введите дату рождения в формате ДД.MM.ГГГГ:", reply_markup=markup)

@bot.message_handler(func=lambda m: user_states.get(m.chat.id) == 'await_dob')
def handle_dob(message):
    chat_id = message.chat.id
    user_data[chat_id]['dob'] = message.text
    user_states[chat_id] = 'await_phone'
    markup = types.InlineKeyboardMarkup()
    markup.add(main_menu_button)
    bot.send_message(chat_id, "Введите номер телефона (например, +7XXXXXXXXXX):", reply_markup=markup)

@bot.message_handler(func=lambda m: user_states.get(m.chat.id) == 'await_phone')
def handle_phone(message):
    chat_id = message.chat.id
    user_data[chat_id]['phone'] = message.text

    # Финальное подтверждение
    ct = user_data[chat_id]['consult_type']
    doc = user_data[chat_id]['doctor']
    dt = user_data[chat_id]['date']
    tm = user_data[chat_id]['time']
    markup = types.InlineKeyboardMarkup()
    markup.add(main_menu_button)
    bot.send_message(
        chat_id,
        f"Вы записались на консультацию {ct} {dt} в {tm} к врачу {doc}.\nДо встречи в Family Clinic!",
        reply_markup=markup
    )
    user_states[chat_id] = None
    user_data[chat_id].clear()

if __name__ == '__main__':
    bot.infinity_polling()
