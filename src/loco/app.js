export async function Start(window, loader) {
    await FetchStyleBundle(window.document);
    await FetchHome(window.document);
    if (loader && loader.finish)
        loader.finish();
}

export async function FetchCss(window, url) {
    const rsp = await window.fetch(url);
    return await rsp.text();
}

// export function AddStyle(document, cssText) {
//     const s = document.createElement('style');
//     s.id = 'AppStyleBundle';
//     s.textContent = cssText;
//     document.head.appendChild(s);
// }

async function FetchStyleBundle(doc) {
    const rsp = await fetch('./app.css')
    const css = await rsp.text();
    const s = doc.createElement('style');
    s.id = 'AppStyleBundle';
    s.textContent = css;
    doc.head.appendChild(s);
}

async function FetchHome(doc) {
    const rsp = await fetch('./screen/Home', { method: 'POST' });
    const data = await rsp.json();
    console.log(data);
    const root = doc.createElement('div')
    root.id = 'AppRoot';
    root.innerHTML = data.html;
    doc.body.appendChild(root);
}
