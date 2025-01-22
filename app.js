const express = require('express');
const { MongoClient } = require('mongodb');
const cors = require('cors');

const app = express();
const PORT = process.env.PORT || 3000;

// MongoDB connection URI
const uri = 'mongodb://mongodb:27017';
const client = new MongoClient(uri);
let db;

// Middleware
app.use(express.json());
app.use(cors({
    origin: '*', // Allow all origins (or specify specific origins if needed)
    methods: ['GET', 'POST', 'PUT', 'DELETE'],
    allowedHeaders: ['Content-Type', 'Authorization']
}));

// MongoDB Connection Function
async function connectToDatabase() {
    try {
        await client.connect();
        console.log('Connected to MongoDB');
        db = client.db('appstore');
    } catch (err) {
        console.error('Failed to connect to MongoDB:', err);
        process.exit(1);
    }
}

// Routes

// Get all apps
app.get('/apps', async (req, res) => {
    try {
        const apps = await db.collection('apps').find().toArray();
        res.json(apps);
    } catch (err) {
        console.error('Error fetching apps:', err);
        res.status(500).json({ error: 'Failed to fetch apps', details: err.message });
    }
});

// Get a single app by ID
app.get('/apps/:id', async (req, res) => {
    const appId = req.params.id;

    try {
        const app = await db.collection('apps').findOne({ _id: appId });
        if (!app) {
            return res.status(404).json({ error: 'App not found' });
        }
        res.json(app);
    } catch (err) {
        console.error('Error fetching app:', err);
        res.status(500).json({ error: 'Failed to fetch app', details: err.message });
    }
});

// Get Docker Compose file URL for an app
app.get('/apps/:id/compose', async (req, res) => {
    const appId = req.params.id;

    try {
        const app = await db.collection('apps').findOne({ _id: appId });
        if (!app) {
            return res.status(404).json({ error: 'App not found' });
        }
        const jsDelivrUrl = `https://cdn.jsdelivr.net/gh/CodingKitten-YT/docksnappy-api@master/data/apps/${app.name}/docker-compose.yml`;
        res.json({ url: jsDelivrUrl });
    } catch (err) {
        console.error('Error fetching Docker Compose URL:', err);
        res.status(500).json({ error: 'Failed to fetch Docker Compose URL', details: err.message });
    }
});

// Add a new app
app.post('/apps', async (req, res) => {
    const newApp = req.body;

    if (!newApp._id || !newApp.name || !newApp.description) {
        return res.status(400).json({ error: 'Missing required fields' });
    }

    try {
        await db.collection('apps').insertOne(newApp);
        res.status(201).json({ message: 'App added successfully', app: newApp });
    } catch (err) {
        console.error('Error adding app:', err);
        res.status(500).json({ error: 'Failed to add app', details: err.message });
    }
});

// Update an app
app.put('/apps/:id', async (req, res) => {
    const appId = req.params.id;
    const updatedApp = req.body;

    if (!updatedApp.name || !updatedApp.description) {
        return res.status(400).json({ error: 'Missing required fields' });
    }

    try {
        const result = await db.collection('apps').updateOne({ _id: appId }, { $set: updatedApp });
        if (result.matchedCount === 0) {
            return res.status(404).json({ error: 'App not found' });
        }
        res.json({ message: 'App updated successfully' });
    } catch (err) {
        console.error('Error updating app:', err);
        res.status(500).json({ error: 'Failed to update app', details: err.message });
    }
});

// Delete an app
app.delete('/apps/:id', async (req, res) => {
    const appId = req.params.id;

    try {
        const result = await db.collection('apps').deleteOne({ _id: appId });
        if (result.deletedCount === 0) {
            return res.status(404).json({ error: 'App not found' });
        }
        res.json({ message: 'App deleted successfully' });
    } catch (err) {
        console.error('Error deleting app:', err);
        res.status(500).json({ error: 'Failed to delete app', details: err.message });
    }
});

// Start Server
async function startServer() {
    await connectToDatabase();
    app.listen(PORT, () => {
        console.log(`Server is running on http://localhost:${PORT}`);
    });
}

startServer();
