const rsp = await fetch('./app.css')
const s = document.createElement('style');
s.id = 'AppStyleBundle';
s.textContent = await rsp.text()
document.head.appendChild(s);

const p = document.createElement('p');
p.textContent = 'Hello, world!'
p.className = 'Home';
document.body.appendChild(p);
