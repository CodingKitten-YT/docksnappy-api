const express = require('express');
const fs = require('fs');
const path = require('path');
const axios = require('axios');
const app = express();
const cors = require('cors');

// Path to the apps.json file
const dataPath = path.join('data', 'apps.json');

// Middleware to parse JSON bodies
app.use(express.json());
app.use(cors());

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

app.get('/apps/:id/compose', async (req, res) => {
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

      // Generate the jsDelivr URL
      const jsDelivrUrl = `https://cdn.jsdelivr.net/gh/CodingKitten-YT/docksnappy-api@master/data/apps/${app.name}/docker-compose.yml`;

      // Check if the file exists on GitHub
      axios.head(jsDelivrUrl)
          .then(() => {
              res.json({ url: jsDelivrUrl });
          })
          .catch(() => {
              res.status(404).json({ error: 'Docker Compose file not found for this app' });
          });
  });
});

// Start the server
app.listen(3000, () => {
    console.log(`Server is running on http://localhost:3000`);
});