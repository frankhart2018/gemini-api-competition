import notificationModel from "./notification-model.js";

export const createNotification = (userId, message, type,redirectionUrl=null ) => {
    return notificationModel.create({ userId, message, type, redirectionUrl });
    }

export const getNotifications = (userId) => {
    return notificationModel.find({ userId: userId });
}

export const deleteNotification = (id) => {
    return notificationModel.deleteOne({ _id: id });
}