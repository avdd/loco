export async function Start() {
    await FetchStyleBundle();
    await FetchHome();
}

async function FetchStyleBundle() {
    const rsp = await fetch('./app.css')
    const s = document.createElement('style');
    s.id = 'AppStyleBundle';
    s.textContent = await rsp.text()
    document.head.appendChild(s);
}

async function FetchHome() {
    const rsp = await fetch('./screen/Home', { method: 'POST' });
    const data = await rsp.json();
    console.log(data);
    const root = document.createElement('div')
    root.id = 'AppRoot';
    root.innerHTML = data.html;
    document.body.appendChild(root);
}
