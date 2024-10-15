const net = require('net');
const fs = require('fs');

// MORE INFORMATIONS http://www.technoai.xyz

function createImage(prompt, apiKey) {
    const host = '37.114.41.55'; // DON'T CHANGE IP
    const port = 6383; // DON'T CHANGE PORT

    const client = new net.Socket();
    client.connect(port, host, () => {
        const request = {
            action: "generate",
            api: apiKey,
            prompt: prompt
        };
        client.write(JSON.stringify(request));
    });

    let response = Buffer.alloc(0);

    client.on('data', (chunk) => {
        response = Buffer.concat([response, chunk]);

        if (response.includes(Buffer.from('<END>'))) {
            const parts = response.indexOf(Buffer.from('<END>'));
            const jsonPart = response.slice(0, parts).toString();
            const imagePart = response.slice(parts + 5); // 5 =

            try {
                const responseData = JSON.parse(jsonPart);

                if (responseData.status === 'success') {
                    const imageFilename = 'generated_image.png';
                    fs.writeFileSync(imageFilename, imagePart);
                    console.log('Image saved successfully as', imageFilename);

                    client.end();
                }
            } catch (err) {
                console.error('Error parsing JSON:', err);
            }
        }
    });

    client.on('close', () => {
        console.log('Connection closed.');
    });
}

const prompt = "Dog."; // YOUR PROMPT
const apiKey = ""; // YOUR API KEY
createImage(prompt, apiKey);
