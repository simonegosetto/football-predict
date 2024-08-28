const axios = require('axios');
const fs = require("node:fs");

if (process.argv.length < 3) {
    console.error('Usage: node prediction.js <fixture_id>');
    process.exit(1);
}
const date = '2024-08-28';
const fixtureId = process.argv[2];

async function run() {

    if (fs.existsSync(`${date}-${fixtureId}.json`)) {
        readPrediction();
        return;
    }

    const options = {
        method: 'GET',
        url: 'https://api-football-v1.p.rapidapi.com/v3/predictions',
        params: {fixture: fixtureId},
        headers: {
            'x-rapidapi-key': 'VuCzPmpQDVmshrHVEkS3j181FLogp1R5eY2jsns3MUThXHfJjK',
            'x-rapidapi-host': 'api-football-v1.p.rapidapi.com'
        }
    };

    try {
        const response = await axios.request(options);
        // console.log(response.data);
        fs.writeFileSync(`${date}-${fixtureId}.json`, JSON.stringify(response.data.response[0], null, 2));
        readPrediction();
    } catch (error) {
        console.error(error);
    }
}

function readPrediction() {
    const data = fs.readFileSync(`${date}-${fixtureId}.json`);
    const predictionData = JSON.parse(data);
    const {teams, predictions} = predictionData;
    console.log(`Prediction for ${teams.home.name} vs ${teams.away.name}`);
    console.log(predictions.advice);
    console.log('Under/Over:', predictions.under_over);
    // console.log('Goals:', `${predictions.goals.home} | ${predictions.goals.away}`);
    console.table(Object.entries(predictions.goals));
    console.table(Object.entries(predictions.percent));

    // console.log(prediction);
}

run().then(() => console.log('Done!'));
