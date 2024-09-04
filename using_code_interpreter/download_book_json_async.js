// Rewrite the for loop to download all the books in parallel with a controlled number of concurrent tabs
const maxConcurrentTabs = 5; // This can be adjusted to allow more or fewer simultaneous downloads

async function downloadBooksInParallel(books, maxTabs) {
    const semaphore = new Array(maxTabs).fill(Promise.resolve());

    async function downloadBook(book) {
        const browser = await puppeteer.launch({
            headless: false,
            defaultViewport: null,
            userDataDir: '/Users/michael/Library/Application Support/Google/Chrome/LibbyProfile',
            args: ['--disable-blink-features=AutomationControlled']
        });
        const page = await browser.newPage();
        await page.setExtraHTTPHeaders({
            'Connection': 'keep-alive',
            'DNT': '1',
        });

        if (!book.reading_journey_url) {
            book.reading_journey_url = `${book.library.url}/similar-${book.title.titleId}/page-1/${book.title.titleId}/journey/${book.title.titleId}`;
        }
        const journeyUrl = book.reading_journey_url;

        if (journeyUrl.includes('undefined')) {
            console.error(`In the book ${book.title.text} (${book.title.titleId}), the journeyUrl has undefined in it: ${journeyUrl}`);
            await browser.close();
            return;
        }

        await page.goto(journeyUrl, { waitUntil: 'networkidle0' });
        const url = await page.evaluate(() => document.URL);

        if (url.includes('libbyjourney')) {
            const response = await fetch(url);
            const data = await response.json();
            await saveJson(data);
        } else {
            console.log("Book not downloaded: " + book.title);
            console.log('Not a journey JSON URL: ' + url);
        }

        await browser.close();
    }

    const downloadPromises = books.map(book => {
        const availableSlot = Promise.race(semaphore);
        return availableSlot.then(() => {
            const downloadPromise = downloadBook(book);
            const index = semaphore.indexOf(availableSlot);
            semaphore[index] = downloadPromise.then(() => availableSlot);
            return downloadPromise;
        });
    });

    await Promise.all(downloadPromises);
}

(async () => {
    const timelineJson = require('../libbytimeline-activities.json');
    const downloadedBooksFile = '../downloaded_books.txt';
    let downloadedBooksList = readBookIdsFromFile(downloadedBooksFile);
    await downloadBooksInParallel(timelineJson.timeline, maxConcurrentTabs);
})();