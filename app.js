const express = require('express');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

// Path to the apps.json file
const dataPath = path.join('data', 'apps.json');

// Middleware to parse JSON bodies
app.use(express.json());

// Route to get all apps
app.get('/apps', (req, res) => {
    fs.readFile(dataPath, 'utf8', (err, data) => {
        if (err) {
            return res.status(500).json({ error: 'Failed to read apps data' });
        }
        const appsData = JSON.parse(data);
        res.json(appsData.apps);
    });
});

// Route to get a single app by ID
app.get('/apps/:id', (req, res) => {
    const appId = req.params.id;

    fs.readFile(dataPath, 'utf8', (err, data) => {
        if (err) {
            return res.status(500).json({ error: 'Failed to read apps data' });
        }
        const appsData = JSON.parse(data);
        const app = appsData.apps.find(a => a.id === appId);

        if (!app) {
            return res.status(404).json({ error: 'App not found' });
        }

        res.json(app);
    });
});

// Start the server
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});