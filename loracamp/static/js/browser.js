const browser = document.querySelector('#browser');
const browseButtonFooter = document.querySelector('footer button.browse-btn:not(.theme-toggle)');
const browseButtonHeader = document.querySelector('header button.browse-btn:not(.theme-toggle)');

const browseResults = browser.querySelector('#results');
const closeButton = browser.querySelector('.close-browser');
const searchField = browser.querySelector('input');
const statusField = browser.querySelector('[role="status"]');

const indexSuffix = window.location.pathname.endsWith('index.html') ? 'index.html' : '';
const rootPrefix = browser.dataset.rootPrefix;

function truncateArtistList(artists, othersLink)  {
    const MAX_CHARS = 40;

    if (artists.length > 2) {
        const nameChars = artists.reduce((sum, artist) => sum + artist.name.length, 0);
        const separatorChars = (artists.length - 1) * 2; // All separating ", " between the artists

        if (nameChars + separatorChars > MAX_CHARS) {
            // Here we have more than two artists, we have a char limit,
            // and we cannot fit all artists within the limit, thus
            // we truncate the list.

            if (LABEL_MODE) {
                // In label mode we show at least one artist, then as many
                // additional ones as fit, e.g. "[artist],[artist] and
                // more"
                let charsUsed = 0;
                const truncatedArtists = artists
                    .filter(artist => {
                        if (charsUsed === 0) {
                            charsUsed += artist.name.length;
                            return true;
                        }

                        charsUsed += artist.name.length;
                        return charsUsed < MAX_CHARS;
                    });

                const rArtists = truncatedArtists
                    .map(artist => {
                        const url = artist.externalPage ?? `${rootPrefix}${artist.url}${indexSuffix}`;
                        return `<a href="${url}">${artist.name}</a>`;
                    })
                    .join(", ");

                return BROWSER_JS_T.xxxAndOthers(rArtists, othersLink);
            }

            // In artist mode we show only "[catalog artist] and others".
            // Our sorting ensures the catalog artist is the first one,
            // so we can just take that.
            const rArtists = `<a href="${rootPrefix}${artists[0].url}${indexSuffix}">${artists[0].name}</a>`;

            return BROWSER_JS_T.xxxAndOthers(rArtists, othersLink);
        }
    }

    return artists
        .map(artist => {
            const url = artist.externalPage ?? `${rootPrefix}${artist.url}${indexSuffix}`;
            return `<a href="${url}">${artist.name}</a>`;
        })
        .join(", ");
}

for (const model of MODELS) {
    let imgModel;
    if (model.cover) {
        imgModel = document.createElement('img');
        imgModel.src = rootPrefix + model.url + model.cover;
    } else {
        imgModel = document.createElement('span');
        imgModel.classList.add('placeholder');
    }

    const aText = document.createElement('a');
    aText.href = rootPrefix + model.url + indexSuffix;

    const aImage = aText.cloneNode(true);
    aImage.tabIndex = -1;
    aImage.appendChild(imgModel);

    aText.dataset.searchable = 'true';
    if (model.tags && model.tags.length > 0) {
        aText.dataset.tags = model.tags.join(' ');
    }
    aText.textContent = model.title;

    const details = document.createElement('div');
    details.appendChild(aText);

    if (model.creator) {
        const creator = document.createElement('div');
        creator.classList.add('artists'); // Keeping class name for CSS compatibility
        creator.textContent = model.creator;
        details.appendChild(creator);
    }

    const row = document.createElement('div');
    row.appendChild(aImage);
    row.appendChild(details);
    browseResults.appendChild(row);

    for (const track of model.tracks) {
        let imgTrack;
        if (track.cover) {
            imgTrack = document.createElement('img');
            imgTrack.src = rootPrefix + model.url + track.cover;
        } else {
            imgTrack = imgModel.cloneNode(true);
        }

        const number = document.createElement('span');
        number.classList.add('number');
        number.textContent = track.number;

        const aTitle = document.createElement('a');
        aTitle.href = rootPrefix + track.url + indexSuffix;

        const aImage = aTitle.cloneNode(true);
        aImage.tabIndex = -1;
        aImage.appendChild(imgTrack);

        aTitle.dataset.searchable = 'true';
        if (track.tags && track.tags.length > 0) {
            aTitle.dataset.tags = track.tags.join(' ');
        }
        aTitle.textContent = track.title;

        const details = document.createElement('div');
        details.appendChild(number);
        details.appendChild(aTitle);

        const row = document.createElement('div');
        row.appendChild(aImage);
        row.appendChild(details);
        row.dataset.track = '';
        row.style.setProperty('display', 'none');
        browseResults.appendChild(row);
    }
}

for (const creator of CREATORS) {
    const aText = document.createElement('a');
    aText.href = rootPrefix + creator.url + indexSuffix;

    let imageCreator;
    if (creator.image) {
        imageCreator = document.createElement('img');
        imageCreator.classList.add('crop');
        imageCreator.src = rootPrefix + creator.url + creator.image;
    } else {
        imageCreator = document.createElement('span');
        imageCreator.classList.add('placeholder');
    }

    const aImage = aText.cloneNode(true);
    aImage.tabIndex = -1;
    aImage.appendChild(imageCreator);

    aText.dataset.searchable = 'true';
    aText.textContent = creator.name;

    const details = document.createElement('div');
    details.appendChild(aText);

    const row = document.createElement('div');
    row.appendChild(aImage);
    row.appendChild(details);
    browseResults.appendChild(row);
}

function hideBrowser() {
    const browseButton = (browseButtonFooter && browseButtonFooter.getAttribute('aria-expanded') === 'true')
        ? browseButtonFooter
        : browseButtonHeader;

    browser.classList.remove('active');
    if (browseButton) {
        browseButton.setAttribute('aria-expanded', 'false');
    }
    searchField.value = '';
    statusField.removeAttribute('aria-label');
    statusField.textContent = '';
    for (const result of browseResults.children) {
        const display = result.dataset.track === undefined;
        result.style.setProperty('display', display ? null : 'none');
    }
    if (browseButton) {
        browseButton.focus();
    }
}

function showBrowser(browseButton) {
    browser.classList.add('active');
    browseButton.setAttribute('aria-expanded', 'true');
    searchField.focus();
    statusField.setAttribute('aria-label', BROWSER_JS_T.showingFeaturedItems);
    statusField.textContent = '';
}

// When the browse/search modal is open and focus moves outside the page
// entirely (e.g. to the addressbar) but then re-enters the page, we need
// to make sure that it returns back to the browse/search modal (instead of
// to an obscured element in the main body)
document.body.addEventListener('focusin', event => {
    if (browser.classList.contains('active') && !browser.contains(event.target)) {
        searchField.focus();
    }
});

browser.addEventListener('focusout', event => {
    if (browser.classList.contains('active') && event.relatedTarget && !browser.contains(event.relatedTarget)) {
        hideBrowser();
    }
});

browser.addEventListener('keydown', event => {
    if (event.key === 'Escape') {
        event.preventDefault();
        hideBrowser();
    }
});

browseButtonFooter?.addEventListener('click', () => showBrowser(browseButtonFooter));
browseButtonHeader?.addEventListener('click', () => showBrowser(browseButtonHeader));

closeButton?.addEventListener('click', hideBrowser);

searchField.addEventListener('input', () => {
    const query = searchField.value.trim();

    if (query.length) {
        const regexp = new RegExp(query.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'i');
        let shown = 0;

        for (const element of browseResults.children) {
            const searchableEl = element.querySelector('[data-searchable]');
            const title = searchableEl.textContent;
            const tags = searchableEl.dataset.tags || '';
            const creator = element.querySelector('.artists')?.textContent || '';
            const searchString = `${title} ${tags} ${creator}`.toLowerCase();
            const display = regexp.test(searchString);
            element.style.setProperty('display', display ? null : 'none');
            if (display) { shown += 1; }
        }

        if (shown === 0) {
            statusField.removeAttribute('aria-label');
            statusField.textContent = BROWSER_JS_T.nothingFoundForXxx(query);
        } else {
            statusField.setAttribute('aria-label', BROWSER_JS_T.showingXxxResultsForXxx(shown, query));
            statusField.textContent = '';
        }
    } else {
        for (const element of browseResults.children) {
            const display = element.dataset.track === undefined;
            element.style.setProperty('display', display ? null : 'none');
        }

        statusField.setAttribute('aria-label', BROWSER_JS_T.showingFeaturedItems);
        statusField.textContent = '';
    }
});
// Initial state and auto-open from query param
if (window.location.search.includes('search=true')) {
    // We need to wait a tiny bit for the DOM and scripts to be ready
    window.addEventListener('load', () => {
        const btn = browseButtonHeader || browseButtonFooter;
        if (btn) showBrowser(btn);
    });
}
