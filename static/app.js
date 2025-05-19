const API = '/api/';
let TOKEN = localStorage.getItem('token') || null;

async function fetchJSON(url, opts = {}) {
    opts.headers = {
        'Content-Type': 'application/json',
        ...(opts.headers || {}),
        ...(TOKEN ? {Authorization: `Token ${TOKEN}`} : {}),
    };
    const r = await fetch(url, opts);
    return await r.json();
}


async function loadResumes() {
    const ul = document.getElementById('resume-list');
    if (!ul || !TOKEN) return; // ✅ запрет просмотра без токена
    ul.innerHTML = '';
    const data = await fetchJSON(API + 'resumes/');
    data.slice(-5).forEach((r) => {
        let li = document.createElement('li');
        li.textContent = `${r.id}: ${r.full_name}`;
        ul.appendChild(li);
    });
}


async function loadVacancies() {
    const ul = document.getElementById('vacancy-list');
    const sel = document.getElementById('match-select');
    if (!ul || !sel) return;
    ul.innerHTML = '';
    sel.innerHTML = '<option value="">-- выберите вакансию --</option>';

    const data = await fetchJSON(API + 'vacancies/');

    // Для списка вакансий показываем последние 5
    data.slice(-5).forEach((v) => {
        let li = document.createElement('li');
        li.textContent = `${v.id}: ${v.name}`;
        ul.appendChild(li);
    });

    // Для выпадающего списка показываем все вакансии
    data.forEach((v) => {
        let opt = document.createElement('option');
        opt.value = v.id;
        opt.textContent = v.name;
        sel.appendChild(opt);
    });
}



// Обработка форм — резюме и вакансии (если есть на странице)
const resumeForm = document.getElementById('resume-form');
if (resumeForm) {
    resumeForm.onsubmit = async (e) => {
        e.preventDefault();
        const body = {
            full_name: e.target['res-full_name'].value,
            phone_number: e.target['res-phone_number'].value,
            mail: e.target['res-mail'].value,
            text: e.target['res-text'].value,
            salary: e.target['res-salary'].value,
        };
        await fetch(API + 'resumes/', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(body),
        });
        e.target.reset();
        if (TOKEN) loadResumes();
    };
}

const vacancyForm = document.getElementById('vacancy-form');
if (vacancyForm) {
    vacancyForm.onsubmit = async (e) => {
        e.preventDefault();
        const body = {
            name: e.target['vac-name'].value,
            description: e.target['vac-desc'].value,
        };
        await fetchJSON(API + 'vacancies/', {
            method: 'POST',
            body: JSON.stringify(body),
        });
        e.target.reset();
        loadVacancies();
    };
}

const btnMatch = document.getElementById('btn-match');
if (btnMatch) {
    btnMatch.onclick = async () => {
        const vid = document.getElementById('match-select').value;
        if (!vid) return alert('Выберите вакансию');
        const data = await fetchJSON(API + `match/${vid}/`);
        const ul = document.getElementById('match-results');
        ul.innerHTML = '';

        for (let m of data.slice(0, 5)) {
            const resume = await fetchJSON(API + `resumes/${m.resume_id}/`);

            let contacts = '';
            if (resume.phone_number) contacts = `<span class="contact">Телефон: ${resume.phone_number}</span>`;
            else if (resume.mail) contacts = `<span class="contact">Email: ${resume.mail}</span>`;

            let li = document.createElement('li');
            li.classList.add('match-item');
            li.innerHTML = `
                <div class="match-header">
                    <span class="resume-id">Резюме ${m.resume_id}</span>
                    <em class="score">${m.score.toFixed(2)}%</em>
                </div>
                <div class="match-text">${m.text}</div>
                <div class="match-contact">— ${resume.full_name} ${contacts}</div>
            `;
            ul.appendChild(li);
        }
    };
}

