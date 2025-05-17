const API = '/api/';
let TOKEN = localStorage.getItem('token') || null;

async function fetchJSON(url, opts={}) {
  opts.headers = {
    'Content-Type':'application/json',
    ...(opts.headers||{}),
    ...(TOKEN ? { 'Authorization': `Token ${TOKEN}` } : {})
  };
  const r = await fetch(url, opts);
  return await r.json();
}

// Загрузка данных
async function loadResumes(){
  const ul = document.getElementById('resume-list');
  ul.innerHTML = '';
  const data = await fetchJSON(API + 'resumes/');
  data.forEach(r => {
    let li = document.createElement('li');
    li.textContent = `${r.id}: ${r.full_name}`;
    ul.appendChild(li);
  });
}

async function loadVacancies(){
  const ul = document.getElementById('vacancy-list');
  const sel = document.getElementById('match-select');
  ul.innerHTML = '';
  sel.innerHTML = '<option value="">-- выберите вакансию --</option>';
  const data = await fetchJSON(API + 'vacancies/');
  data.forEach(v => {
    let li = document.createElement('li');
    li.textContent = `${v.id}: ${v.name}`;
    ul.appendChild(li);
    let opt = document.createElement('option');
    opt.value = v.id; opt.textContent = v.name;
    sel.appendChild(opt);
  });
}

// Формы
document.getElementById('resume-form').onsubmit = async e => {
  e.preventDefault();
  const body = {
    full_name:    e.target['res-full_name'].value,
    phone_number: e.target['res-phone_number'].value,
    mail:         e.target['res-mail'].value,
    text:         e.target['res-text'].value,
  };
  await fetchJSON(API + 'resumes/', {
    method: 'POST',
    body: JSON.stringify(body)
  });
  e.target.reset();
  loadResumes();
};

document.getElementById('vacancy-form').onsubmit = async e => {
  e.preventDefault();
  const body = {
    name:        e.target['vac-name'].value,
    description: e.target['vac-desc'].value,
  };
  await fetchJSON(API + 'vacancies/', {
    method: 'POST',
    body: JSON.stringify(body)
  });
  e.target.reset();
  loadVacancies();
};

// Матчи
document.getElementById('btn-match').onclick = async () => {
  const vid = document.getElementById('match-select').value;
  if (!vid) return alert('Выберите вакансию');
  const data = await fetchJSON(API + `match/${vid}/`);
  const ul = document.getElementById('match-results');
  ul.innerHTML = '';
  data.forEach(m => {
    let li = document.createElement('li');
    li.textContent = `Resume ${m.resume_id}: ${m.score}% — ${m.text}`;
    ul.appendChild(li);
  });
};

// Логин/логаут
document.getElementById('login-form').onsubmit = async e => {
  e.preventDefault();
  const email = e.target['login-email'].value;
  const password = e.target['login-password'].value;
  const resp = await fetchJSON('/api-token-auth/', {
    method: 'POST',
    body: JSON.stringify({ username: email, password })
  });
  if (resp.token) {
    TOKEN = resp.token;
    localStorage.setItem('token', TOKEN);
    document.getElementById('login-form').style.display = 'none';
    document.getElementById('btn-logout').style.display = 'inline';
    loadResumes();
    loadVacancies();
  } else {
    alert('Не удалось войти');
  }
};

document.getElementById('btn-logout').onclick = () => {
  TOKEN = null;
  localStorage.removeItem('token');
  location.reload(); // перезагрузка страницы
};


// Инициализация
window.addEventListener('DOMContentLoaded', () => {
  if (TOKEN) {
    document.getElementById('login-form').style.display = 'none';
    document.getElementById('btn-logout').style.display = 'inline';
  }
  loadResumes();
  loadVacancies();
});
