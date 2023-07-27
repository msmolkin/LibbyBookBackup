const puppeteer = require('puppeteer');
const fs = require('fs');
const { format } = require('date-fns');

// Load the JSON data file
const timelineJson = require('../libbytimeline-activities.json');

async function saveJson(data, folder = "books") {
    if (!data) {
        console.error("No data to save");
        return;
    }

    // if data is a URL, fetch it
    if (typeof data === "string") {
        const response = await fetch(data);
        data = await response.json();
    }

    // if data is a Reading Journey json file, read it
    if (data instanceof File) {
        data = await data.text();
        data = JSON.parse(data);
    }

    const timestamp = Math.max(...data.circulation.map(item => item.timestamp));
    const date1 = format(new Date(timestamp), 'yyyy-MM-dd HH-mm');
    const current_date = format(new Date(), 'yyyy-MM-dd HH-mm');
    const title = data.readingJourney.title.text.replace(/[/\\?%*:|"<>]/g, ''); // remove illegal characters from the title so it can be used as a filename
    const author = data.readingJourney.author;
    const format = data.readingJourney.cover.format;

    const filename = `Book ${date1} ${title} by ${author} ${format} notes (downloaded ${current_date}).json`;
    const path = `${folder}/${filename}`;

    if (!fs.existsSync(folder)) {
        fs.mkdirSync(folder);
    }

    fs.writeFileSync(path, JSON.stringify(data, null, 2));
}
// rename this file to ..._async.js

// Start Puppeteer
(async () => {
    const browser = await puppeteer.launch({
        headless: false,  // Change to true if Puppeteer can run in headless mode and generate the JSON files
        defaultViewport: null,
        userDataDir: '/Users/michael/Library/Application Support/Google/Chrome/LibbyProfile',
        args: ['--disable-blink-features=AutomationControlled'] // hide the fact that this is an automated browser
    });


    const page = await browser.newPage();

    // Set the request authorization headers, as per your uploaded headers
    await page.setExtraHTTPHeaders({
        // 'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiJyZWFkaXZlcnNlIiwiaXNzIjoic2VudHJ5IiwiY2hpcCI6eyJpZCI6Ijg2OWU2NmNkLTQ5ZjYtNGM2My05MzM3LTJlMjM3NGU1ZTk2OCIsInByaSI6IjA3MTc4YmU1LTAxNDYtNDgzZC04ZTlmLTk2M2EyMzFiZWJiMCIsImFnIjo5MDk0NTU5LCJhY2NvdW50cyI6W3siYWciOjkwOTQ1NTksImlkIjoiMTkyOTg3NDciLCJ0eXAiOiJsaWJyYXJ5IiwiY2FyZHMiOlt7ImlkIjoiNzE1NzE3MiIsIm5hbWUiOiIyMTkwMTAxNzQyNDU4NSIsImxpYiI6eyJpZCI6IjM3NyIsImtleSI6ImNjYyJ9fV19LHsiYWciOjkwOTQ1NTksImlkIjoiNjQ4OTgwMjIiLCJ0eXAiOiJsaWJyYXJ5IiwiY2FyZHMiOlt7ImlkIjoiNDg4MzQ4NzIiLCJuYW1lIjoiMiAxMTExIDAyMzkzIDY3MDEiLCJsaWIiOnsiaWQiOiI4OSIsImtleSI6ImJyb29rbHluIn19XX0seyJhZyI6OTA5NDU1OSwiaWQiOiI0MjA1NTQ5OCIsInR5cCI6ImxpYnJhcnkiLCJjYXJkcyI6W3siaWQiOiIyNzM3MzM5OSIsIm5hbWUiOiIyMTIyMzAzNDk4MjEwMSIsImxpYiI6eyJpZCI6IjM3MiIsImtleSI6InNmcGwifX1dfSx7ImFnIjo5MDk0NTU5LCJpZCI6IjY4MjU0OTczIiwidHlwIjoibGlicmFyeSIsImNhcmRzIjpbeyJpZCI6IjUyMTYyMTgzIiwibmFtZSI6bnVsbCwibGliIjp7ImlkIjoiMTAwNzY4Iiwia2V5IjoiY2FuZGlkIn19XX0seyJhZyI6OTA5NDU1OSwiaWQiOiI3NDc5Mjc5MSIsInR5cCI6ImxpYnJhcnkiLCJjYXJkcyI6W3siaWQiOiI1ODY0Mjg4NSIsIm5hbWUiOiIyIDMzMzMgMTIyNDggMDQ2OCIsImxpYiI6eyJpZCI6IjM3Iiwia2V5IjoibnlwbCJ9fV19XX19.cbtriZC14BX05r73PX_-Fvl_iSNy_8cl9nixFw2vgKannojHN8l_eon_2rsTY_sqHRwtO9O8enk7WZgPDY53XMSXEj8SnJ3TZhqrfJAYBRJjYT5Maev4aZeClgDoZ7lnTSxiiES-kh01mFsJvZozm7exvO1UpJzDXAgBUSisp6I677n5jF3aa8ZAzX5r5VFpI3zV_s5dMLlPdYlBuvOPZu4O_t6Ai0imia9nGS8k4DV32MeHL56igaOlhH05NL4vIy8JYvFkkc7fjaF4YvFDdXKZDkWTfNEDdLJAoqeg7MBXy6ZAlNgv9WusViROa5NIEeGKhZ-iyQErn38q5HmOJA',
        'Connection': 'keep-alive',
        // 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        // 'x-client-id': 'dewey',
        'DNT': '1',
    });

    // let readingJourneyJsonUrl;  // Create a global variable to store the URL

    // page.on('response', async (response) => {
    //     const url = response.url();
    //     if (response) console.log(response.status(), url);
    //     if (url.includes('libbyjourney')) {
    //         readingJourneyJsonUrl = url;
    //     }
    //     else {
    //         console.log('Not a journey JSON URL: ' + url);
    //     }
    // });

    // Visit each book's reading journey URL and export the data
    for (let book of timelineJson.timeline) {

        const journeyUrl = book.reading_journey_url;

        await page.goto(journeyUrl, { waitUntil: 'networkidle0' });

        // TODO: figure out why this errors out when not doing it manually and slowly
        for (let selector of ['#shelf-actions-pill-0001 > span', 'a:nth-of-type(2) > span', 'a:nth-of-type(3) > span:nth-of-type(1)']) {
            try {
                await page.waitForSelector(selector);
                await page.hover(selector);
                await page.evaluate((selector) => document.querySelector(selector).click(), selector);
                // await page.click(selector);
                // await page.waitForNavigation({waitUntil: 'networkidle2'}); // Wait for the button to be clicked
            } catch (error) {
                if (error.message == "Node is either not visible or not an HTMLElement") {
                    // If this happened, then manually just wait a few seconds and click the selector
                    await page.waitForTimeout(5000);
                    await page.evaluate((selector) => document.querySelector(selector).click(), selector);
                } else {
                    console.error("An error occurred: ", error);
                }
            }
        }

        // Wait for the download to complete
        await page.waitForNavigation({ waitUntil: 'networkidle0' });
        const url = await page.evaluate(() => document.URL);

        let readingJourneyJsonUrl;  // URL of the JSON file containing the circulation, and bookmarks and notes

        if (url.includes('libbyjourney')) {
            readingJourneyJsonUrl = url;
        }
        else {
            console.log("Book not downloaded: " + book.title)
            console.log('Not a journey JSON URL: ' + url);
        }


        // // Add the download URL to the JSON data
        // // this doesn't work because readingJourneyJsonUrl is not defined when the JSON is opened
        book["download_url"] = readingJourneyJsonUrl;

        // // Save JSON data
        await saveJson(readingJourneyJsonUrl);

    }

    await browser.close();
})();
