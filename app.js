const express = require('express');
const { MongoClient } = require('mongodb');
const cors = require('cors');

const app = express();
const PORT = process.env.PORT || 3000;

// MongoDB connection URI
const uri = 'mongodb://mongodb:27017';
const client = new MongoClient(uri);

// Middleware to parse JSON bodies
app.use(express.json());
app.use(
    cors({
        origin: '*', // Allow all origins
        methods: ['GET', 'POST', 'PUT', 'DELETE'], // Allow these methods
        allowedHeaders: ['Content-Type', 'Authorization'], // Allow these headers
    })
);

// Connect to MongoDB
let db;
async function connectToMongoDB() {
    try {
        await client.connect();
        console.log('Connected to MongoDB');
        db = client.db('appstore');
    } catch (err) {
        console.error('Failed to connect to MongoDB:', err);
        process.exit(1);
    }
}

// Route to get all apps
app.get('/apps', async (req, res) => {
    try {
        const apps = await db.collection('apps').find({}, { projection: { _id: 0 } }).toArray();
        res.json(apps);
    } catch (err) {
        console.error('Error fetching apps:', err);
        res.status(500).json({ error: 'Failed to fetch apps', details: err.message });
    }
});

// Route to get a single app by ID
app.get('/apps/:id', async (req, res) => {
    const appId = req.params.id;

    try {
        const app = await db.collection('apps').findOne({ ID: appId }, { projection: { _id: 0 } });
        if (!app) {
            return res.status(404).json({ error: 'App not found' });
        }
        res.json(app);
    } catch (err) {
        console.error('Error fetching app:', err);
        res.status(500).json({ error: 'Failed to fetch app', details: err.message });
    }
});

// Route to get the Docker Compose file URL for an app
app.get('/apps/:id/compose', async (req, res) => {
    const appId = req.params.id;

    try {
        const app = await db.collection('apps').findOne({ ID: appId }, { projection: { _id: 0 } });
        if (!app) {
            return res.status(404).json({ error: 'App not found' });
        }

        res.json({ url: app.docker_compose_url });
    } catch (err) {
        console.error('Error fetching Docker Compose URL:', err);
        res.status(500).json({ error: 'Failed to fetch Docker Compose URL', details: err.message });
    }
});

// Route to add a new app
app.post('/apps', async (req, res) => {
    const newApp = req.body;

    if (!newApp.ID || !newApp.Name || !newApp.Description) {
        return res.status(400).json({ error: 'Missing required fields' });
    }

    try {
        // Ensure the `ID` is unique
        const existingApp = await db.collection('apps').findOne({ ID: newApp.ID });
        if (existingApp) {
            return res.status(409).json({ error: 'App with this ID already exists' });
        }

        // Insert the app, suppressing MongoDB's `_id`
        await db.collection('apps').insertOne({ ...newApp });
        res.status(201).json({ message: 'App added successfully', app: newApp });
    } catch (err) {
        console.error('Error adding app:', err);
        res.status(500).json({ error: 'Failed to add app', details: err.message });
    }
});

// Route to update an app
app.put('/apps/:id', async (req, res) => {
    const appId = req.params.id;
    const updatedApp = req.body;

    if (!updatedApp.Name || !updatedApp.Description) {
        return res.status(400).json({ error: 'Missing required fields' });
    }

    try {
        const result = await db.collection('apps').updateOne(
            { ID: appId },
            { $set: updatedApp }
        );

        if (result.matchedCount === 0) {
            return res.status(404).json({ error: 'App not found' });
        }

        res.json({ message: 'App updated successfully' });
    } catch (err) {
        console.error('Error updating app:', err);
        res.status(500).json({ error: 'Failed to update app', details: err.message });
    }
});

// Route to delete an app
app.delete('/apps/:id', async (req, res) => {
    const appId = req.params.id;

    try {
        const result = await db.collection('apps').deleteOne({ ID: appId });

        if (result.deletedCount === 0) {
            return res.status(404).json({ error: 'App not found' });
        }

        res.json({ message: 'App deleted successfully' });
    } catch (err) {
        console.error('Error deleting app:', err);
        res.status(500).json({ error: 'Failed to delete app', details: err.message });
    }
});

// Start the server after connecting to MongoDB
async function startServer() {
    await connectToMongoDB();
    app.listen(PORT, () => {
        console.log(`Server is running on http://localhost:${PORT}`);
    });
}

startServer();
