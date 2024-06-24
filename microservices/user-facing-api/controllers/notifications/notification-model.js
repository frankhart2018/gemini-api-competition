import mongoose from "mongoose";
import notificationSchema from "./notification-schema.js";
const notificationModel = mongoose.model("notificationModel", notificationSchema);
export default notificationModel;
