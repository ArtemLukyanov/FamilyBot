
// ------------ УСТАНОВИТЕ свой токен! ------------
const TELEGRAM_BOT_TOKEN = '7444859157:AAFo2yC6vxHZ1PG5HYd3JYnlJMALFRcvsXw';
const CHAT_ID           = '-1002820181829';   // ID вашей группы
// ------------------------------------------------

const doctorsData = {
  'Консультация хирурга': [
    { name:'Серобян Анастасия Александровна', img:'https://prodoctorov.ru/media/photo/yalta/doctorimage/724888/2918167-724888-kostina_square_small.jpg' },
    { name:'Кальчук', img:'https://via.placeholder.com/80?text=%D0%9A' },
    { name:'Фасхутдинов Руслан Ильдусович', img:'https://prodoctorov.ru/media/photo/surgut/doctorimage/875138/943142-875138-fashutdinov_square_small.jpg' },
  ],
  'Консультация ортопеда': [
    { name:'Серобян Анастасия Александровна', img:'https://prodoctorov.ru/media/photo/yalta/doctorimage/724888/2918167-724888-kostina_square_small.jpg' },
      { name: 'Кальчук', img:'https://www.meme-arsenal.com/memes/9c5e255a3dc3ffbcfe9d364f65691319.jpg' },
    { name:'Фасхутдинов Руслан Ильдусович', img:'https://prodoctorov.ru/media/photo/surgut/doctorimage/875138/943142-875138-fashutdinov_square_small.jpg' },
  ],
  'Консультация косметолога-дерматолога': [
    { name:'Копчук Оксана Сергеевна', img:'https://prodoctorov.ru/media/photo/yalta/doctorimage/231267/471941-231267-kopchuk_square_small.jpg' },
    { name:'Жидких Анастасия Юрьевна', img:'https://prodoctorov.ru/media/photo/yalta/doctorimage/980540/3587082-980540-zhidkih_square_small.jpg' },
    { name:'Бикбова Елена Анатольевна', img:'https://prodoctorov.ru/media/photo/yalta/doctorimage/231264/634567-231264-bikbova_square_small.jpg' },
  ],
};

const form = document.getElementById('booking-form');
const directionEl = document.getElementById('direction');
const doctorBtn = document.getElementById('doctor-btn');
const doctorList = document.getElementById('doctor-list');
const doctorHidden = document.getElementById('doctor');
const dateEl = document.getElementById('date');
const timeEl = document.getElementById('time');
const fioEl = document.getElementById('fio');
const ageEl = document.getElementById('age');
const phoneEl = document.getElementById('phone');
const commentEl = document.getElementById('comment');
const submitBtn = document.getElementById('submitBtn');

dateEl.min = new Date().toISOString().split('T')[0];

phoneEl.addEventListener('input', () => {
  let d = phoneEl.value.replace(/\D/g, '');
  if (d.startsWith('7')) d = d.slice(1);
  d = d.slice(0, 10);
  let fmt = '+7 (' + d.slice(0, 3);
  if (d.length >= 3) fmt += ') ' + d.slice(3, 6);
  if (d.length >= 6) fmt += '-' + d.slice(6, 8);
  if (d.length >= 8) fmt += '-' + d.slice(8, 10);
  phoneEl.value = fmt;
});

directionEl.addEventListener('change', () => {
  const list = doctorsData[directionEl.value] || [];
  doctorBtn.disabled = !list.length;
  doctorBtn.innerHTML = 'Выберите врача <span class="arrow"></span>';
  doctorHidden.value = '';
  doctorList.innerHTML = list.map(d =>
    `<li data-name="${d.name}" data-img="${d.img}">
        <img src="${d.img}" alt="${d.name}"/>
        <span>${d.name}</span>
     </li>`).join('');
  doctorList.classList.add('hidden');
  validate();
});

doctorBtn.addEventListener('click', () => {
  if (doctorBtn.disabled) return;
  doctorList.classList.toggle('hidden');
});
document.addEventListener('click', e => {
  if (!e.target.closest('.doctor-select')) doctorList.classList.add('hidden');
});

doctorList.addEventListener('click', e => {
  const li = e.target.closest('li');
  if (!li) return;
  const name = li.dataset.name;
  const img  = li.dataset.img;
  doctorBtn.innerHTML = `${name}<img src="${img}" alt="${name}"/>`;
  doctorHidden.value = name;
  doctorList.classList.add('hidden');
  validate();
});

[directionEl, dateEl, timeEl, fioEl, ageEl, phoneEl]
  .forEach(el => el.addEventListener('input', validate));

function validate() {
  const phoneOk = phoneEl.value.replace(/\D/g, '').length === 11;
  const ageOk = parseInt(ageEl.value) > 0;
  const ok = directionEl.value && doctorHidden.value && dateEl.value
           && timeEl.value && fioEl.value.trim().length > 5
           && ageOk && phoneOk;
  submitBtn.disabled = !ok;
}
validate();

function formatDateToRussian(dateStr) {
  const months = ['января','февраля','марта','апреля','мая','июня','июля','августа','сентября','октября','ноября','декабря'];
  const [y,m,d] = dateStr.split('-');
  return `${d}-${months[parseInt(m,10)-1]}-${y}`;
}

form.addEventListener('submit', async e => {
  e.preventDefault();
  submitBtn.disabled = true;

  const text = [
    '*❗ НОВАЯ ЗАПИСЬ ❗*',
    `*Направление:* ${directionEl.value}`,
    `*Врач:* ${doctorHidden.value}`,
    `*Дата:* ${formatDateToRussian(dateEl.value)} ${timeEl.value}`,
    `*Пациент:* ${fioEl.value}`,
    `*Возраст:* ${ageEl.value}`,
    `*Тел.:* ${phoneEl.value}`,
    commentEl.value ? `*Комментарий:* ${commentEl.value}` : ''
  ].filter(Boolean).join('%0A');

  try {
    const url = `https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage?`
              + `chat_id=${CHAT_ID}&parse_mode=Markdown&text=${text}`;
    const res = await fetch(url);
    const data = await res.json();
    if(data.ok){
      form.innerHTML = '<h3 style="text-align:center;margin:40px 0">Спасибо! Заявка отправлена.</h3>';
    } else {
      alert('Ошибка: ' + data.description);
      submitBtn.disabled = false;
    }
  } catch (err) {
    alert('Сетевая ошибка, попробуйте позже.');
    console.error(err);
    submitBtn.disabled = false;
  }
});
