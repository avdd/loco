export default {
    Start,
    FetchCss,
    FetchHome,
    AddStyle,
    AddHome,
}

async function Start(window, loader) {
    const css = await FetchCss(window, './app.css');
    AddStyle(window.document, css);
    const data = await FetchHome(window, './screen/Home');
    AddHome(window.document, data.html);
    if (loader && loader.finish)
        loader.finish();
}

async function FetchCss(window, url) {
    const rsp = await window.fetch(url);
    return await rsp.text();
}

async function FetchHome(window, url) {
    const rsp = await window.fetch(url, { method: 'POST' });
    return await rsp.json();
}

function AddStyle(document, cssText) {
    const s = document.createElement('style');
    s.id = 'LocoStylesheet';
    s.textContent = cssText;
    document.head.appendChild(s);
}

function AddHome(document, html) {
    const el = document.createElement('div');
    el.id = 'LocoContainer';
    el.innerHTML = html;
    document.body.appendChild(el);
}
