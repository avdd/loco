// @ts-check
import App from '../../src/loco/app.js';

function mockWindow(data, spy) {
    const resolve = () => Promise.resolve(data);
    const rsp = { text: resolve, json: resolve };
    return {
        fetch(url, options) {
            spy.push({ url, options });
            return Promise.resolve(rsp);
        }
    }
}

function mockDocument(spy) {
    const node = {
        appendChild(element) {
            spy.push(element);
        }
    }
    return {
        head: node,
        body: node,
        createElement(tagName) {
            return { tagName }
        }
    }
}

describe('app', function () {

    it('fetches css', async function () {
        const url = 'css-url';
        const testCss = 'css data';
        const spy = []
        const win = mockWindow(testCss, spy);
        const css = await App.FetchCss(win, url);
        expect(spy[0].url).toBe(url);
        expect(css).toBe(testCss);
    })

    it('adds stylesheet', function () {
        const cssText = 'mock css';
        const spy = [];
        const doc = mockDocument(spy);
        App.AddStyle(doc, cssText);
        const result = spy[0];
        expect(result.tagName).toBe('style');
        expect(result.textContent).toBe(cssText);
    })

    it('fetches home', async function () {
        const url = 'home-url';
        const rsp = { html: '<h1>Hello</h1>' }
        const spy = [];
        const win = mockWindow(rsp, spy);
        const data = await App.FetchHome(win, url);
        expect(spy[0].url).toBe(url);
        expect(spy[0].options.method).toBe('POST');
        expect(data.html).toBe(rsp.html);
    })

    it('adds home content', function () {
        const homeContent = '<p>content';
        const spy = [];
        const doc = mockDocument(spy);
        App.AddHome(doc, homeContent);
        const result = spy[0];
        expect(result.tagName).toBe('div');
        expect(result.innerHTML).toBe(homeContent);
    })
})
