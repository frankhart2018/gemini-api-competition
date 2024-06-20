import * as notificationDao from "./notification-dao.js";
import * as userDao from "../users/user-dao.js";
import {logger, LogLevel} from "../../utils/logging.js";
const notificationController = (app)=>{
app.post("/api/notification", createNotification);
app.get("/api/notification/:userId", getNotifications);
app.delete("/api/notification/:id", deleteNotification);
}

const createNotification = async (req, res) => {
    try {
        const { userId, message, type,redirectionUrl } = req.body;
        if (!userId || !message || !type) {
            return res.status(400).send({ message: "userId, message, and type are required" });
        }
        await notificationDao.createNotification(userId, message, type, redirectionUrl);
        res.status(201).send({ message: "Notification created successfully" });
    } catch (err) {
        logger.log(LogLevel.ERROR, err);
        res.status(500).send({ message: "An error occurred" });
    }
}

const getNotifications = async (req, res) => {
    try {
        const userId = req.params.userId;
        if (!userId) {
            return res.status(400).send({ message: "User ID is required" });
        }
        const user = await userDao.findUserById(userId);
        if (!user) {
            return res.status(404).send({ message: "User not found" });
        }
        const notifications = await notificationDao.getNotifications(userId);
        res.send(notifications);
    } catch (err) {
        logger.log(LogLevel.ERROR, err);
        res.status(500).send({ message: "An error occurred" });
    }
}

const deleteNotification = async (req, res) => {
    try {
        const notificationId = req.params.id;
        if (!notificationId) {
            return res.status(400).send({ message: "Notification ID is required" });
        }
        const result = await notificationDao.deleteNotification(notificationId);
        if (result.deletedCount === 0) {
            return res.status(404).send({ message: "Notification not found" });
        }
        res.send({ message: "Notification deleted successfully" });
    } catch (err) {
        logger.log(LogLevel.ERROR, err);
        res.status(500).send({ message: "An error occurred" });
    }
}
export default notificationController;