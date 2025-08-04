const https = require('https');
const fs = require('fs');
const path = require('path');

const files = [
    {
        url: 'https://ajax.googleapis.com/ajax/libs/angularjs/1.8.3/angular.min.js',
        filename: 'angular.min.js'
    },
    {
        url: 'https://ajax.googleapis.com/ajax/libs/angularjs/1.8.3/angular-route.min.js',
        filename: 'angular-route.min.js'
    },
    {
        url: 'https://ajax.googleapis.com/ajax/libs/angularjs/1.8.3/angular-resource.min.js',
        filename: 'angular-resource.min.js'
    },
    {
        url: 'https://ajax.googleapis.com/ajax/libs/angularjs/1.8.3/angular-animate.min.js',
        filename: 'angular-animate.min.js'
    }
];

const downloadFile = (url, filename) => {
    return new Promise((resolve, reject) => {
        const filepath = path.join('static', 'js', 'lib', filename);
        const file = fs.createWriteStream(filepath);
        
        https.get(url, (response) => {
            response.pipe(file);
            file.on('finish', () => {
                file.close();
                console.log(`Downloaded: ${filename}`);
                resolve();
            });
        }).on('error', (err) => {
            fs.unlink(filepath, () => {}); // 删除不完整的文件
            console.error(`Error downloading ${filename}:`, err.message);
            reject(err);
        });
    });
};

const downloadAll = async () => {
    console.log('Starting AngularJS download...');
    for (const file of files) {
        try {
            await downloadFile(file.url, file.filename);
        } catch (error) {
            console.error(`Failed to download ${file.filename}`);
        }
    }
    console.log('Download completed!');
};

downloadAll(); 