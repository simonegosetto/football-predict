const axios = require('axios');
const fs = require('fs');

const date = '2024-08-28';

async function run() {
    const options = {
        method: 'GET',
        url: 'https://api-football-v1.p.rapidapi.com/v3/fixtures',
        params: {date},
        headers: {
            'x-rapidapi-key': 'VuCzPmpQDVmshrHVEkS3j181FLogp1R5eY2jsns3MUThXHfJjK',
            'x-rapidapi-host': 'api-football-v1.p.rapidapi.com'
        }
    };

    try {
        const response = await axios.request(options);
        // console.log(response.data);
        fs.writeFileSync(`${date}.json`, JSON.stringify(response.data, null, 2));
    } catch (error) {
        console.error(error);
    }
}

run().then(() => console.log('Done!'));
