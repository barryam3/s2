import { S2Page } from './app.po';

describe('s2 App', () => {
  let page: S2Page;

  beforeEach(() => {
    page = new S2Page();
  });

  it('should display welcome message', () => {
    page.navigateTo();
    expect(page.getParagraphText()).toEqual('Welcome to app!');
  });
});
