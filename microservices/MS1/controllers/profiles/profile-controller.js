import * as profileDao from "./profile-dao.js";

const ProfileController = (app) => {
    app.post("/api/profile", createUpdateProfile);
    app.get("/api/profile/:userId", getProfile);
    app.post("/api/friends/request", sendFriendRequest);
    app.post("/api/friends/requests/respond", respondToFriendRequest);
    app.get("/api/friends/:userId", getFriends);
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



const sendFriendRequest = async (req, res) => {
    const { userId, friendId } = req.body;
        try {
            if(!userId || !friendId){
                return res.status(400).json({ message: 'User ID and friendId ID are required' });
            }
            if(userId===friendId){
                return res.status(400).json({ message: 'Cannot send friend request to self' });
            }
            const profile = await profileDao.findProfile(userId);
            const friendProfile = await profileDao.findProfile(friendId);
            if (!profile || !friendProfile) {
              return res.status(404).json({ message: 'Profile not found' });
            }
          // Check if friend request already exists
          const existingRequest=await profileDao.findRequest(userId, friendId);
            if(existingRequest){
                return res.status(400).json({ message: 'Friend request already exists' });
            }
            await profileDao.sendRequest(userId, friendId);
            res.status(201).json({ message: 'Friend request sent successfully' });
    } catch (err) {
        res.status(500).send({ message: "An error occurred" });
    }
}

const respondToFriendRequest = async (req, res) => {
    const { userId, friendId, status } = req.body;
    try {
        if(!userId || !friendId || !status){
            return res.status(400).json({ message: 'User ID, friend ID, and status are required' });
        }
        if(userId===friendId){
            return res.status(400).json({ message: 'Cannot send friend request to self' });
        }
        if(status!=='accepted' && status!=='declined'){
            return res.status(400).json({ message: 'Invalid status' });
        }
        const profile = await profileDao.findProfile(userId);
        const friendProfile = await profileDao.findProfile(friendId);
        if (!profile || !friendProfile) {
          return res.status(404).json({ message: 'Profile not found' });
        }
        const existingRequest=await profileDao.findRequest(friendId, userId);
        if(!existingRequest){
            return res.status(404).json({ message: 'Friend request not found' });
        }
        await profileDao.respondToRequest(userId, friendId, status);
       
        res.status(201).json({ message: 'Friend request responded successfully' });
    } catch (err) {
        res.status(500).send({ message: "An error occurred" });
    }
}

const getFriends = async (req, res) => {
    try {
        const userId = req.params.userId;
        if (!userId) {
            return res.status(400).send({ message: "User ID is required" });
        }
        const profile = await profileDao.findProfile(userId);
        if (!profile) {
            return res.status(404).send({ message: "Profile not found" });
        }
        res.send(profile.friends);
    } catch (err) {
        res.status(500).send({ message: "An error occurred" });
    }
}

export default ProfileController;
