const puppeteer = require('puppeteer');
const fs = require('fs');

// Load the JSON data file
const data = require('./libbytimeline-activities.json');

// Start Puppeteer
(async () => {
    const browser = await puppeteer.launch({
        headless: false,  // Change to true if Puppeteer can run in headless mode
        userDataDir: '/Users/michael/Library/Application Support/Google/Chrome/LibbyProfile',
    });
    
    
    const page = await browser.newPage();

    // Set the request authorization headers, as per your uploaded headers
    await page.setExtraHTTPHeaders({
        // 'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiJyZWFkaXZlcnNlIiwiaXNzIjoic2VudHJ5IiwiY2hpcCI6eyJpZCI6Ijg2OWU2NmNkLTQ5ZjYtNGM2My05MzM3LTJlMjM3NGU1ZTk2OCIsInByaSI6IjA3MTc4YmU1LTAxNDYtNDgzZC04ZTlmLTk2M2EyMzFiZWJiMCIsImFnIjo5MDk0NTU5LCJhY2NvdW50cyI6W3siYWciOjkwOTQ1NTksImlkIjoiMTkyOTg3NDciLCJ0eXAiOiJsaWJyYXJ5IiwiY2FyZHMiOlt7ImlkIjoiNzE1NzE3MiIsIm5hbWUiOiIyMTkwMTAxNzQyNDU4NSIsImxpYiI6eyJpZCI6IjM3NyIsImtleSI6ImNjYyJ9fV19LHsiYWciOjkwOTQ1NTksImlkIjoiNjQ4OTgwMjIiLCJ0eXAiOiJsaWJyYXJ5IiwiY2FyZHMiOlt7ImlkIjoiNDg4MzQ4NzIiLCJuYW1lIjoiMiAxMTExIDAyMzkzIDY3MDEiLCJsaWIiOnsiaWQiOiI4OSIsImtleSI6ImJyb29rbHluIn19XX0seyJhZyI6OTA5NDU1OSwiaWQiOiI0MjA1NTQ5OCIsInR5cCI6ImxpYnJhcnkiLCJjYXJkcyI6W3siaWQiOiIyNzM3MzM5OSIsIm5hbWUiOiIyMTIyMzAzNDk4MjEwMSIsImxpYiI6eyJpZCI6IjM3MiIsImtleSI6InNmcGwifX1dfSx7ImFnIjo5MDk0NTU5LCJpZCI6IjY4MjU0OTczIiwidHlwIjoibGlicmFyeSIsImNhcmRzIjpbeyJpZCI6IjUyMTYyMTgzIiwibmFtZSI6bnVsbCwibGliIjp7ImlkIjoiMTAwNzY4Iiwia2V5IjoiY2FuZGlkIn19XX0seyJhZyI6OTA5NDU1OSwiaWQiOiI3NDc5Mjc5MSIsInR5cCI6ImxpYnJhcnkiLCJjYXJkcyI6W3siaWQiOiI1ODY0Mjg4NSIsIm5hbWUiOiIyIDMzMzMgMTIyNDggMDQ2OCIsImxpYiI6eyJpZCI6IjM3Iiwia2V5IjoibnlwbCJ9fV19XX19.cbtriZC14BX05r73PX_-Fvl_iSNy_8cl9nixFw2vgKannojHN8l_eon_2rsTY_sqHRwtO9O8enk7WZgPDY53XMSXEj8SnJ3TZhqrfJAYBRJjYT5Maev4aZeClgDoZ7lnTSxiiES-kh01mFsJvZozm7exvO1UpJzDXAgBUSisp6I677n5jF3aa8ZAzX5r5VFpI3zV_s5dMLlPdYlBuvOPZu4O_t6Ai0imia9nGS8k4DV32MeHL56igaOlhH05NL4vIy8JYvFkkc7fjaF4YvFDdXKZDkWTfNEDdLJAoqeg7MBXy6ZAlNgv9WusViROa5NIEeGKhZ-iyQErn38q5HmOJA',
        // 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'x-client-id': 'dewey'
    });    

    // Visit each book's reading journey URL and export the data
    for (let book of data.timeline) {
        const journeyUrl = book.reading_journey_url;

        await page.goto(journeyUrl);

        await page.waitForSelector('#shelf-actions-pill-0001 > span');  // Actual selector of the "Actions" button
        await page.click('#shelf-actions-pill-0001 > span');
        await page.waitForSelector('a:nth-of-type(2) > span');  // Actual ID or selector of the "Export Reading Data" option
        await page.click('a:nth-of-type(2) > span');
        await page.waitForSelector('a:nth-of-type(3) > span:nth-of-type(1)');  // Actual ID or selector of the "Data" (JSON) option
        await page.click('a:nth-of-type(3) > span:nth-of-type(1)');

        // The JSON file should now be downloaded to your default download location
    }

    // Fetch the JSON data from the page
    // const data = await page.evaluate(() => {
    //     return JSON.stringify(jsonData);
    // });
    const data = await page.content();


    console.log(data);  // Send the data to stdout

    await browser.close();
})();
