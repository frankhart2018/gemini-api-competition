import * as profileDao from "./profile-dao.js";

const ProfileController = (app) => {
    app.post("/api/profile", createUpdateProfile);
    app.get("/api/profile/:userId", getProfile);
}

const createUpdateProfile = async (req, res) => {
    try {
        const { userId, bio, age, location, interests } = req.body;
        if (!userId) {
            return res.status(400).send({ message: "User ID is required" });
        }
        if (!location || typeof location !== 'object' || !location.city || !location.country) {
            return res.status(400).send({ message: "Location must be an object with city and country properties" });
        }
        const profile = await profileDao.findProfile(userId);
        if (!profile) {
            await profileDao.createProfile(userId, bio, age, location, interests);
            return res.status(201).send({ message: "Profile created successfully" });
        }
        await profileDao.updateProfile(userId, bio, age, location, interests);
        res.send({ message: "Profile updated successfully" });
    } catch (err) {
        res.status(500).send({ message: "An error occurred" });
    }
}

const getProfile = async (req, res) => {
    try {
        const userId = req.params.userId;
        if (!userId) {
            return res.status(400).send({ message: "User ID is required" });
        }
        const profile = await profileDao.findProfile(userId);
        if (!profile) {
            return res.status(404).send({ message: "Profile not found" });
        }
        res.send(profile);
    } catch (err) {
        res.status(500).send({ message: "An error occurred" });
    }
}

export default ProfileController;
