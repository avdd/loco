// @ts-check
import { FetchCss } from '../../src/loco/app.js';

function fetchMocker(data) {
    return {
        fetch(url, options) {
            this.calledArgs = { url, options };
            const rsp = {
                async text() {
                    return Promise.resolve(data);
                }
            }
            return Promise.resolve(rsp);
        }
    }
}

describe('app', function () {
    it('fetches css', async function () {
        const testCss = 'css data';
        const win = fetchMocker(testCss);
        const css = await FetchCss(win, 'url');
        expect(win.calledArgs.url).toBe('url');
        expect(css).toBe(testCss);
    })
})
