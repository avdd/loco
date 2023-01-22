// @ts-check
import { FetchCss, AddStyle, FetchHome } from '../../src/loco/app.js';

function mockWindow(data) {
    return {
        fetch(url, options) {
            this.calledArgs = { url, options };
            const rsp = {
                async text() {
                    return Promise.resolve(data);
                },
                async json() {
                    return Promise.resolve(data);
                }
            }
            return Promise.resolve(rsp);
        }
    }
}

function mockDocument() {
    const _styles = [];
    return {
        _styles,
        head: {
            appendChild(element) {
                _styles.push(element);
            }
        },
        createElement(name) {
            return { tag: name }
        }
    }
}

describe('app', function () {

    it('fetches css', async function () {
        const testCss = 'css data';
        const win = mockWindow(testCss);
        const css = await FetchCss(win, 'url');
        expect(win.calledArgs.url).toBe('url');
        expect(css).toBe(testCss);
    })

    it('adds stylesheet', function () {
        const cssText = 'mock css';
        const doc = mockDocument();
        AddStyle(doc, cssText);
        expect(doc._styles[0].textContent).toBe(cssText);
    })

    it('fetches body', async function () {
        const rsp = { html: '<h1>Hello</h1>' }
        const win = mockWindow(rsp);
        const data = await FetchHome(win, './home');
        expect(win.calledArgs.url).toBe('./home');
        expect(win.calledArgs.options.method).toBe('POST');
        expect(data.html).toBe(rsp.html);
    })
})
